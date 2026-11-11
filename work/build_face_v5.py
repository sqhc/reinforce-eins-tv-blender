# -*- coding: utf-8 -*-
import bpy, bmesh, math, sys
from mathutils import Vector
WORK=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import lib

BASE=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
rig=bpy.data.objects['RIG-Reinforce']; scene=bpy.context.scene
coll=lib.coll('COL_Head')
M_WHITE=bpy.data.materials['M_EyeWhite']; M_IRIS=bpy.data.materials['M_Iris']; M_PUPIL=bpy.data.materials['M_Pupil']; M_LASH=bpy.data.materials['M_Lash']; M_SKIN=bpy.data.materials['M_Skin']

CX=0.04005; CY=-0.0645; CZ=1.5480
RX=0.0242; RY=0.0080; RZ=0.0135
S=1.015

# remove old eye system
for ob in list(bpy.data.objects):
    if ob.type=='MESH' and (ob.name in ('GEO-Eye_L','GEO-Eye_R') or ob.name.startswith(('GEO-Eyeball','GEO-Eyelid','GEO-Iris','GEO-BlinkLid','GEO-Lash'))):
        bpy.data.objects.remove(ob, do_unlink=True)

# facial bones
bpy.context.view_layer.objects.active=rig
try: bpy.ops.object.mode_set(mode='EDIT')
except Exception: pass
eb=rig.data.edit_bones
for n in ['Pupil_L','Pupil_R','Lid_Up_L','Lid_Up_R','Lid_Dn_L','Lid_Dn_R']:
    if n in eb: eb.remove(eb[n])
head=eb['head']
def add_bone(name,h,t):
    b=eb.new(name); b.head=h; b.tail=t; b.parent=head; b.use_connect=False; b.use_deform=True
for side,sx in (('L',1),('R',-1)):
    cx=sx*CX
    add_bone('Pupil_'+side,(cx,CY,CZ),(cx,CY-0.020,CZ))
    add_bone('Lid_Up_'+side,(cx,CY,CZ+RZ*0.8),(cx,CY,CZ+RZ*1.35))
    add_bone('Lid_Dn_'+side,(cx,CY,CZ-RZ*0.8),(cx,CY,CZ-RZ*1.35))
try: bpy.ops.object.mode_set(mode='OBJECT')
except Exception: pass

def recalc(ob):
    bm=bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(ob.data); bm.free()

def add_arm(ob,bone):
    vg=ob.vertex_groups.new(name=bone); vg.add([v.index for v in ob.data.vertices],1.0,'REPLACE')
    md=ob.modifiers.new('Armature','ARMATURE'); md.object=rig
    ob.parent=rig; ob.matrix_parent_inverse=rig.matrix_world.inverted()

def make_obj(name, verts, faces, mats):
    me=bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts],[],[tuple(f) for f in faces]); me.update()
    ob=bpy.data.objects.new(name,me); coll.objects.link(ob)
    for m in mats: me.materials.append(m)
    for p in me.polygons: p.use_smooth=True
    recalc(ob)
    return ob


def lash_upper(side,sx):
    cx=sx*CX; pts=[]; rad=[]
    for i in range(9):
        t=-1.0+2.0*i/8
        x=cx+0.0225*t
        z=CZ+0.0105-0.0042*(abs(t)**2)
        y=-0.0748
        pts.append((x,y,z)); rad.append(0.0016)
    ob=lib.tube('GEO-Lash_Up_'+side,pts,rad,'COL_Head',M_LASH,n=8,caps=True)
    add_arm(ob,'Lid_Up_'+side)

def eyeball(side,sx):
    cx=sx*CX
    bm=bmesh.new(); bmesh.ops.create_uvsphere(bm,u_segments=64,v_segments=32,radius=1.0)
    for v in bm.verts:
        v.co=Vector((cx+v.co.x*RX, CY+v.co.y*RY, CZ+v.co.z*RZ))
    for f in bm.faces: f.material_index=0
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    me=bpy.data.meshes.new('GEO-Eyeball_'+side); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new('GEO-Eyeball_'+side,me); coll.objects.link(ob)
    me.materials.append(M_WHITE)
    for p in me.polygons: p.use_smooth=True
    add_arm(ob,'Pupil_'+side)

def iris(side,sx):
    cx=sx*CX; IRX=0.0142; IRZ=0.0098; NR=7; NS=64; TH=0.0012
    verts=[]; faces=[]
    def pt(u,vv,back):
        x=cx+IRX*u; z=CZ+IRZ*vv
        y=CY-RY*math.sqrt(max(0.0,1.0-(x-cx)**2/RX**2-(z-CZ)**2/RZ**2))-0.0007
        if back: y+=TH
        return (x,y,z)
    # front center + back center
    verts.append(pt(0,0,False)); verts.append(pt(0,0,True))
    fr=[]; br=[]
    for i in range(1,NR+1):
        rr=i/NR; frow=[]; brow=[]
        for j in range(NS):
            a=2*math.pi*j/NS; u=rr*math.cos(a); vv=rr*math.sin(a)
            frow.append(len(verts)); verts.append(pt(u,vv,False))
            brow.append(len(verts)); verts.append(pt(u,vv,True))
        fr.append(frow); br.append(brow)
    # front faces
    for j in range(NS): faces.append((0,fr[0][j],fr[0][(j+1)%NS]))
    for i in range(NR-1):
        for j in range(NS):
            a=fr[i][j]; b=fr[i][(j+1)%NS]; c=fr[i+1][(j+1)%NS]; d=fr[i+1][j]
            faces.append((a,b,c,d))
    # back faces reversed
    for j in range(NS): faces.append((1,br[0][(j+1)%NS],br[0][j]))
    for i in range(NR-1):
        for j in range(NS):
            a=br[i][j]; b=br[i][(j+1)%NS]; c=br[i+1][(j+1)%NS]; d=br[i+1][j]
            faces.append((d,c,b,a))
    # rim
    for j in range(NS):
        j2=(j+1)%NS
        faces.append((fr[-1][j],br[-1][j],br[-1][j2],fr[-1][j2]))
    ob=make_obj('GEO-Iris_'+side,verts,faces,[M_IRIS,M_PUPIL])
    for p in ob.data.polygons:
        c=p.center; u=(c.x-cx)/IRX; vv=(c.z-CZ)/IRZ
        if math.hypot(u,vv)<0.42: p.material_index=1
    add_arm(ob,'Pupil_'+side)

def blink_card(side,sx):
    cx=sx*CX; RX2=0.027; RZ2=0.0155; NR=6; NS=48; TH=0.0010
    y0=-0.055
    verts=[]; faces=[]
    verts.append((cx,y0-TH/2,CZ)); verts.append((cx,y0+TH/2,CZ))
    fr=[]; br=[]
    for i in range(1,NR+1):
        rr=i/NR; frow=[]; brow=[]
        for j in range(NS):
            a=2*math.pi*j/NS; x=cx+RX2*rr*math.cos(a); z=CZ+RZ2*rr*math.sin(a)
            frow.append(len(verts)); verts.append((x,y0-TH/2,z))
            brow.append(len(verts)); verts.append((x,y0+TH/2,z))
        fr.append(frow); br.append(brow)
    for j in range(NS): faces.append((0,fr[0][j],fr[0][(j+1)%NS]))
    for i in range(NR-1):
        for j in range(NS):
            a=fr[i][j]; b=fr[i][(j+1)%NS]; c=fr[i+1][(j+1)%NS]; d=fr[i+1][j]
            faces.append((a,b,c,d))
    for j in range(NS): faces.append((1,br[0][(j+1)%NS],br[0][j]))
    for i in range(NR-1):
        for j in range(NS):
            a=br[i][j]; b=br[i][(j+1)%NS]; c=br[i+1][(j+1)%NS]; d=br[i+1][j]
            faces.append((d,c,b,a))
    for j in range(NS):
        j2=(j+1)%NS
        faces.append((fr[-1][j],br[-1][j],br[-1][j2],fr[-1][j2]))
    ob=make_obj('GEO-BlinkLid_'+side,verts,faces,[M_SKIN,M_LASH])
    for p in ob.data.polygons:
        c=p.center
        if c.z>CZ+0.0136: p.material_index=1
    ob.shape_key_add(name='Basis')
    kb=ob.shape_key_add(name='blink')
    for i,v in enumerate(ob.data.vertices):
        co=v.co; kb.data[i].co=(co.x,-0.0765,co.z)
    for k in ob.data.shape_keys.key_blocks:
        if k.name!='Basis': k.value=0.0
    add_arm(ob,'Lid_Up_'+side)

def lid(side,sx,upper):
    cx=sx*CX; NF=10; NS=9
    us=[-0.97+1.94*i/(NF-1) for i in range(NF)]
    verts=[]; faces=[]
    for s in range(NS+1):
        t=s/NS
        for u in us:
            base=math.sqrt(max(0.0,1.0-u*u))
            if upper:
                ve=0.72*base; vv=ve+(1.0-ve)*t
            else:
                ve=-0.72*base; vv=ve+(-1.0-ve)*t
            x=cx+RX*S*u; z=CZ+RZ*S*vv
            y=CY-RY*S*math.sqrt(max(0.0,1.0-u*u-vv*vv))+0.025*(abs(u)**2)
            verts.append((x,y,z))
    for s in range(NS):
        for i in range(NF-1):
            a=s*NF+i; b=a+1; c=a+1+NF; d=a+NF
            faces.append((a,b,c,d))
    ob=lib.new_obj('GEO-Eyelid_%s_%s'%('Up' if upper else 'Dn',side),verts,faces,'COL_Head',M_SKIN,smooth=True)
    ob.data.materials.append(M_LASH)
    if upper:
        for fi in range(NF-1): ob.data.polygons[fi].material_index=1
    recalc(ob)
    lib.solidify(ob,0.0012,0.0); recalc(ob)
    ob.shape_key_add(name='Basis')
    specs=({'squint':(-0.004,-0.0010),'wide_open':(0.003,0.0008)} if upper else {'squint':(0.002,-0.0008),'wide_open':(-0.002,0.0006)})
    for kn,(dz,dy) in specs.items():
        kb=ob.shape_key_add(name=kn)
        for i,v in enumerate(ob.data.vertices):
            co=v.co; kb.data[i].co=(co.x,co.y+dy,co.z+dz)
    for k in ob.data.shape_keys.key_blocks:
        if k.name!='Basis': k.value=0.0
    add_arm(ob,'Lid_Up_'+side if upper else 'Lid_Dn_'+side)

for side,sx in (('L',1),('R',-1)):
    eyeball(side,sx); iris(side,sx); blink_card(side,sx); lid(side,sx,True); lid(side,sx,False); lash_upper(side,sx)

# mouth shape keys
m=bpy.data.objects['GEO-Mouth']
if not m.data.shape_keys:
    m.shape_key_add(name='Basis')
    xs=[v.co.x for v in m.data.vertices]; w=max(1e-6,max(abs(x) for x in xs))
    for name in ('smile','open'):
        kb=m.shape_key_add(name=name)
        for i,v in enumerate(m.data.vertices):
            x,y,z=v.co
            if name=='smile': kb.data[i].co=(x,y,z+0.0058*(abs(x)/w)**1.4)
            else: kb.data[i].co=(x,y,z-0.0072*(1.0-abs(x)/w))
    for k in m.data.shape_keys.key_blocks:
        if k.name!='Basis': k.value=0.0

print('FACE_V5',len([o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('GEO-Eyeball','GEO-Eyelid','GEO-Iris','GEO-BlinkLid'))]),'bones',len(rig.data.bones))
bpy.ops.wm.save_as_mainfile(filepath=BASE+'Reinforce_Eins_TV.blend')
