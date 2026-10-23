# -*- coding: utf-8 -*-
import bpy, math, sys, os
WORK = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import spec, lib

for nm in list(bpy.data.objects.keys()):
    if nm.startswith(('GEO-Head','GEO-Face','GEO-Eye','GEO-Iris','GEO-Pupil','GEO-Lash','GEO-Brow','GEO-Mouth','GEO-Nose')):
        lib.delete_obj(nm)

skin = lib.mat('M_Skin', spec.COLORS['skin'], 0.0, 0.58)
eye_white = lib.mat('M_EyeWhite', spec.COLORS['eye_white'], 0.0, 0.35)
iris_m = lib.mat('M_Iris', spec.COLORS['iris'], 0.0, 0.30)
pupil_m = lib.mat('M_Pupil', spec.COLORS['pupil'], 0.0, 0.25)
lash_m = lib.mat('M_Lash', spec.COLORS['lash'], 0.0, 0.45)
brow_m = lib.mat('M_Brow', '#C9CED8', 0.0, 0.5)
mouth_m = lib.mat('M_Mouth', '#8A4348', 0.0, 0.5)

# head profile relative to chin: (t, half_width, half_depth)
prof = [
    (0.000, 0.006, 0.010),
    (0.030, 0.028, 0.036),
    (0.060, 0.043, 0.052),
    (0.100, 0.056, 0.066),
    (0.150, 0.066, 0.076),
    (0.210, 0.075, 0.083),
    (0.280, 0.083, 0.088),
    (0.350, 0.087, 0.091),
    (0.420, 0.089, 0.093),
    (0.500, 0.090, 0.095),
    (0.580, 0.090, 0.096),
    (0.660, 0.088, 0.097),
    (0.740, 0.085, 0.096),
    (0.810, 0.079, 0.092),
    (0.870, 0.070, 0.085),
    (0.920, 0.057, 0.073),
    (0.960, 0.041, 0.056),
    (0.985, 0.023, 0.034),
    (1.000, 0.005, 0.010),
]
CHIN = spec.Z_CHIN
HH = spec.HEAD_H

def head_wd(z):
    t = (z - CHIN) / HH
    t = max(0.0, min(1.0, t))
    for i in range(len(prof) - 1):
        a, b = prof[i], prof[i+1]
        if a[0] <= t <= b[0]:
            f = (t - a[0]) / max(1e-9, b[0] - a[0])
            return (a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f)
    return prof[-1][1], prof[-1][2]

FLAT = 0.14
CY = 0.004

def face_y(x, z):
    w, d = head_wd(z)
    q = max(0.0, 1.0 - (x / max(1e-6, w)) ** 2)
    return CY - d * (1.0 - FLAT) * math.sqrt(q)

rings = []
for (t, w, d) in prof:
    z = CHIN + t * HH
    rings.append(lib.ring(z, w, d, 48, cy=CY, flat_front=FLAT))
head = lib.loft('GEO-Head', rings, 'COL_Head', skin, cap_start=True, cap_end=True, smooth=True)

# nose bump
me = head.data
for v in me.vertices:
    x, y, z = v.co
    if y < 0 and 1.500 < z < 1.540 and abs(x) < 0.022:
        g = math.exp(-((x / 0.014) ** 2 + ((z - 1.514) / 0.014) ** 2))
        v.co.y -= 0.008 * g
me.update()

# ---- anime eye: one curved patch with 4 material zones ----
def eye_mesh(name, cx, cz, ax, az, tilt, sx):
    n = 32
    rr = [0.30, 0.62, 1.00]
    verts = []
    verts.append((cx, face_y(cx, cz) - 0.0010, cz))
    for r in rr:
        for i in range(n):
            a = lib.TAU * i / n
            x = cx + ax * r * math.cos(a)
            z = cz + az * r * math.sin(a) + tilt * math.cos(a)
            verts.append((x, face_y(x, z) - 0.0010, z))
    faces = []
    mats = []
    for i in range(n):
        j = (i + 1) % n
        faces.append((0, 1 + i, 1 + j)); mats.append(2)          # pupil
    for i in range(n):
        j = (i + 1) % n
        faces.append((1 + i, 1 + n + i, 1 + n + j, 1 + j)); mats.append(1)  # iris
    for i in range(n):
        j = (i + 1) % n
        a = lib.TAU * (i + 0.5) / n
        mi = 3 if math.sin(a) > 0.55 else 0
        faces.append((1 + n + i, 1 + 2 * n + i, 1 + 2 * n + j, 1 + n + j)); mats.append(mi)
    ob = lib.new_obj(name, verts, faces, 'COL_Head', eye_white, smooth=True)
    me = ob.data
    for m in (iris_m, pupil_m, lash_m):
        me.materials.append(m)
    for f, mi in zip(me.polygons, mats):
        f.material_index = mi
    lib.solidify(ob, 0.0006, 0.0)
    return ob

def band(name, pts2d, width, matobj, col='COL_Head', thick=0.0012):
    top = [(x, face_y(x, z + width * 0.5) - 0.0010, z + width * 0.5) for (x, z) in pts2d]
    bot = [(x, face_y(x, z - width * 0.5) - 0.0010, z - width * 0.5) for (x, z) in pts2d]
    n = len(pts2d)
    verts = top + bot
    faces = []
    for i in range(n - 1):
        faces.append((i, i + 1, n + i + 1, n + i))
    ob = lib.new_obj(name, verts, faces, col, matobj, smooth=True)
    lib.solidify(ob, thick, 0.0)
    return ob

for side, sx in (('L', 1.0), ('R', -1.0)):
    ex = sx * 0.040
    ez = 1.548
    eye_mesh('GEO-Eye_' + side, ex, ez, 0.0240, 0.0130, sx * 0.0035, sx)
    brow = []
    for k in range(9):
        f = k / 8.0
        x = ex + sx * (-0.022 + 0.044 * f)
        z = 1.578 + 0.006 * math.sin(math.pi * f) - 0.004 * f
        brow.append((x, z))
    band('GEO-Brow_' + side, brow, 0.0030, brow_m, thick=0.0010)

# mouth
mp = []
for k in range(9):
    f = k / 8.0
    x = -0.013 + 0.026 * f
    z = 1.494 + 0.0025 * math.sin(math.pi * f)
    mp.append((x, face_y(x, z) - 0.0008, z))
mouth = lib.tube('GEO-Mouth', mp, 0.0016, 'COL_Head', mouth_m, n=8, caps=True)

print('HEAD_OK verts=%d' % len(head.data.vertices))
for ob in bpy.data.objects:
    if ob.type == 'MESH' and ob.name.startswith('GEO-') and 'Head' in ob.name:
        print(ob.name, len(ob.data.vertices))
