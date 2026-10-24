# -*- coding: utf-8 -*-
import bpy, math, os
from mathutils import Vector
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
rig=bpy.data.objects['RIG-Reinforce']
sc=bpy.context.scene
sc.frame_set(1)
rig.animation_data.action=bpy.data.actions['Idle']
for tr in rig.animation_data.nla_tracks: tr.mute=(tr.name!='Idle')
# floor
old=bpy.data.objects.get('RND-Ground')
if old: bpy.data.objects.remove(old, do_unlink=True)
me=bpy.data.meshes.new('RND-Ground')
me.from_pydata([(-9,-9,-0.002),(9,-9,-0.002),(9,9,-0.002),(-9,9,-0.002)],[],[(0,1,2,3)])
me.update()
gob=bpy.data.objects.new('RND-Ground',me); bpy.data.collections['COL_Render'].objects.link(gob)
fm=bpy.data.materials.get('M_Floor') or bpy.data.materials.new('M_Floor')
fm.use_nodes=True
bs=next((n for n in fm.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
if bs:
    bs.inputs['Base Color'].default_value=(0.012,0.016,0.028,1)
    bs.inputs['Roughness'].default_value=0.75
me.materials.append(fm)
# camera
cd=bpy.data.cameras.get('CAM_Turn') or bpy.data.cameras.new('CAM_Turn')
cd.lens=58
cam=bpy.data.objects.get('CAM_Turn')
if cam is None:
    cam=bpy.data.objects.new('CAM_Turn',cd); bpy.data.collections['COL_Render'].objects.link(cam)
cam.data=cd
sc.camera=cam
sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=800; sc.render.resolution_y=1200; sc.render.resolution_percentage=100
try: sc.eevee.taa_render_samples=24
except Exception: pass
outdir=base+'render/anim/frames'
os.makedirs(outdir,exist_ok=True)
R=4.9; Z=1.10; N=48
for i in range(N):
    a=2*math.pi*i/N
    loc=Vector((R*math.sin(a), -R*math.cos(a), Z))
    cam.location=loc
    d=Vector((0,0,1.0))-loc
    cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=outdir+'/frame_%03d.png'%i
    bpy.ops.render.render(write_still=True)
    print('FRAME',i)
# remove floor before save
bpy.data.objects.remove(gob, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=base+'Reinforce_Eins_TV.blend')
print('TURNTABLE_FRAMES_DONE')
