# -*- coding: utf-8 -*-
import bpy, math, sys, os
from mathutils import Vector
WORK = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import spec, lib

# remove old rig
for ob in list(bpy.data.objects):
    if ob.type == 'ARMATURE':
        bpy.data.objects.remove(ob, do_unlink=True)
for ob in bpy.data.objects:
    if ob.type == 'MESH':
        for m in list(ob.modifiers):
            if m.type == 'ARMATURE':
                ob.modifiers.remove(m)
        for vg in list(ob.vertex_groups):
            ob.vertex_groups.remove(vg)
        if ob.parent and ob.parent.type == 'ARMATURE':
            ob.parent = None

COL = bpy.data.collections['COL_Rig']
arm = bpy.data.armatures.new('RIG-Reinforce')
rig = bpy.data.objects.new('RIG-Reinforce', arm)
COL.objects.link(rig)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='EDIT')
E = arm.edit_bones

def eb(name, head, tail, parent=None, connect=False):
    b = E.new(name)
    b.head = Vector(head); b.tail = Vector(tail)
    if parent is not None:
        b.parent = parent
        b.use_connect = bool(connect)
    return b

root = eb('root', (0,0,0.0), (0,0,0.10))
pelvis = eb('pelvis', (0,0,0.84), (0,0,0.92), root)
sp1 = eb('spine_01', (0,0,0.92), (0,0,1.04), pelvis, True)
sp2 = eb('spine_02', (0,0,1.04), (0,0,1.18), sp1, True)
chest = eb('chest', (0,0,1.18), (0,0,1.32), sp2, True)
neck = eb('neck', (0,0,1.32), (0,0,1.44), chest, True)
head = eb('head', (0,0,1.44), (0,0,1.68), neck, True)

arm_bones = {}
for side, sx in (('L',1),('R',-1)):
    cl = eb('clavicle_'+side, (sx*0.02,0,1.315), (sx*0.165,0,1.344), chest)
    ua = eb('upperarm_'+side, (sx*0.165,0,1.344), (sx*0.335,0,1.110), cl, True)
    fa = eb('forearm_'+side, (sx*0.335,0,1.110), (sx*0.475,0,0.905), ua, True)
    hd = eb('hand_'+side, (sx*0.475,0,0.905), (sx*0.525,-0.005,0.815), fa, True)
    th = eb('thigh_'+side, (sx*0.090,0,0.870), (sx*0.085,0.005,0.448), pelvis)
    sh = eb('shin_'+side, (sx*0.085,0.005,0.448), (sx*0.075,0,0.060), th, True)
    ft = eb('foot_'+side, (sx*0.075,0,0.060), (sx*0.075,-0.140,0.020), sh, True)
    arm_bones[side] = (cl,ua,fa,hd,th,sh,ft)

# wings: 3-bone chains along the wing top edge
for side, sx in (('L',1),('R',-1)):
    for tag, root0, tip0 in (
        ('wing_up_'+side, (sx*0.070,0.090,1.290), (sx*0.560,0.215,2.120)),
        ('wing_low_'+side, (sx*0.080,0.090,1.180), (sx*0.420,0.160,0.330)),
    ):
        r0 = Vector(root0); t0 = Vector(tip0)
        p1 = r0 + (t0-r0)*0.38
        p2 = r0 + (t0-r0)*0.72
        b1 = eb(tag+'_01', r0, p1, chest)
        b2 = eb(tag+'_02', p1, p2, b1, True)
        b3 = eb(tag+'_03', p2, t0, b2, True)

# hair
hb = {}
for i,(a,b) in enumerate([((0,0.075,1.62),(0,0.105,1.38)),((0,0.105,1.38),(0,0.120,1.14)),((0,0.120,1.14),(0,0.115,0.95))]):
    hb['back_%d'%(i+1)] = eb('hair_back_%02d'%(i+1), a, b, head if i==0 else hb['back_%d'%i], i>0)
for side,sx in (('L',1),('R',-1)):
    a=(sx*0.090,0.000,1.60); b=(sx*0.115,-0.010,1.36); c=(sx*0.135,-0.020,1.12)
    b1=eb('hair_side_'+side+'_01', a, b, head)
    b2=eb('hair_side_'+side+'_02', b, c, b1, True)

# coat
for side,sx in (('L',1),('R',-1)):
    for tag, a, b, c in (
        ('coat_back_'+side, (sx*0.050,0.105,1.00), (sx*0.120,0.145,0.60), (sx*0.180,0.180,0.20)),
        ('coat_side_'+side, (sx*0.130,0.035,1.00), (sx*0.180,0.060,0.60), (sx*0.240,0.080,0.20)),
    ):
        b1=eb(tag+'_01', a, b, pelvis)
        b2=eb(tag+'_02', b, c, b1, True)

bpy.ops.object.mode_set(mode='OBJECT')
rig.show_in_front = True
print('BONES', len(arm.bones))

# ---------------- weights ----------------
def VG(ob, name):
    vg = ob.vertex_groups.get(name)
    if vg is None: vg = ob.vertex_groups.new(name=name)
    return vg

def assign_z(ob, centers, extra=None):
    # centers: list of (z, bone) sorted ascending; linear blend between nearest two
    cs = sorted(centers, key=lambda x: x[0])
    groups = {b: VG(ob,b) for (_,b) in cs}
    for v in ob.data.vertices:
        z = v.co.z
        if z <= cs[0][0]:
            w = {cs[0][1]:1.0}
        elif z >= cs[-1][0]:
            w = {cs[-1][1]:1.0}
        else:
            w = {}
            for i in range(len(cs)-1):
                z0,b0 = cs[i]; z1,b1 = cs[i+1]
                if z0 <= z <= z1:
                    f = (z-z0)/max(1e-9,z1-z0)
                    w[b0] = 1.0-f; w[b1] = f
                    break
        for b,ww in w.items():
            if ww > 1e-4: groups[b].add([v.index], ww, 'REPLACE')
    if extra:
        for b,ww in extra.items():
            groups[b] = VG(ob,b)
            for v in ob.data.vertices:
                groups[b].add([v.index], ww, 'REPLACE')

def dist_seg(p, a, b):
    ab = b-a; t = max(0.0, min(1.0, (p-a).dot(ab)/max(1e-12,ab.length_squared)))
    return (p-(a+ab*t)).length, t

def assign_arm(ob, side):
    sh=Vector((0.165 if side=='L' else -0.165,0,1.344))
    el=Vector((0.335 if side=='L' else -0.335,0,1.110))
    wr=Vector((0.475 if side=='L' else -0.475,0,0.905))
    hd=Vector((0.525 if side=='L' else -0.525,-0.005,0.815))
    bu=VG(ob,'upperarm_'+side); bf=VG(ob,'forearm_'+side); bh=VG(ob,'hand_'+side)
    for v in ob.data.vertices:
        p=v.co
        d1,_=dist_seg(p,sh,el); d2,_=dist_seg(p,el,wr); d3,_=dist_seg(p,wr,hd)
        w1=math.exp(-(d1/0.070)**2); w2=math.exp(-(d2/0.060)**2); w3=math.exp(-(d3/0.045)**2)
        s=w1+w2+w3
        if s<1e-9: w1,w2,w3,s=1,0,0,1
        bu.add([v.index], w1/s, 'REPLACE')
        bf.add([v.index], w2/s, 'REPLACE')
        bh.add([v.index], w3/s, 'REPLACE')

def assign_leg(ob, side, sx):
    hip=Vector((sx*0.090,0,0.870)); knee=Vector((sx*0.085,0.005,0.448)); ank=Vector((sx*0.075,0,0.060))
    bt=VG(ob,'thigh_'+side); bs=VG(ob,'shin_'+side); bf=VG(ob,'foot_'+side)
    for v in ob.data.vertices:
        p=v.co
        d1,_=dist_seg(p,hip,knee); d2,_=dist_seg(p,knee,ank)
        w1=math.exp(-(d1/0.080)**2); w2=math.exp(-(d2/0.065)**2)
        wf=1.0 if p.z < 0.12 else 0.0
        s=w1+w2+wf
        bt.add([v.index], w1/s, 'REPLACE'); bs.add([v.index], w2/s, 'REPLACE'); bf.add([v.index], wf/s, 'REPLACE')

def one(ob, bone):
    vg=VG(ob,bone)
    idx=[v.index for v in ob.data.vertices]
    if idx: vg.add(idx,1.0,'REPLACE')

def wing_weights(ob, side, up=True):
    root=Vector((0.070 if side=='L' else -0.070,0.09,1.290)) if up else Vector((0.080 if side=='L' else -0.080,0.09,1.180))
    if up:
        tip=Vector((0.560 if side=='L' else -0.560,0.215,2.120)); names=['wing_up_'+side+'_01','wing_up_'+side+'_02','wing_up_'+side+'_03']
    else:
        tip=Vector((0.420 if side=='L' else -0.420,0.160,0.330)); names=['wing_low_'+side+'_01','wing_low_'+side+'_02','wing_low_'+side+'_03']
    L=(tip-root).length
    groups=[VG(ob,n) for n in names]
    for v in ob.data.vertices:
        t=max(0.0,min(1.0,(v.co-root).length/max(1e-9,L)))
        # three-bone triangular weights
        w=[max(0.0,1.0-abs(t-0.2)/0.45), max(0.0,1.0-abs(t-0.55)/0.40), max(0.0,1.0-abs(t-0.9)/0.40)]
        s=sum(w)
        if s<1e-9: w=[1,0,0]; s=1
        for g,ww in zip(groups,w):
            g.add([v.index], ww/s, 'REPLACE')

meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('GEO-')]
for ob in meshes:
    n=ob.name
    if n=='GEO-Body':
        assign_z(ob, [(0.84,'pelvis'),(0.98,'spine_01'),(1.12,'spine_02'),(1.26,'chest'),(1.40,'neck')])
    elif n.startswith('GEO-Arm'):
        assign_arm(ob, n[-1])
    elif n.startswith('GEO-Leg'):
        assign_leg(ob, n[-1], 1 if n[-1]=='L' else -1)
    elif n.startswith(('GEO-Head','GEO-Eye','GEO-Brow','GEO-Mouth','GEO-Nose','GEO-Hair_Cap','GEO-Hair_Bang','GEO-Hair_Front','GEO-Hair_Feather')):
        one(ob,'head')
    elif n.startswith('GEO-Hair_Back'):
        assign_z(ob, [(0.95,'hair_back_03'),(1.14,'hair_back_02'),(1.38,'hair_back_01'),(1.55,'head')])
    elif n.startswith('GEO-Hair_Side_L'):
        assign_z(ob, [(1.12,'hair_side_L_02'),(1.36,'hair_side_L_01'),(1.55,'head')])
    elif n.startswith('GEO-Hair_Side_R'):
        assign_z(ob, [(1.12,'hair_side_R_02'),(1.36,'hair_side_R_01'),(1.55,'head')])
    elif n.startswith(('GEO-Dress_Bodice','GEO-Dress_Collar','GEO-Dress_PipingCollar','GEO-Dress_TrimX')):
        assign_z(ob, [(0.99,'pelvis'),(1.06,'spine_01'),(1.18,'spine_02'),(1.30,'chest'),(1.40,'neck')])
    elif n.startswith(('GEO-Dress_Sleeve','GEO-Dress_PipingSleeve')):
        one(ob,'upperarm_'+('L' if n.endswith('L') else 'R'))
    elif n.startswith('GEO-Dress_Skirt'):
        one(ob,'pelvis')
    elif n.startswith('GEO-Belt'):
        one(ob,'pelvis')
    elif n.startswith('GEO-Coat_Back_L'):
        assign_z(ob, [(0.20,'coat_back_L_02'),(0.60,'coat_back_L_01'),(1.00,'pelvis')])
    elif n.startswith('GEO-Coat_Back_R'):
        assign_z(ob, [(0.20,'coat_back_R_02'),(0.60,'coat_back_R_01'),(1.00,'pelvis')])
    elif n.startswith('GEO-Coat_Side_L'):
        assign_z(ob, [(0.20,'coat_side_L_02'),(0.60,'coat_side_L_01'),(1.00,'pelvis')])
    elif n.startswith('GEO-Coat_Side_R'):
        assign_z(ob, [(0.20,'coat_side_R_02'),(0.60,'coat_side_R_01'),(1.00,'pelvis')])
    elif n.startswith('GEO-Stocking_L'):
        assign_z(ob, [(0.30,'foot_L'),(0.42,'shin_L'),(0.52,'shin_L'),(0.64,'thigh_L')])
    elif n.startswith('GEO-Stocking_R'):
        assign_z(ob, [(0.30,'foot_R'),(0.42,'shin_R'),(0.52,'shin_R'),(0.64,'thigh_R')])
    elif n.startswith('GEO-Boot'):
        side='L' if ('_L' in n or n.endswith('L')) else 'R'
        assign_z(ob, [(0.0,'foot_'+side),(0.12,'foot_'+side),(0.20,'shin_'+side),(0.36,'shin_'+side)])
    elif n.startswith('GEO-Glove'):
        one(ob,'forearm_'+('L' if n.endswith('L') else 'R'))
    elif n.startswith(('GEO-Hand','GEO-Finger','GEO-Thumb')):
        side='L' if ('_L' in n or n.endswith('L')) else 'R'
        one(ob,'hand_'+side)
    elif n.startswith('GEO-Wing_Upper_L'):
        wing_weights(ob,'L',True)
    elif n.startswith('GEO-Wing_Upper_R'):
        wing_weights(ob,'R',True)
    elif n.startswith('GEO-Wing_Lower_L'):
        wing_weights(ob,'L',False)
    elif n.startswith('GEO-Wing_Lower_R'):
        wing_weights(ob,'R',False)
    else:
        assign_z(ob, [(0.84,'pelvis'),(1.2,'spine_02')])
    # modifier + parent
    md=ob.modifiers.new('Armature','ARMATURE'); md.object=rig
    ob.parent=rig
    ob.matrix_parent_inverse=rig.matrix_world.inverted()

# validation
bad=[]
for ob in meshes:
    tot=0; unw=0
    for v in ob.data.vertices:
        s=sum(g.weight for g in v.groups)
        if s < 1e-4: unw+=1
        tot+=1
    if unw: bad.append((ob.name, unw, tot))
print('UNWEIGHTED', bad[:10], 'count', len(bad))
print('RIG_OK bones=%d meshes=%d' % (len(arm.bones), len(meshes)))
