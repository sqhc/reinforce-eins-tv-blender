# -*- coding: utf-8 -*-
import bpy, math, os
from mathutils import Vector
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
rig=bpy.data.objects['RIG-Reinforce']; sc=bpy.context.scene
sc.camera=bpy.data.objects['CAM_Front']
sc.render.engine='BLENDER_EEVEE'; sc.render.resolution_x=700; sc.render.resolution_y=900; sc.render.resolution_percentage=100
os.makedirs(base+'render/rig',exist_ok=True)
bpy.context.view_layer.objects.active=rig
try:
    if bpy.context.object and bpy.context.object.mode!='POSE': bpy.ops.object.mode_set(mode='POSE')
except Exception as e: print('mode warn',e)
def zero():
    for pb in rig.pose.bones:
        pb.rotation_mode='XYZ'; pb.rotation_euler=(0,0,0); pb.location=(0,0,0)
def rot(n,x=0,y=0,z=0):
    pb=rig.pose.bones.get(n)
    if pb: pb.rotation_euler=(math.radians(x),math.radians(y),math.radians(z))
def move_world(bn,delta):
    pb=rig.pose.bones.get(bn)
    if not pb: return
    q=pb.bone.matrix_local.to_3x3(); pb.location=q.inverted() @ Vector(delta)
def ik_mute(v):
    for side in ('L','R'):
        for bn in ('shin_'+side,'forearm_'+side):
            c=rig.pose.bones[bn].constraints.get('IK_'+bn)
            if c: c.mute=bool(v)
def render(nm):
    bpy.context.view_layer.update()
    sc.render.filepath=base+'render/rig/'+nm+'.png'; bpy.ops.render.render(write_still=True); print('POSE',nm)
if rig.animation_data:
    rig.animation_data.action=None
    for tr in rig.animation_data.nla_tracks: tr.mute=True
ik_mute(True)
zero(); render('pose_1_rest')
zero(); rot('upperarm_L',0,0,-55); rot('upperarm_R',0,0,55); rot('forearm_L',-30,0,0); rot('forearm_R',-30,0,0)
rot('wing_up_L_01',25,0,0); rot('wing_up_R_01',25,0,0); rot('wing_low_L_01',-15,0,0); rot('wing_low_R_01',-15,0,0)
render('pose_2_arms')
zero(); rot('thigh_L',-35,0,0); rot('shin_L',55,0,0); rot('thigh_R',-35,0,0); rot('shin_R',55,0,0)
rot('spine_01',10,0,0); rot('wing_up_L_01',15,0,0); rot('wing_up_R_01',15,0,0)
render('pose_3_crouch')
zero(); rot('wing_up_L_01',-25,0,0); rot('wing_up_R_01',-25,0,0); rot('wing_up_L_02',10,0,0); rot('wing_up_R_02',10,0,0)
rot('wing_low_L_01',10,0,0); rot('wing_low_R_01',10,0,0); rot('spine_02',3,0,0)
render('pose_4_flap')

ik_mute(False); zero()
for side in ('L','R'):
    move_world('CTRL-hand_IK_'+side,(0,-0.14,0.04))
move_world('CTRL-foot_IK_L',(0.02,-0.08,0.0)); move_world('CTRL-foot_IK_R',(0,0.02,0.0))
rot('spine_01',-4,0,0); rot('head',4,0,0)
render('pose_5_ik')

zero()
for i in range(4):
    for k in (1,2):
        pb=rig.pose.bones.get('finger_L_%d_%02d'%(i,k))
        if pb: pb.rotation_euler=(math.radians(40),0,0)
for nm,ang in [('skirt_F',-5),('skirt_B',4),('skirt_L',-3),('skirt_R',3)]:
    pb=rig.pose.bones.get(nm)
    if pb: pb.rotation_euler=(math.radians(ang),0,0)
render('pose_6_finger_skirt')

# 7 IK crouch, feet planted, hands forward; lower wings swept back
zero()
move_world('pelvis',(0,0,-0.20))
move_world('CTRL-hand_IK_L',(0,-0.18,0.02)); move_world('CTRL-hand_IK_R',(0,-0.18,0.02))
rot('spine_01',-10,0,0); rot('spine_02',-5,0,0); rot('head',7,0,0)
rot('skirt_F',-6,0,0); rot('skirt_B',4,0,0); rot('skirt_L',-3,0,0); rot('skirt_R',3,0,0)
rot('wing_up_L_01',8,0,0); rot('wing_up_R_01',8,0,0)
rot('wing_low_L_01',55,0,0); rot('wing_low_R_01',55,0,0)
rot('coat_back_L',-3,0,0); rot('coat_back_R',-3,0,0)
render('pose_7_ik_crouch')

# 8 IK reach overhead + left leg forward
zero()
move_world('CTRL-hand_IK_L',(0.08,-0.02,0.78)); move_world('CTRL-hand_IK_R',(-0.08,-0.02,0.78))
move_world('CTRL-foot_IK_L',(0.02,-0.16,0.06))
rot('spine_01',2,0,0); rot('chest',3,0,0); rot('head',-5,0,0)
rot('skirt_F',-4,0,0); rot('skirt_B',3,0,0)
rot('wing_up_L_01',-18,0,0); rot('wing_up_R_01',-18,0,0)
rot('wing_low_L_01',6,0,0); rot('wing_low_R_01',6,0,0)
render('pose_8_ik_reach')

# restore
zero(); ik_mute(False)
if rig.animation_data:
    for tr in rig.animation_data.nla_tracks: tr.mute=(tr.name!='Idle')
    rig.animation_data.action=bpy.data.actions['Idle']
sc.frame_set(1)
try: bpy.ops.object.mode_set(mode='OBJECT')
except Exception: pass
bpy.ops.wm.save_as_mainfile(filepath=base+'Reinforce_Eins_TV.blend')
print('POSES_DONE')
