# -*- coding: utf-8 -*-
import bpy, math, os
from mathutils import Vector
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
rig=bpy.data.objects['RIG-Reinforce']; sc=bpy.context.scene
rig.animation_data.action=bpy.data.actions['SecondaryFlow']
for tr in rig.animation_data.nla_tracks: tr.mute=True
cd=bpy.data.cameras.get('CAM_Secondary') or bpy.data.cameras.new('CAM_Secondary'); cd.lens=62
cam=bpy.data.objects.get('CAM_Secondary')
if cam is None:
    cam=bpy.data.objects.new('CAM_Secondary',cd); bpy.data.collections['COL_Render'].objects.link(cam)
cam.location=(2.4,-3.6,1.45); d=Vector((0,0,1.05))-cam.location; cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
sc.camera=cam
sc.render.engine='BLENDER_EEVEE'; sc.render.resolution_x=720; sc.render.resolution_y=900; sc.render.resolution_percentage=100
try: sc.eevee.taa_render_samples=24
except Exception: pass
outdir=base+'render/anim/secondary_frames'; os.makedirs(outdir,exist_ok=True)
frames=list(range(1,96,2))
for i,fr in enumerate(frames):
    sc.frame_set(fr)
    sc.render.filepath=outdir+'/f_%03d.png'%i
    bpy.ops.render.render(write_still=True)
    if i%10==0: print('SECFRAME',i)
rig.animation_data.action=bpy.data.actions['Idle']; sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=base+'Reinforce_Eins_TV.blend')
print('SECONDARY_FRAMES',len(frames))
