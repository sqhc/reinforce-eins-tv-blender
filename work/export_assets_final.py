# -*- coding: utf-8 -*-
import bpy, os
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
rig=bpy.data.objects['RIG-Reinforce']
meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('GEO-')]
bpy.context.scene.frame_set(1)
rig.animation_data.action=bpy.data.actions['Idle']
for tr in rig.animation_data.nla_tracks: tr.mute=(tr.name!='Idle')
bpy.ops.wm.save_as_mainfile(filepath=base+'Reinforce_Eins_TV.blend')
try: bpy.ops.object.mode_set(mode='OBJECT')
except Exception: pass
bpy.context.view_layer.objects.active=rig
try: bpy.ops.object.mode_set(mode='OBJECT')
except Exception: pass
bpy.ops.object.select_all(action='DESELECT')
for o in meshes: o.select_set(True)
rig.select_set(True); bpy.context.view_layer.objects.active=rig
try:
    bpy.ops.export_scene.gltf(filepath=base+'export/Reinforce_Eins_TV.glb', export_format='GLB', use_selection=True, export_animations=True, export_skins=True, export_apply=False, export_yup=True)
    print('GLB_OK', os.path.getsize(base+'export/Reinforce_Eins_TV.glb'))
except Exception as e:
    print('GLB_ERR', repr(e))
try:
    bpy.ops.export_scene.fbx(filepath=base+'export/Reinforce_Eins_TV.fbx', use_selection=True, add_leaf_bones=False, bake_anim=True, bake_anim_use_all_actions=True, apply_scale_options='FBX_SCALE_ALL')
    print('FBX_OK', os.path.getsize(base+'export/Reinforce_Eins_TV.fbx'))
except Exception as e:
    print('FBX_ERR', repr(e))
try: bpy.ops.object.mode_set(mode='OBJECT')
except Exception: pass
bpy.ops.object.select_all(action='DESELECT')
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active=meshes[0]
try:
    bpy.ops.wm.obj_export(filepath=base+'export/Reinforce_Eins_TV.obj', export_selected_objects=True, apply_modifiers=True, export_materials=True, export_triangulated_mesh=True)
    print('OBJ_OK', os.path.getsize(base+'export/Reinforce_Eins_TV.obj'))
except Exception as e:
    print('OBJ_ERR', repr(e))
print('DONE')
