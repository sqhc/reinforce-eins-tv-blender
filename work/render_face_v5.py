# -*- coding: utf-8 -*-
import bpy, math, os
from mathutils import Vector
BASE=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
rig=bpy.data.objects['RIG-Reinforce']; sc=bpy.context.scene
os.makedirs(BASE+'render/face',exist_ok=True)
# clear action and pose
if rig.animation_data:
    rig.animation_data.action=None
    for tr in rig.animation_data.nla_tracks: tr.mute=True
for pb in rig.pose.bones:
    pb.rotation_mode='XYZ'; pb.rotation_euler=(0,0,0); pb.location=(0,0,0)
def setkeys(name,val):
    for o in bpy.data.objects:
        if o.type=='MESH' and o.data.shape_keys and name in o.data.shape_keys.key_blocks:
            o.data.shape_keys.key_blocks[name].value=float(val)
def resetkeys():
    for o in bpy.data.objects:
        if o.type=='MESH' and o.data.shape_keys:
            for kb in o.data.shape_keys.key_blocks:
                if kb.name!='Basis': kb.value=0.0
def resetpose():
    for pb in rig.pose.bones:
        pb.rotation_mode='XYZ'; pb.rotation_euler=(0,0,0); pb.location=(0,0,0)
def move_world(bn,delta):
    pb=rig.pose.bones.get(bn)
    if not pb: return
    q=pb.bone.matrix_local.to_3x3(); pb.location=q.inverted() @ Vector(delta)
def rot(n,x=0,y=0,z=0):
    pb=rig.pose.bones.get(n)
    if pb: pb.rotation_euler=(math.radians(x),math.radians(y),math.radians(z))
# camera
cd=bpy.data.cameras.get('CAM_FaceV5') or bpy.data.cameras.new('CAM_FaceV5'); cd.lens=85
cam=bpy.data.objects.get('CAM_FaceV5')
if cam is None:
    cam=bpy.data.objects.new('CAM_FaceV5',cd); bpy.data.collections['COL_Render'].objects.link(cam)
cam.data=cd; sc.camera=cam
sc.render.engine='BLENDER_EEVEE'; sc.render.resolution_x=900; sc.render.resolution_y=900; sc.render.resolution_percentage=100
try: sc.eevee.taa_render_samples=48
except Exception: pass
def place(pos,target):
    cam.location=pos; d=Vector(target)-Vector(pos); cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
def render(name,pos=(0.015,-0.78,1.555),target=(0.0,-0.02,1.55)):
    place(pos,target); bpy.context.view_layer.update()
    sc.render.filepath=BASE+'render/face/v5_'+name+'.png'; bpy.ops.render.render(write_still=True); print('FACE',name)
resetkeys(); resetpose()
render('neutral')
resetkeys(); resetpose(); setkeys('blink',1.0); render('blink')
resetkeys(); resetpose(); setkeys('wide_open',1.0); rot('jaw',10); move_world('brow_L',(0,0,0.006)); move_world('brow_R',(0,0,0.006)); rot('Pupil_L',12); rot('Pupil_R',12); render('surprise')
resetkeys(); resetpose(); setkeys('squint',1.0); move_world('brow_L',(0,0,-0.004)); move_world('brow_R',(0,0,-0.004)); render('squint')
resetkeys(); resetpose(); setkeys('smile',1.0); rot('jaw',2); move_world('brow_L',(0,0,0.002)); move_world('brow_R',(0,0,0.002)); render('smile')
resetkeys(); resetpose(); render('profile',pos=(0.42,-0.66,1.56),target=(0.0,-0.02,1.55))
# restore
resetkeys()
for pb in rig.pose.bones:
    pb.rotation_euler=(0,0,0); pb.location=(0,0,0)
if rig.animation_data:
    rig.animation_data.action=bpy.data.actions['Idle']
    for tr in rig.animation_data.nla_tracks: tr.mute=(tr.name!='Idle')
sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=BASE+'Reinforce_Eins_TV.blend')
print('FACE_RENDER_DONE')
