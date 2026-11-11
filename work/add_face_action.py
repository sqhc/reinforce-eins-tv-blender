# -*- coding: utf-8 -*-
import bpy, math
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
rig=bpy.data.objects['RIG-Reinforce']; sc=bpy.context.scene
if rig.animation_data is None: rig.animation_data_create()
if 'FaceDemoV5' in bpy.data.actions:
    bpy.data.actions.remove(bpy.data.actions['FaceDemoV5'])
    for tr in list(rig.animation_data.nla_tracks):
        if tr.name=='FaceDemoV5': rig.animation_data.nla_tracks.remove(tr)
act=bpy.data.actions.new('FaceDemoV5'); rig.animation_data.action=act
for pb in rig.pose.bones:
    pb.rotation_mode='XYZ'; pb.rotation_euler=(0,0,0); pb.location=(0,0,0)
bones=['jaw','brow_L','brow_R','Pupil_L','Pupil_R','Lid_Up_L','Lid_Up_R','Lid_Dn_L','Lid_Dn_R']
keys=[(1,0,0,0,0),(18,10,0.006,12,0),(26,-2,-0.004,0,2),(34,3,0.002,0,0),(42,0,0,0,0)]
for fr,jaw,brow,pupil,lid in keys:
    sc.frame_set(fr)
    for bn in bones:
        pb=rig.pose.bones[bn]; pb.rotation_euler=(0,0,0); pb.location=(0,0,0)
    rig.pose.bones['jaw'].rotation_euler=(math.radians(jaw),0,0)
    for bn in ('brow_L','brow_R'):
        pb=rig.pose.bones[bn]
        pb.rotation_euler=(math.radians(3 if fr==18 else (-2 if fr==26 else 0)),0,0)
        # world-ish upward shift in bone local
        q=pb.bone.matrix_local.to_3x3(); pb.location=q.inverted() @ __import__('mathutils').Vector((0,0,brow))
    for bn in ('Pupil_L','Pupil_R'):
        rig.pose.bones[bn].rotation_euler=(math.radians(pupil),0,0)
    for bn in ('Lid_Up_L','Lid_Up_R','Lid_Dn_L','Lid_Dn_R'):
        rig.pose.bones[bn].rotation_euler=(math.radians(lid),0,0)
    for bn in bones:
        rig.pose.bones[bn].keyframe_insert('rotation_euler',frame=fr)
        rig.pose.bones[bn].keyframe_insert('location',frame=fr)
act.use_fake_user=True
tr=rig.animation_data.nla_tracks.new(); tr.name='FaceDemoV5'; st=tr.strips.new('FaceDemoV5',1,act); tr.mute=True
# reset
for pb in rig.pose.bones:
    pb.rotation_euler=(0,0,0); pb.location=(0,0,0)
rig.animation_data.action=bpy.data.actions['Idle']
for tr in rig.animation_data.nla_tracks: tr.mute=(tr.name!='Idle')
sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=base+'Reinforce_Eins_TV.blend')
print('FACE_ACTION', [a.name for a in bpy.data.actions])
