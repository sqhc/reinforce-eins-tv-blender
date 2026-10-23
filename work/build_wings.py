# -*- coding: utf-8 -*-
import bpy, math, sys, os
from mathutils import Vector
WORK = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import spec, lib

for ob in list(bpy.data.objects):
    if ob.type=='MESH' and ob.name.startswith('GEO-Wing'):
        lib.delete_obj(ob.name)

wing_m = lib.mat('M_Wing', spec.COLORS['wing'], 0.10, 0.42, sheen=0.25)
wing2 = lib.mat('M_WingCovert', spec.COLORS['wing2'], 0.08, 0.38, sheen=0.2)

def make_fan(name, root, U, V, ang0, ang1, Lmax, nf, n_u=40, n_v=8, r0=0.025,
             scale=1.0, ofs=0.0, matobj=wing_m, edge_min=0.86):
    U = Vector(U).normalized(); V = Vector(V).normalized()
    N = U.cross(V).normalized()
    root = Vector(root)
    verts=[]; 
    for i in range(n_u):
        u = i/(n_u-1.0)
        th = math.radians(ang0 + (ang1-ang0)*u)
        d = (math.cos(th)*U + math.sin(th)*V).normalized()
        L = Lmax * scale * (0.80 + 0.20*math.sin(math.pi*u))
        f = (u*nf) % 1.0
        edge = L * (edge_min + (1.0-edge_min)*(1.0-f))
        for j in range(n_v):
            v = j/(n_v-1.0)
            r = r0 + (edge-r0)*v
            bump = 0.0020*math.sin(2*math.pi*f) * v
            groove = -0.0035*math.exp(-((f-0.0)/0.10)**2) * v
            p = root + d*r + N*(bump+groove+ofs + 0.045*math.sin(math.pi*v)*math.sin(math.pi*u))
            verts.append((p.x,p.y,p.z))
    faces=[]
    for i in range(n_u-1):
        for j in range(n_v-1):
            a=i*n_v+j; b=a+1; c=(i+1)*n_v+j+1; d=(i+1)*n_v+j
            faces.append((a,b,c,d))
    ob=lib.new_obj(name, verts, faces, 'COL_Wings', matobj, smooth=True)
    # orient normals outward from body (toward front)
    import bmesh as _bm
    bm=_bm.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
    for f in bm.faces:
        if f.normal.dot(Vector((0,-1,0))) < 0:
            f.normal_flip()
    bm.to_mesh(ob.data); bm.free(); ob.data.update()
    lib.solidify(ob, 0.004, 0.0)
    return ob

def make_wing(side, sx):
    # upper
    root = (sx*0.070, 0.090, 1.290)
    U = (sx*1.0, 0.25, 0.0); V=(0,0,1)
    make_fan('GEO-Wing_Upper_'+side+'_Fan', root, U, V, -36, 64, 1.12, 30, n_u=72, n_v=10, edge_min=0.94)
    make_fan('GEO-Wing_Upper_'+side+'_Covert', root, U, V, -32, 60, 1.12, 24, n_u=44, n_v=5,
             scale=0.52, ofs=0.014, matobj=wing2, edge_min=0.92)
    # lower
    root2 = (sx*0.080, 0.090, 1.180)
    U2 = (sx*1.0, 0.20, -0.10); V2=(0,0,1)
    make_fan('GEO-Wing_Lower_'+side+'_Fan', root2, U2, V2, -98, 2, 0.90, 24, n_u=56, n_v=9, edge_min=0.94)
    make_fan('GEO-Wing_Lower_'+side+'_Covert', root2, U2, V2, -94, 0, 0.90, 20, n_u=38, n_v=5,
             scale=0.52, ofs=0.014, matobj=wing2, edge_min=0.92)

for side, sx in (('L',1),('R',-1)):
    make_wing(side, sx)

print('WINGS_OK')
for ob in bpy.data.objects:
    if ob.type=='MESH' and ob.name.startswith('GEO-Wing'):
        zs=[v.co.z for v in ob.data.vertices]; xs=[v.co.x for v in ob.data.vertices]
        print(ob.name, len(ob.data.vertices), 'x[%.2f,%.2f] z[%.2f,%.2f]'%(min(xs),max(xs),min(zs),max(zs)))
