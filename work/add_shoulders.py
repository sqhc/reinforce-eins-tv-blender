# -*- coding: utf-8 -*-
import bpy, bmesh
from mathutils import Matrix
dress=bpy.data.materials['M_Dress']
rig=bpy.data.objects['RIG-Reinforce']
for side,sx in (('L',1),('R',-1)):
    nm='GEO-Dress_Shoulder_'+side
    old=bpy.data.objects.get(nm)
    if old: bpy.data.objects.remove(old, do_unlink=True)
    me=bpy.data.meshes.new(nm); bm=bmesh.new()
    mtx=Matrix.Translation((sx*0.165,0.0,1.344)) @ Matrix.Diagonal((0.078,0.072,0.074,1.0))
    bmesh.ops.create_uvsphere(bm,u_segments=24,v_segments=16,radius=1.0,matrix=mtx)
    bmesh.ops.recalc_face_normals(bm,faces=bm.faces)
    bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(nm,me); bpy.data.collections['COL_Dress'].objects.link(ob)
    for p in me.polygons: p.use_smooth=True
    me.materials.append(dress)
    vg=ob.vertex_groups.new(name='upperarm_'+side)
    vg.add([v.index for v in me.vertices],1.0,'REPLACE')
    md=ob.modifiers.new('Armature','ARMATURE'); md.object=rig
    ob.parent=rig; ob.matrix_parent_inverse=rig.matrix_world.inverted()
print('CAPS_OK')
