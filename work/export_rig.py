# -*- coding: utf-8 -*-
import bpy, os
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
os.makedirs(base+'export', exist_ok=True)
rig=bpy.data.objects['RIG-Reinforce']
meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('GEO-')]
bpy.ops.object.select_all(action='DESELECT')
for o in meshes: o.select_set(True)
rig.select_set(True)
bpy.context.view_layer.objects.active=rig
bpy.context.scene.frame_set(1)
rig.animation_data.action=bpy.data.actions['Idle']

def gltf():
    kw=dict(filepath=base+'export/Reinforce_Eins_TV.glb', export_format='GLB', use_selection=True,
            export_animations=True, export_skins=True, export_apply=False, export_yup=True)
    try:
        bpy.ops.export_scene.gltf(**kw, export_animation_mode='ACTIONS', export_force_sampling=True)
    except TypeError as e:
        print('GLTF fallback',e)
        bpy.ops.export_scene.gltf(**kw)
    print('GLB_DONE', os.path.getsize(base+'export/Reinforce_Eins_TV.glb'))
try:
    gltf()
except Exception as e:
    print('GLB_ERROR',repr(e))

def fbx():
    kw=dict(filepath=base+'export/Reinforce_Eins_TV.fbx', use_selection=True, add_leaf_bones=False,
            bake_anim=True, bake_anim_use_all_actions=True, apply_scale_options='FBX_SCALE_ALL')
    try:
        bpy.ops.export_scene.fbx(**kw)
    except TypeError as e:
        print('FBX fallback',e)
        bpy.ops.export_scene.fbx(filepath=base+'export/Reinforce_Eins_TV.fbx', use_selection=True, add_leaf_bones=False)
    print('FBX_DONE', os.path.getsize(base+'export/Reinforce_Eins_TV.fbx'))
try:
    fbx()
except Exception as e:
    print('FBX_ERROR',repr(e))

# static obj (no armature)
bpy.ops.object.select_all(action='DESELECT')
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active=meshes[0]
try:
    bpy.ops.wm.obj_export(filepath=base+'export/Reinforce_Eins_TV.obj', export_selected_objects=True,
                          apply_modifiers=True, export_materials=True, export_triangulated_mesh=True)
    print('OBJ_DONE', os.path.getsize(base+'export/Reinforce_Eins_TV.obj'))
except Exception as e:
    print('OBJ_ERROR',repr(e))
print('EXPORT_ALL_DONE')
