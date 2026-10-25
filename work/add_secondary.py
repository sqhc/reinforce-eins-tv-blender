# -*- coding: utf-8 -*-
import bpy, math
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
rig=bpy.data.objects['RIG-Reinforce']; sc=bpy.context.scene
sc.frame_set(1); rig.animation_data.action=bpy.data.actions['Idle']
# remove old action/track if re-run
old=bpy.data.actions.get('SecondaryFlow')
if old:
    for tr in list(rig.animation_data.nla_tracks):
        if tr.name=='SecondaryFlow': rig.animation_data.nla_tracks.remove(tr)
    bpy.data.actions.remove(old)
act=bpy.data.actions.new('SecondaryFlow'); rig.animation_data.action=act
chains={
 'hair_back':['hair_back_01','hair_back_02','hair_back_03'],
 'hair_side_L':['hair_side_L_01','hair_side_L_02'],
 'hair_side_R':['hair_side_R_01','hair_side_R_02'],
 'coat_back_L':['coat_back_L_01','coat_back_L_02'],
 'coat_back_R':['coat_back_R_01','coat_back_R_02'],
 'coat_side_L':['coat_side_L_01','coat_side_L_02'],
 'coat_side_R':['coat_side_R_01','coat_side_R_02'],
 'skirt':['skirt_F','skirt_B','skirt_L','skirt_R'],
}
# init state
state={}
for ci,(name,bs) in enumerate(chains.items()):
    for bi,bn in enumerate(bs):
        state[bn]=[0.0,0.0]  # angle, vel
        pb=rig.pose.bones[bn]; pb.rotation_mode='XYZ'
N=96; dt=1/24.0
for fr in range(1,N+1):
    t=(fr-1)*dt
    for ci,(name,bs) in enumerate(chains.items()):
        base_phase=ci*0.63
        for bi,bn in enumerate(bs):
            angle,vel=state[bn]
            # wind gust + root-driven sway, stronger at tips
            force=(0.55+0.15*bi)*math.sin(2*math.pi*0.33*t+base_phase+0.7*bi)
            force+=0.25*math.sin(2*math.pi*0.87*t+base_phase*1.7)
            k=22.0+4.0*bi; c=3.2+0.4*bi
            acc=k*(0.0-angle)-c*vel+force
            vel+=acc*dt; angle+=vel*dt
            angle=max(-0.28,min(0.28,angle))
            state[bn]=[angle,vel]
            pb=rig.pose.bones[bn]
            pb.rotation_euler=(angle,0.0,angle*0.35)
            pb.keyframe_insert('rotation_euler',frame=fr)
act.use_fake_user=True
tr=rig.animation_data.nla_tracks.new(); tr.name='SecondaryFlow'; st=tr.strips.new('SecondaryFlow',1,act); tr.mute=True
rig.animation_data.action=bpy.data.actions['Idle']; sc.frame_set(1)
print('SECONDARY_BONES',sum(len(v) for v in chains.values()),'FRAMES',N)
bpy.ops.wm.save_as_mainfile(filepath=base+'Reinforce_Eins_TV.blend')
