# -*- coding: utf-8 -*-
import bpy, math
from mathutils import Vector
rig=bpy.data.objects['RIG-Reinforce']
sc=bpy.context.scene
sc.frame_set(1)
# ensure object mode and rig active
bpy.context.view_layer.objects.active=rig
rig.select_set(True)
try:
    if bpy.context.object and bpy.context.object.mode!='OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
except Exception as _e:
    print('mode_set warn', _e)

# ---------- add bones ----------
bpy.ops.object.mode_set(mode='EDIT')
E=rig.data.edit_bones
def eb(name, head, tail, parent, deform=True, connect=False):
    b=E.new(name); b.head=Vector(head); b.tail=Vector(tail)
    if parent is not None:
        b.parent=parent; b.use_connect=bool(connect)
    b.use_deform=bool(deform)
    return b
rootb=E['root']; pelvis=E['pelvis']; chest=E['chest']

# controls
for side,sx in (('L',1),('R',-1)):
    c1=eb('CTRL-foot_IK_'+side,(sx*0.075,0.0,0.060),(sx*0.075,-0.120,0.020),rootb,False)
    eb('CTRL-knee_pole_'+side,(sx*0.085,-0.350,0.500),(sx*0.085,-0.350,0.600),rootb,False)
    c2=eb('CTRL-hand_IK_'+side,(sx*0.475,0.0,0.905),(sx*0.525,-0.005,0.815),rootb,False)
    eb('CTRL-elbow_pole_'+side,(sx*0.335,0.300,1.110),(sx*0.335,0.300,1.210),rootb,False)

# skirt bones
eb('skirt_F',(0.0,-0.080,1.000),(0.0,-0.140,0.780),pelvis,True)
eb('skirt_B',(0.0, 0.080,1.000),(0.0, 0.140,0.780),pelvis,True)
eb('skirt_L',( 0.100,0.0,1.000),( 0.160,0.0,0.780),pelvis,True)
eb('skirt_R',(-0.100,0.0,1.000),(-0.160,0.0,0.780),pelvis,True)

# fingers
def bbox_obj(nm):
    o=bpy.data.objects.get(nm)
    if not o: return None
    vs=[o.matrix_world @ v.co for v in o.data.vertices]
    return (Vector((min(v.x for v in vs),min(v.y for v in vs),min(v.z for v in vs))),
            Vector((max(v.x for v in vs),max(v.y for v in vs),max(v.z for v in vs))))
for side,sx in (('L',1),('R',-1)):
    h=E['hand_'+side]
    for i in range(4):
        bb=bbox_obj('GEO-Finger_%s_%d'%(side,i))
        if not bb: continue
        mn,mx=bb
        # base near palm: for L larger x is tip; base x=mn.x, tip x=mx.x
        yc=(mn.y+mx.y)*0.5
        base=Vector((mn.x if sx>0 else mx.x, yc, mx.z))
        tip=Vector((mx.x if sx>0 else mn.x, yc, mn.z))
        mid=(base+tip)*0.5
        b1=eb('finger_%s_%d_01'%(side,i),base,mid,h,True)
        eb('finger_%s_%d_02'%(side,i),mid,tip,b1,True,True)
    bb=bbox_obj('GEO-Thumb_'+side)
    if bb:
        mn,mx=bb
        base=Vector((mn.x if sx>0 else mx.x, mx.y, mx.z))
        tip=Vector((mx.x if sx>0 else mn.x, mn.y, mn.z))
        mid=(base+tip)*0.5
        b1=eb('thumb_%s_01'%side,base,mid,h,True)
        eb('thumb_%s_02'%side,mid,tip,b1,True,True)

bpy.ops.object.mode_set(mode='OBJECT')
print('BONES_NOW',len(rig.data.bones))

# ---------- IK constraints ----------
for side in ('L','R'):
    for bn,tgt,pole in (('shin_'+side,'CTRL-foot_IK_'+side,'CTRL-knee_pole_'+side),
                        ('forearm_'+side,'CTRL-hand_IK_'+side,'CTRL-elbow_pole_'+side)):
        pb=rig.pose.bones[bn]
        for c in list(pb.constraints):
            if c.type=='IK': pb.constraints.remove(c)
        c=pb.constraints.new('IK'); c.name='IK_'+bn
        c.target=rig; c.subtarget=tgt
        c.pole_target=rig; c.pole_subtarget=pole
        c.chain_count=2; c.use_stretch=False
        # pole angle: try 0; adjust after visual test
        c.pole_angle=math.radians(0)

# ---------- weights: hands/fingers ----------
def clear(ob):
    for vg in list(ob.vertex_groups): ob.vertex_groups.remove(vg)
def vg(ob,n):
    g=ob.vertex_groups.get(n) or ob.vertex_groups.new(name=n); return g
def t_on(p,a,b):
    ab=b-a; return max(0.0,min(1.0,(p-a).dot(ab)/max(1e-12,ab.length_squared)))

for side in ('L','R'):
    palm=bpy.data.objects.get('GEO-Hand_'+side)
    if palm:
        clear(palm); g=vg(palm,'hand_'+side); g.add([v.index for v in palm.data.vertices],1.0,'REPLACE')
    for i in range(4):
        ob=bpy.data.objects.get('GEO-Finger_%s_%d'%(side,i))
        if not ob: continue
        clear(ob)
        b1=rig.data.bones['finger_%s_%d_01'%(side,i)]; b2=rig.data.bones['finger_%s_%d_02'%(side,i)]
        g1=vg(ob,b1.name); g2=vg(ob,b2.name)
        a=b1.head_local; b=b2.tail_local
        for v in ob.data.vertices:
            t=t_on(v.co,a,b)
            g1.add([v.index],1.0-t,'REPLACE'); g2.add([v.index],t,'REPLACE')
    ob=bpy.data.objects.get('GEO-Thumb_'+side)
    if ob:
        clear(ob)
        b1=rig.data.bones['thumb_%s_01'%side]; b2=rig.data.bones['thumb_%s_02'%side]
        g1=vg(ob,b1.name); g2=vg(ob,b2.name)
        a=b1.head_local; b=b2.tail_local
        for v in ob.data.vertices:
            t=t_on(v.co,a,b)
            g1.add([v.index],1.0-t,'REPLACE'); g2.add([v.index],t,'REPLACE')

# add armature mods/parent for hand objects
for nm in [n for n in bpy.data.objects.keys() if n.startswith(('GEO-Hand','GEO-Finger','GEO-Thumb'))]:
    ob=bpy.data.objects[nm]
    if not any(m.type=='ARMATURE' for m in ob.modifiers):
        md=ob.modifiers.new('Armature','ARMATURE'); md.object=rig
    ob.parent=rig; ob.matrix_parent_inverse=rig.matrix_world.inverted()

# ---------- skirt weights ----------
sk=bpy.data.objects.get('GEO-Dress_Skirt')
if sk:
    clear(sk)
    gp=vg(sk,'pelvis'); gf=vg(sk,'skirt_F'); gb=vg(sk,'skirt_B'); gl=vg(sk,'skirt_L'); gr=vg(sk,'skirt_R')
    for v in sk.data.vertices:
        x,y,z=v.co
        t=max(0.0,min(1.0,(1.005-z)/0.220))
        wf=max(0.0,-y); wb=max(0.0,y); wl=max(0.0,x); wr=max(0.0,-x)
        s=wf+wb+wl+wr
        if s<1e-9: wf=1.0; s=1.0
        wf/=s; wb/=s; wl/=s; wr/=s
        gp.add([v.index],1.0-t,'REPLACE')
        gf.add([v.index],t*wf,'REPLACE'); gb.add([v.index],t*wb,'REPLACE')
        gl.add([v.index],t*wl,'REPLACE'); gr.add([v.index],t*wr,'REPLACE')

bpy.context.view_layer.update()
print('RIG_UPGRADE_DONE bones=%d'%len(rig.data.bones))
print('UNWEIGHTED', [o.name for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('GEO-') and any(sum(g.weight for g in v.groups)<1e-4 for v in o.data.vertices)])
bpy.ops.wm.save_as_mainfile(filepath=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/Reinforce_Eins_TV.blend")
