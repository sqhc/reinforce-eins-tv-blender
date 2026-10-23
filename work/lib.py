# -*- coding: utf-8 -*-
import bpy, bmesh, math
from mathutils import Vector, Matrix

TAU = math.pi * 2.0

def srgb(c):
    c = float(c)
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def hex_lin(h):
    h = h.lstrip('#')
    return tuple(srgb(int(h[i:i+2], 16) / 255.0) for i in (0, 2, 4))

def coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c

def link(ob, colname):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    coll(colname).objects.link(ob)

def mat(name, hexcolor, metallic=0.0, roughness=0.6, sheen=0.0, emission=None, estr=0.0):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get('Principled BSDF')
    if bsdf is None:
        for n in nt.nodes:
            if n.type == 'BSDF_PRINCIPLED':
                bsdf = n
                break
    col = hex_lin(hexcolor)
    bsdf.inputs['Base Color'].default_value = (*col, 1.0)
    bsdf.inputs['Metallic'].default_value = float(metallic)
    bsdf.inputs['Roughness'].default_value = float(roughness)
    try:
        bsdf.inputs['Sheen Weight'].default_value = float(sheen)
        if sheen > 0:
            bsdf.inputs['Sheen Tint'].default_value = (*hex_lin('#FFFFFF'), 1.0)
    except Exception:
        pass
    if emission:
        try:
            bsdf.inputs['Emission Color'].default_value = (*hex_lin(emission), 1.0)
            bsdf.inputs['Emission Strength'].default_value = float(estr)
        except Exception:
            pass
    m.diffuse_color = (*col, 1.0)
    return m

def new_obj(name, verts, faces, colname, matobj=None, smooth=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces])
    me.update()
    ob = bpy.data.objects.new(name, me)
    coll(colname).objects.link(ob)
    if matobj is not None:
        me.materials.append(matobj)
    for p in me.polygons:
        p.use_smooth = bool(smooth)
    return ob

def ring(z, rx, ry, n=48, cx=0.0, cy=0.0, flat_front=0.0, power=2.0, front_bulge=0.0):
    pts = []
    for i in range(n):
        a = TAU * i / n
        c, s = math.cos(a), math.sin(a)
        if abs(power - 2.0) > 1e-9:
            c = math.copysign(abs(c) ** (2.0 / power), c)
            s = math.copysign(abs(s) ** (2.0 / power), s)
        x = cx + rx * c
        y = cy + ry * s
        if s < 0:
            y *= (1.0 - flat_front)
            y -= front_bulge * (-s)
        pts.append((x, y, z))
    return pts

def loft(name, rings, colname, matobj=None, cap_start=True, cap_end=True, smooth=True):
    n = len(rings[0])
    verts = []
    for r in rings:
        assert len(r) == n
        verts.extend(r)
    faces = []
    for k in range(len(rings) - 1):
        b0, b1 = k * n, (k + 1) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((b0 + i, b0 + j, b1 + j, b1 + i))
    if cap_start:
        faces.append(tuple(range(n - 1, -1, -1)))
    if cap_end:
        b = (len(rings) - 1) * n
        faces.append(tuple(range(b, b + n)))
    ob = new_obj(name, verts, faces, colname, matobj, smooth)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(ob.data)
    bm.free()
    return ob

def tube(name, pts, radii, colname, matobj=None, n=16, caps=True, smooth=True):
    pts = [Vector(p) for p in pts]
    rings = []
    for i, p in enumerate(pts):
        if i == 0:
            t = (pts[1] - pts[0]).normalized()
        elif i == len(pts) - 1:
            t = (pts[-1] - pts[-2]).normalized()
        else:
            t = (pts[i + 1] - pts[i - 1]).normalized()
        up = Vector((0, 0, 1))
        if abs(t.dot(up)) > 0.95:
            up = Vector((0, 1, 0))
        sx = t.cross(up).normalized()
        sy = sx.cross(t).normalized()
        r = radii[i] if isinstance(radii, (list, tuple)) else radii
        ring = []
        for k in range(n):
            a = TAU * k / n
            v = p + sx * (math.cos(a) * r) + sy * (math.sin(a) * r)
            ring.append((v.x, v.y, v.z))
        rings.append(ring)
    return loft(name, rings, colname, matobj, cap_start=caps, cap_end=caps, smooth=smooth)

def solidify(ob, thickness, offset=0.0, mat_offset=0):
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.selected_objects:
        o.select_set(False)
    ob.select_set(True)
    md = ob.modifiers.new('solidify', 'SOLIDIFY')
    md.thickness = float(thickness)
    md.offset = float(offset)
    md.material_offset = int(mat_offset)
    md.use_rim = True
    md.use_rim_only = False
    bpy.ops.object.modifier_apply(modifier=md.name)
    return ob

def subsurf(ob, levels=1):
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.selected_objects:
        o.select_set(False)
    ob.select_set(True)
    md = ob.modifiers.new('subsurf', 'SUBSURF')
    md.levels = int(levels)
    md.render_levels = int(levels)
    bpy.ops.object.modifier_apply(modifier=md.name)
    return ob

def apply_mods(ob):
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.selected_objects:
        o.select_set(False)
    ob.select_set(True)
    for m in list(ob.modifiers):
        try:
            bpy.ops.object.modifier_apply(modifier=m.name)
        except Exception:
            pass
    return ob

def mirror_x(ob, newname):
    me = ob.data.copy()
    nb = bpy.data.objects.new(newname, me)
    for c in ob.users_collection:
        c.objects.link(nb)
    nb.matrix_world = ob.matrix_world.copy()
    nb.scale.x = -1.0
    bpy.context.view_layer.objects.active = nb
    for o in bpy.context.selected_objects:
        o.select_set(False)
    nb.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bm = bmesh.new(); bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    return nb

def translate(ob, v):
    ob.location = (ob.location.x + v[0], ob.location.y + v[1], ob.location.z + v[2])
    return ob

def delete_obj(name):
    ob = bpy.data.objects.get(name)
    if ob:
        me = ob.data if ob.type == 'MESH' else None
        bpy.data.objects.remove(ob, do_unlink=True)
        if me is not None and me.users == 0:
            bpy.data.meshes.remove(me)

def bbox(ob):
    vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
    if not vs:
        return None
    return (min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs),
            max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs))

def smoothstep(a, b, x):
    if a == b:
        return 0.0 if x < a else 1.0
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)
