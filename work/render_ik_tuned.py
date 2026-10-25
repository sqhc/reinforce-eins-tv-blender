# -*- coding: utf-8 -*-
import bpy, math, os
from mathutils import Vector
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
rig=bpy.data.objects['RIG-Reinforce']; sc=bpy.context.scene
sc.camera=bpy.data.objects['CAM_Front']
sc.render.engine='BLENDER_EEVEE'; sc.render.resolution_x=700; sc.render.resolution_y=900; sc.render.resolution_percentage=100
bpy.context.view_layer.objects.active=rig
try: bpy.ops.object.mode_set(mode='POSE')
except Exception: pass
def zero():
    for pb in rig.pose.bones:
        pb.rotation_mode='XYZ'; pb.rotation_euler=(0,0,0); pb.location=(0,0,0)
def rot(n,x=0,y=0,z=0):
    pb=rig.pose.bones.get(n)
    if pb: pb.rotation_euler=(math.radians(x),math.radians(y),math.radians(z))
def move_world(bn,delta):
    pb=rig.pose.bones.get(bn)
    if not pb: return
    q=pb.bone.matrix_local.to_3x3()
    pb.location=q.inverted() @ Vector(delta)
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
ik_mute(False)

# 7: IK crouch, feet planted, hands forward
zero()
move_world('pelvis',(0,0,-0.16))
move_world('CTRL-hand_IK_L',(0,-0.16,0.06)); move_world('CTRL-hand_IK_R',(0,-0.16,0.06))
rot('spine_01',-8,0,0); rot('spine_02',-6,0,0); rot('chest',-4,0,0); rot('head',8,0,0)
rot('skirt_F',-22,0,0); rot('skirt_B',14,0,0); rot('skirt_L',-10,0,0); rot('skirt_R',10,0,0)
rot('coat_back_L',-8,0,0); rot('coat_back_R',-8,0,0)
rot('wing_up_L_01',12,0,0); rot('wing_up_R_01',12,0,0); rot('wing_low_L_01',-8,0,0); rot('wing_low_R_01',-8,0,0)
render('pose_7_ik_crouch')

# 8: IK overhead reach + one leg forward
zero()
move_world('CTRL-hand_IK_L',(0.06,-0.02,0.52)); move_world('CTRL-hand_IK_R',(-0.06,-0.02,0.52))
move_world('CTRL-foot_IK_L',(0.02,-0.18,0.10))
rot('spine_01',4,0,0); rot('chest',4,0,0); rot('head',-6,0,0)
rot('skirt_F',-12,0,0); rot('skirt_B',8,0,0); rot('skirt_L',-8,0,0); rot('skirt_R',8,0,0)
rot('wing_up_L_01',-22,0,0); rot('wing_up_R_01',-22,0,0); rot('wing_up_L_02',8,0,0); rot('wing_up_R_02',8,0,0)
rot('wing_low_L_01',8,0,0); rot('wing_low_R_01',8,0,0)
render('pose_8_ik_reach')

# restore
zero(); ik_mute(False)
if rig.animation_data:
    rig.animation_data.action=bpy.data.actions['Idle']
    for tr in rig.animation_data.nla_tracks: tr.mute=(tr.name!='Idle')
sc.frame_set(1)
try: bpy.ops.object.mode_set(mode='OBJECT')
except Exception: pass
bpy.ops.wm.save_as_mainfile(filepath=base+'Reinforce_Eins_TV.blend')
print('IK_TUNED_DONE')
