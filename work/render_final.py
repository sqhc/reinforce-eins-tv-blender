# -*- coding: utf-8 -*-
import bpy, math
from mathutils import Vector
sc=bpy.context.scene
rig=bpy.data.objects['RIG-Reinforce']
rig.animation_data.action=bpy.data.actions['Idle']
sc.frame_set(1)

# hair silver tweak
_hm=bpy.data.materials.get('M_Hair')
if _hm:
    _b=next((n for n in _hm.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    if _b:
        _b.inputs['Base Color'].default_value=(0.46,0.50,0.57,1.0)
        _b.inputs['Roughness'].default_value=0.50
        if 'Specular IOR Level' in _b.inputs: _b.inputs['Specular IOR Level'].default_value=0.12
# eye material tweak (flat TV look, no specular blowout)
for _mn,_sp,_rg in [('M_EyeWhite',0.08,0.60),('M_Iris',0.05,0.60),('M_Pupil',0.05,0.70),('M_Lash',0.05,0.55)]:
    _m=bpy.data.materials.get(_mn)
    if _m:
        _b=next((n for n in _m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
        if _b:
            if 'Specular IOR Level' in _b.inputs: _b.inputs['Specular IOR Level'].default_value=_sp
            _b.inputs['Roughness'].default_value=_rg
# floor (render only)
old=bpy.data.objects.get('RND-Ground')
if old: bpy.data.objects.remove(old, do_unlink=True)
me=bpy.data.meshes.new('RND-Ground')
me.from_pydata([(-8,-8,-0.002),(8,-8,-0.002),(8,8,-0.002),(-8,8,-0.002)],[],[(0,1,2,3)])
me.update()
gob=bpy.data.objects.new('RND-Ground',me); bpy.data.collections['COL_Render'].objects.link(gob)
fm=bpy.data.materials.get('M_Floor') or bpy.data.materials.new('M_Floor')
fm.use_nodes=True
bs=fm.node_tree.nodes.get('Principled BSDF')
if bs is None:
    bs=next((n for n in fm.node_tree.nodes if n.type=='BSDF_PRINCIPLED'), None)
if bs is None:
    raise RuntimeError('no principled bsdf in floor material')
bs.inputs['Base Color'].default_value=(0.012,0.016,0.028,1)
bs.inputs['Roughness'].default_value=0.75
me.materials.append(fm)

# lights (soften)
for nm,en in [('LGT_Key',200.0),('LGT_Fill',60.0),('LGT_Rim',80.0),('LGT_Top',25.0),('LGT_Face',35.0)]:
    ob=bpy.data.objects.get(nm)
    if ob: ob.data.energy=en

col=bpy.data.collections['COL_Render']
def camera(name, loc, target, lens=62):
    ob=bpy.data.objects.get(name)
    if ob is None:
        cd=bpy.data.cameras.new(name); ob=bpy.data.objects.new(name,cd); col.objects.link(ob)
    ob.data.lens=lens
    ob.location=loc
    d=Vector(target)-Vector(loc); ob.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    return ob
camera('CAM_Front',(0,-4.8,1.02),(0,0,0.98),62)
camera('CAM_ThreeQ',(3.4,-3.8,1.45),(0,0,0.98),62)
camera('CAM_Side',(4.8,0,1.02),(0,0,0.98),62)
camera('CAM_Back',(0,4.8,1.02),(0,0,0.98),62)
camera('CAM_Hero',(2.6,-3.2,0.95),(0,0,1.15),52)
camera('CAM_Portrait',(0.85,-1.95,1.52),(0,0,1.42),85)
camera('CAM_Lower',(0,-2.4,0.55),(0,0,0.30),80)

sc.render.engine='BLENDER_EEVEE'
sc.render.image_settings.file_format='PNG'
sc.render.film_transparent=False
try: sc.eevee.taa_render_samples=64
except Exception: pass
views=[
 ('render/qc/front.png','CAM_Front',1000,1500),
 ('render/qc/side.png','CAM_Side',1000,1500),
 ('render/qc/back.png','CAM_Back',1000,1500),
 ('render/qc/three_quarter.png','CAM_ThreeQ',1000,1500),
 ('render/final/hero.png','CAM_Hero',1080,1920),
 ('render/final/portrait.png','CAM_Portrait',1000,1200),
 ('render/final/lower_body.png','CAM_Lower',1000,1000),
]
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
import os
for rel,cam,w,h in views:
    sc.camera=bpy.data.objects[cam]
    sc.render.resolution_x=w; sc.render.resolution_y=h; sc.render.resolution_percentage=100
    os.makedirs(os.path.dirname(base+rel),exist_ok=True)
    sc.render.filepath=base+rel
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.render.render(write_still=True)
    print('RENDERED',rel)
# save blend
_g=bpy.data.objects.get('RND-Ground')
if _g: bpy.data.objects.remove(_g, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=base+'Reinforce_Eins_TV.blend')
print('SAVED_BLEND')
