# -*- coding: utf-8 -*-
import bpy, bmesh, math
from mathutils import Vector, Matrix
import sys, os
WORK=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import spec, lib

for ob in list(bpy.data.objects):
    if ob.type=='MESH' and ob.name.startswith(('GEO-Boot','GEO-Stocking','GEO-Shoe','GEO-Sock')):
        lib.delete_obj(ob.name)

dress=lib.mat('M_Dress', spec.COLORS['dress'], 0.0, 0.72)
boot=lib.mat('M_Boot', spec.COLORS['boot'], 0.0, 0.40)
stock=lib.mat('M_Stocking', spec.COLORS['stocking'], 0.0, 0.55)
gold=lib.mat('M_Gold', spec.COLORS['gold'], 0.85, 0.32)

def leg_x(z, sx):
    if z>=0.448:
        f=(0.87-z)/(0.87-0.448); return sx*(0.090+(0.085-0.090)*f)
    f=(0.448-z)/(0.448-0.06); return sx*(0.085+(0.075-0.085)*f)

def one(ob, bone):
    vg=ob.vertex_groups.new(name=bone)
    vg.add([v.index for v in ob.data.vertices],1.0,'REPLACE')

def add_mod(ob):
    rig=bpy.data.objects['RIG-Reinforce']
    md=ob.modifiers.new('Armature','ARMATURE'); md.object=rig
    ob.parent=rig; ob.matrix_parent_inverse=rig.matrix_world.inverted()

def shoe(side,sx):
    cx=sx*0.075
    # low ankle shoe with pointed toe and heel
    prof=[(0.000,0.044,0.112,-0.055),(0.020,0.046,0.115,-0.058),(0.050,0.043,0.104,-0.050),
          (0.080,0.039,0.086,-0.040),(0.110,0.037,0.066,-0.020),(0.140,0.043,0.057,0.000),
          (0.165,0.049,0.059,0.000),(0.195,0.051,0.060,0.000)]
    rings=[lib.ring(z,rx,ry,32,cx=cx,cy=cy) for (z,rx,ry,cy) in prof]
    body=lib.loft('GEO-Shoe_'+side, rings, 'COL_Legs', boot, cap_start=True, cap_end=False)
    lib.solidify(body,0.0025,0.0)
    # pointed toe cone
    tip=[(cx,-0.105,0.050),(cx,-0.150,0.040),(cx,-0.182,0.032)]
    tr=lib.tube('GEO-Shoe_Toe_'+side, tip, [0.031,0.017,0.0030], 'COL_Legs', boot, n=12, caps=True)
    # ankle cuff
    crings=[lib.ring(z,0.055,0.058,32,cx=cx) for z in (0.150,0.165,0.180,0.195)]
    cuff=lib.loft('GEO-Shoe_Cuff_'+side, crings, 'COL_Legs', boot, cap_start=False, cap_end=False)
    lib.solidify(cuff,0.0022,0.0)
    # gold band on cuff
    grings=[lib.ring(z,0.058,0.061,32,cx=cx) for z in (0.160,0.170)]
    gb=lib.loft('GEO-Shoe_CuffGold_'+side, grings, 'COL_Legs', gold, cap_start=False, cap_end=False)
    lib.solidify(gb,0.0015,0.0)
    # heel block (high heel)
    vs=[(cx-0.018,0.055,0.070),(cx+0.018,0.055,0.070),(cx+0.018,0.090,0.070),(cx-0.018,0.090,0.070),
        (cx-0.008,0.070,0.000),(cx+0.008,0.070,0.000),(cx+0.008,0.090,0.000),(cx-0.008,0.090,0.000)]
    fs=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    lib.new_obj('GEO-Shoe_Heel_'+side, vs, fs, 'COL_Legs', boot, smooth=False)
    # gold toe diamond
    me=bpy.data.meshes.new('GEO-Shoe_ToeGold_'+side)
    bm=bmesh.new()
    mtx=Matrix.Translation((cx,-0.118,0.100)) @ Matrix.Diagonal((0.016,0.010,0.020,1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0, matrix=mtx)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new('GEO-Shoe_ToeGold_'+side, me); bpy.data.collections['COL_Legs'].objects.link(ob)
    me.materials.append(gold)
    for p in me.polygons: p.use_smooth=True
    return body

for side,sx in (('L',1),('R',-1)):
    shoe(side,sx)

# long stocking on character's RIGHT (x negative = R object), short sock on LEFT (+X)
pts=[]; rs=[]
for z,r in [(0.080,0.045),(0.120,0.050),(0.200,0.060),(0.300,0.073),(0.400,0.066),(0.448,0.064),(0.520,0.083),(0.580,0.092),(0.640,0.097)]:
    pts.append((leg_x(z,-1),0.004,z)); rs.append(r)
st=lib.tube('GEO-Stocking_Long_R', pts, rs, 'COL_Legs', stock, n=20, caps=False)
lib.solidify(st,0.0015,0.0)
# short sock on LEFT
pts=[]; rs=[]
for z,r in [(0.100,0.066),(0.140,0.070),(0.180,0.074),(0.220,0.078),(0.260,0.081),(0.300,0.082)]:
    pts.append((leg_x(z,1),0.004,z)); rs.append(r)
sk=lib.tube('GEO-Sock_Short_L', pts, rs, 'COL_Legs', stock, n=20, caps=False)
lib.solidify(sk,0.0015,0.0)

# weights
rig=bpy.data.objects['RIG-Reinforce']
def clear(ob):
    for vg in list(ob.vertex_groups): ob.vertex_groups.remove(vg)
for side,sx in (('L',1),('R',-1)):
    for nm in ['GEO-Shoe_'+side,'GEO-Shoe_Cuff_'+side,'GEO-Shoe_CuffGold_'+side,'GEO-Shoe_Heel_'+side,'GEO-Shoe_Toe_'+side,'GEO-Shoe_ToeGold_'+side]:
        ob=bpy.data.objects.get(nm)
        if not ob: continue
        clear(ob); one(ob,'foot_'+side); add_mod(ob)
# long stocking R: foot/shin/thigh by z
clear(st)
gfoot=st.vertex_groups.new(name='foot_R'); gshin=st.vertex_groups.new(name='shin_R'); gthigh=st.vertex_groups.new(name='thigh_R')
for v in st.data.vertices:
    z=v.co.z
    if z<0.12:
        gfoot.add([v.index],1.0,'REPLACE')
    elif z<0.42:
        gshin.add([v.index],1.0,'REPLACE')
    elif z<0.50:
        f=(z-0.42)/0.08; gshin.add([v.index],1.0-f,'REPLACE'); gthigh.add([v.index],f,'REPLACE')
    else:
        gthigh.add([v.index],1.0,'REPLACE')
add_mod(st)
# short sock L
clear(sk)
gf=sk.vertex_groups.new(name='foot_L'); gs=sk.vertex_groups.new(name='shin_L')
for v in sk.data.vertices:
    z=v.co.z
    if z<0.12: gf.add([v.index],1.0,'REPLACE')
    else: gs.add([v.index],1.0,'REPLACE')
add_mod(sk)

print('LEGWEAR_OK')
for ob in bpy.data.objects:
    if ob.type=='MESH' and ob.name.startswith(('GEO-Shoe','GEO-Sock','GEO-Stocking')):
        zs=[v.co.z for v in ob.data.vertices]
        print(ob.name, len(ob.data.vertices), 'z[%.3f,%.3f]'%(min(zs),max(zs)))
bpy.ops.wm.save_as_mainfile(filepath=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/Reinforce_Eins_TV.blend")
