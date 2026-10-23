# -*- coding: utf-8 -*-
import bpy, math
from mathutils import Vector
sc = bpy.context.scene
# remove old render helpers
for nm in ['CAM_Front','CAM_ThreeQ','LGT_Key','LGT_Fill','LGT_Rim']:
    ob = bpy.data.objects.get(nm)
    if ob: bpy.data.objects.remove(ob, do_unlink=True)
col = bpy.data.collections['COL_Render']

def camera(name, loc, target, lens=60):
    cd = bpy.data.cameras.new(name); cd.lens = lens
    ob = bpy.data.objects.new(name, cd); col.objects.link(ob)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
    return ob

def area(name, loc, target, energy, size=3.0, color=(1,1,1)):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.shape='SQUARE'; ld.size=size; ld.color=color
    ob = bpy.data.objects.new(name, ld); col.objects.link(ob)
    ob.location = loc
    d = Vector(target) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
    return ob

cam = camera('CAM_Front', (0,-4.8,1.05), (0,0,0.98), 62)
camera('CAM_ThreeQ', (3.4,-3.8,1.45), (0,0,0.98), 62)
area('LGT_Key', (2.4,-2.8,3.0), (0,0,1.1), 150, 2.6, (1.0,0.96,0.92))
area('LGT_Fill', (-2.8,-2.2,1.8), (0,0,1.0), 55, 2.4, (0.75,0.82,1.0))
area('LGT_Rim', (0.0,3.0,2.6), (0,0,1.2), 220, 2.2, (0.55,0.65,1.0))
area('LGT_Top', (0.0,0.0,4.0), (0,0,1.2), 35, 2.0, (1.0,0.95,0.9))
sc.camera = cam
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x = 900; sc.render.resolution_y = 1200
sc.render.resolution_percentage = 100
try: sc.eevee.taa_render_samples = 48
except Exception: pass
sc.render.image_settings.file_format='PNG'
sc.render.filepath = r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/render/wip/front_test.png"
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.render.render(write_still=True)
print('RENDER_OK', sc.render.filepath)
