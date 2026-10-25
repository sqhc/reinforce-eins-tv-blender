# -*- coding: utf-8 -*-
import bpy, math
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
rig=bpy.data.objects['RIG-Reinforce']
sc=bpy.context.scene
sc.frame_set(1)
if rig.animation_data: rig.animation_data.action=bpy.data.actions['Idle']
bpy.context.view_layer.objects.active=rig
bpy.ops.object.mode_set(mode='EDIT')
eb=rig.data.edit_bones
head=eb['head']
def add(name,h,t,parent):
    if name in eb: eb.remove(eb[name])
    b=eb.new(name); b.head=h; b.tail=t; b.parent=eb[parent]; b.use_connect=False; b.use_deform=True
    return b
jaw=add('jaw',(0,0,1.500),(0,-0.025,1.452),'head')
browL=add('brow_L',(0.034,-0.064,1.578),(0.034,-0.074,1.596),'head')
browR=add('brow_R',(-0.034,-0.064,1.578),(-0.034,-0.074,1.596),'head')
bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.update()

# weights: head lower-front -> jaw
ob=bpy.data.objects['GEO-Head']
hg=ob.vertex_groups.get('head') or ob.vertex_groups.new(name='head')
jg=ob.vertex_groups.get('jaw') or ob.vertex_groups.new(name='jaw')
for v in ob.data.vertices:
    z,y=v.co.z,v.co.y
    wz=max(0.0,min(1.0,(1.520-z)/0.055))
    wy=max(0.0,min(1.0,(0.020-y)/0.030))
    wj=0.90*wz*wy
    if wj>1e-4:
        jg.add([v.index],wj,'REPLACE'); hg.add([v.index],1.0-wj,'REPLACE')
# mouth mostly jaw
m=bpy.data.objects['GEO-Mouth']
hg=m.vertex_groups.get('head') or m.vertex_groups.new(name='head')
jg=m.vertex_groups.get('jaw') or m.vertex_groups.new(name='jaw')
for v in m.data.vertices:
    jg.add([v.index],0.85,'REPLACE'); hg.add([v.index],0.15,'REPLACE')
# brows
for nm,bn in [('GEO-Brow_L','brow_L'),('GEO-Brow_R','brow_R')]:
    o=bpy.data.objects[nm]
    for g in o.vertex_groups:
        if g.name!='head': pass
    hg=o.vertex_groups.get('head') or o.vertex_groups.new(name='head')
    bg=o.vertex_groups.get(bn) or o.vertex_groups.new(name=bn)
    for v in o.data.vertices:
        bg.add([v.index],1.0,'REPLACE'); hg.add([v.index],0.0,'REPLACE')

# FaceDemo action
act=bpy.data.actions.new('FaceDemo')
rig.animation_data.action=act
pbj=rig.pose.bones['jaw']; pbl=rig.pose.bones['brow_L']; pbr=rig.pose.bones['brow_R']
for pb in (pbj,pbl,pbr): pb.rotation_mode='XYZ'
keys=[(1,0.0,0.0,0.0),(12,math.radians(9),math.radians(4),math.radians(4)),(24,0.0,0.0,0.0),(36,math.radians(5),math.radians(-2),math.radians(-2)),(48,0.0,0.0,0.0)]
for fr,jx,bx,by in keys:
    sc.frame_set(fr)
    pbj.rotation_euler=(jx,0,0); pbl.rotation_euler=(bx,0,0); pbr.rotation_euler=(by,0,0)
    for pb in (pbj,pbl,pbr): pb.keyframe_insert('rotation_euler',frame=fr)
act.use_fake_user=True
# NLA track muted
tr=rig.animation_data.nla_tracks.new(); tr.name='FaceDemo'; st=tr.strips.new('FaceDemo',1,act); tr.mute=True
rig.animation_data.action=bpy.data.actions['Idle']; sc.frame_set(1)
print('FACE_BONES',len(rig.data.bones),'GROUPS',[g.name for g in bpy.data.objects['GEO-Head'].vertex_groups])
bpy.ops.wm.save_as_mainfile(filepath=base+'Reinforce_Eins_TV.blend')
