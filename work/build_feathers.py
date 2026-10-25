# -*- coding: utf-8 -*-
import bpy, bmesh, math
from mathutils import Vector
import sys, os
WORK=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import spec, lib

for ob in list(bpy.data.objects):
    if ob.type=='MESH' and ob.name.startswith('GEO-Wing'):
        lib.delete_obj(ob.name)

wing_m=lib.mat('M_Wing', spec.COLORS['wing'], 0.10, 0.42, sheen=0.25)
wing2=lib.mat('M_WingCovert', spec.COLORS['wing2'], 0.08, 0.38, sheen=0.2)
rig=bpy.data.objects['RIG-Reinforce']

def feather(name, root, d, N, L, W, matobj, bow=0.025, ridge=0.0):
    d=Vector(d).normalized(); N=Vector(N).normalized()
    wdir=d.cross(N).normalized()
    nu,seg=12,12
    th=0.0009
    verts=[]; rings=[]
    for i in range(nu):
        u=i/(nu-1.0)
        center=Vector(root)+d*(u*L)+N*(bow*math.sin(math.pi*u))
        rx=W*0.5*(0.18+0.92*(math.sin(math.pi*u)**0.65))*max(0.05,1.0-u**8)
        rx=max(0.0022,rx)
        ring=[]
        for k in range(seg):
            a=2*math.pi*k/seg
            p=center+wdir*(rx*math.cos(a))+N*(th*math.sin(a))
            ring.append(len(verts)); verts.append((p.x,p.y,p.z))
        rings.append(ring)
    faces=[]
    for i in range(nu-1):
        for k in range(seg):
            a=rings[i][k]; b=rings[i][(k+1)%seg]; c=rings[i+1][(k+1)%seg]; d2=rings[i+1][k]
            faces.append((a,b,c,d2))
    faces.append(tuple(reversed(rings[0])))
    faces.append(tuple(rings[-1]))
    ob=lib.new_obj(name,verts,faces,'COL_Wings',matobj,smooth=True)
    bm=bmesh.new(); bm.from_mesh(ob.data)
    bmesh.ops.reverse_faces(bm, faces=list(bm.faces))
    bm.to_mesh(ob.data); bm.free()
    return ob

def add_mod(ob):
    md=ob.modifiers.new('Armature','ARMATURE'); md.object=rig
    ob.parent=rig; ob.matrix_parent_inverse=rig.matrix_world.inverted()

def wfeather(ob, side, upper):
    if upper:
        root=Vector((0.07 if side=='L' else -0.07,0.09,1.290)); Lmax=1.12
        names=['wing_up_'+side+'_01','wing_up_'+side+'_02','wing_up_'+side+'_03']
    else:
        root=Vector((0.08 if side=='L' else -0.08,0.09,1.180)); Lmax=0.90
        names=['wing_low_'+side+'_01','wing_low_'+side+'_02','wing_low_'+side+'_03']
    groups=[ob.vertex_groups.new(name=n) for n in names]
    for v in ob.data.vertices:
        t=max(0.0,min(1.0,(v.co-root).length/max(1e-9,Lmax)))
        ws=[max(0.0,1.0-abs(t-0.20)/0.45),max(0.0,1.0-abs(t-0.55)/0.40),max(0.0,1.0-abs(t-0.90)/0.40)]
        s=sum(ws)
        if s<1e-9: ws=[1,0,0]; s=1
        for g,ww in zip(groups,ws):
            g.add([v.index],ww/s,'REPLACE')
    add_mod(ob)


def build_backing(side,sx,upper):
    if upper:
        root=Vector((sx*0.070,0.090,1.290)); U=Vector((sx*1.0,0.25,0.0)); V=Vector((0,0,1))
        ang0,ang1,Lmax=(-13.0,66.0,1.02); tag='Upper'
    else:
        root=Vector((sx*0.080,0.090,1.180)); U=Vector((sx*1.0,0.20,-0.10)); V=Vector((0,0,1))
        ang0,ang1,Lmax=(-107.0,-33.0,0.82); tag='Lower'
    N=U.cross(V).normalized(); na,nr=16,7
    verts=[]; rows=[]
    for ia in range(na):
        t=ia/(na-1.0); a=math.radians(ang0+(ang1-ang0)*t)
        d=(math.cos(a)*U+math.sin(a)*V).normalized()
        row=[]
        for ir in range(nr):
            r=0.10+0.84*(ir/(nr-1.0))
            p=root+d*(Lmax*r)+N*(-sx*(0.060-0.015*math.sin(math.pi*r)))
            row.append(len(verts)); verts.append((p.x,p.y,p.z))
        rows.append(row)
    faces=[]
    for ia in range(na-1):
        for ir in range(nr-1):
            a=rows[ia][ir]; b=rows[ia][ir+1]; c=rows[ia+1][ir+1]; d2=rows[ia+1][ir]
            faces.append((a,b,c,d2))
    ob=lib.new_obj('GEO-Wing_%s_%s_Backing'%(tag,side),verts,faces,'COL_Wings',wing_m,smooth=True)
    lib.solidify(ob,0.0015,0.0)
    wfeather(ob,side,upper)
    return ob

def build_wing(side,sx,upper):
    if upper:
        root=Vector((sx*0.070,0.090,1.290)); U=Vector((sx*1.0,0.25,0.0)); V=Vector((0,0,1))
        ang0,ang1,Lmax=(-18.0,70.0,1.12); n_prim,n_cov=13,6
    else:
        root=Vector((sx*0.080,0.090,1.180)); U=Vector((sx*1.0,0.20,-0.10)); V=Vector((0,0,1))
        ang0,ang1,Lmax=(-112.0,-28.0,0.90); n_prim,n_cov=11,5
    N=U.cross(V).normalized()
    tag='Upper' if upper else 'Lower'
    # primaries
    for i in range(n_prim):
        t=i/(n_prim-1.0)
        a=math.radians(ang0+(ang1-ang0)*t)
        d=(math.cos(a)*U+math.sin(a)*V).normalized()
        L=Lmax*(0.72+0.28*math.sin(math.pi*t)**0.7)
        W=Lmax*(0.115+0.045*math.sin(math.pi*t))
        r=root+d*0.018
        ob=feather('GEO-Wing_%s_%s_F%02d'%(tag,side,i),r,d,N,L,W,wing_m)
        wfeather(ob,side,upper)
    # coverts
    for i in range(n_cov):
        t=i/(n_cov-1.0)
        a=math.radians(ang0+8+(ang1-ang0-12)*t)
        d=(math.cos(a)*U+math.sin(a)*V).normalized()
        L=Lmax*(0.38+0.12*math.sin(math.pi*t))
        W=Lmax*(0.085+0.030*math.sin(math.pi*t))
        r=root+d*0.025+N*0.022
        ob=feather('GEO-Wing_%s_%s_C%02d'%(tag,side,i),r,d,N,L,W,wing2,bow=0.015,ridge=0.004)
        wfeather(ob,side,upper)

for side,sx in (('L',1),('R',-1)):
    build_backing(side,sx,True)
    build_backing(side,sx,False)
    build_wing(side,sx,True)
    build_wing(side,sx,False)
print('FEATHERS_OK', len([o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('GEO-Wing')]))
bpy.ops.wm.save_as_mainfile(filepath=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/Reinforce_Eins_TV.blend")
