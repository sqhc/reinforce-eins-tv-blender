# -*- coding: utf-8 -*-
import bpy, math
rig=bpy.data.objects['RIG-Reinforce']
sc=bpy.context.scene
sc.render.fps=24
bpy.context.view_layer.objects.active=rig
rig.select_set(True)
bpy.ops.object.mode_set(mode='POSE')
for pb in rig.pose.bones:
    pb.rotation_mode='XYZ'; pb.rotation_euler=(0,0,0); pb.location=(0,0,0); pb.scale=(1,1,1)
if rig.animation_data:
    rig.animation_data_clear()
for _a in list(bpy.data.actions):
    bpy.data.actions.remove(_a)
rig.animation_data_create()

def key(name, frame, rot=None, loc=None):
    pb=rig.pose.bones.get(name)
    if not pb: return
    pb.rotation_mode='XYZ'
    if rot is not None:
        pb.rotation_euler=(math.radians(rot[0]),math.radians(rot[1]),math.radians(rot[2]))
        pb.keyframe_insert(data_path='rotation_euler', frame=frame)
    if loc is not None:
        pb.location=loc
        pb.keyframe_insert(data_path='location', frame=frame)

def make_idle():
    act=bpy.data.actions.new('Idle')
    rig.animation_data.action=act
    for f,(s,c,h) in [(1,(0,0,0)),(18,(1.2,0.6,0.8)),(36,(0,0,0)),(54,(-1.0,-0.5,-0.8)),(72,(0,0,0))]:
        key('spine_02',f,(s,0,0)); key('chest',f,(c,0,0)); key('head',f,(0,0,h))
        key('upperarm_L',f,(0,0,-0.8)); key('upperarm_R',f,(0,0,0.8))
        key('wing_up_L_01',f,(3+2*s,0,0)); key('wing_up_R_01',f,(3+2*s,0,0))
        key('wing_low_L_01',f,(-1+1*s,0,0)); key('wing_low_R_01',f,(-1+1*s,0,0))
        key('hair_back_01',f,(1+0.6*s,0,0)); key('hair_back_02',f,(1.5+0.8*s,0,0))
        key('coat_back_L_01',f,(1+0.4*s,0,0)); key('coat_back_R_01',f,(1+0.4*s,0,0))
    act.use_fake_user=True
    return act

def make_flap():
    act=bpy.data.actions.new('WingFlap')
    rig.animation_data.action=act
    keys=[(1,0,0),(8,-28,12),(15,8,-4),(22,-30,14),(31,0,0)]
    for f,a,b in keys:
        key('wing_up_L_01',f,(a,0,0)); key('wing_up_R_01',f,(a,0,0))
        key('wing_up_L_02',f,(b,0,0)); key('wing_up_R_02',f,(b,0,0))
        key('wing_low_L_01',f,(-a*0.35,0,0)); key('wing_low_R_01',f,(-a*0.35,0,0))
        key('wing_low_L_02',f,(-b*0.3,0,0)); key('wing_low_R_02',f,(-b*0.3,0,0))
        key('pelvis',f,None,(0,0,0.006*math.sin(f/31*math.pi)))
        key('spine_02',f,(1.0,0,0)); key('head',f,(0,0,1.5*math.sin(f/31*math.pi)))
        key('hair_back_01',f,(2.0+1.5*math.sin(f/31*math.pi),0,0))
        key('coat_back_L_01',f,(1.5,0,0)); key('coat_back_R_01',f,(1.5,0,0))
    act.use_fake_user=True
    return act

idle=make_idle(); flap=make_flap()
# NLA tracks
for act in (idle, flap):
    tr=rig.animation_data.nla_tracks.new(); tr.name=act.name
    st=tr.strips.new(act.name, 1, act); st.name=act.name
for tr in rig.animation_data.nla_tracks:
    tr.mute = (tr.name != 'Idle')
rig.animation_data.action=idle
sc.frame_start=1; sc.frame_end=72; sc.frame_set(18)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
print('ANIM_OK', [a.name for a in bpy.data.actions])
