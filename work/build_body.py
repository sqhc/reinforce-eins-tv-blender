# -*- coding: utf-8 -*-
import bpy, math, sys, os
WORK = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import spec, lib

for nm in ['GEO-Body','GEO-Arm_L','GEO-Arm_R','GEO-Leg_L','GEO-Leg_R','GEO-Foot_L','GEO-Foot_R']:
    lib.delete_obj(nm)

skin = lib.mat('M_Skin', spec.COLORS['skin'], 0.0, 0.58)

# ---- torso ----
prof = [
    (0.780, 0.150, 0.100, 0.000),
    (0.840, 0.160, 0.104, 0.000),
    (0.900, 0.156, 0.102, 0.000),
    (0.960, 0.136, 0.094, 0.000),
    (1.000, 0.110, 0.081, 0.000),
    (1.040, 0.101, 0.076, 0.000),
    (1.080, 0.109, 0.082, 0.000),
    (1.120, 0.121, 0.088, 0.000),
    (1.160, 0.133, 0.094, 0.000),
    (1.200, 0.143, 0.099, 0.000),
    (1.232, 0.149, 0.101, 0.000),
    (1.262, 0.153, 0.099, 0.000),
    (1.292, 0.157, 0.095, 0.000),
    (1.322, 0.161, 0.089, 0.000),
    (1.338, 0.160, 0.083, 0.000),
    (1.352, 0.140, 0.077, 0.000),
    (1.372, 0.106, 0.070, 0.000),
    (1.392, 0.074, 0.061, 0.000),
    (1.412, 0.058, 0.054, 0.000),
    (1.432, 0.052, 0.050, 0.000),
    (1.452, 0.050, 0.048, 0.000),
]
rings = [lib.ring(z, rx, ry, 48, flat_front=0.10, power=2.0) for (z, rx, ry, _) in prof]
torso = lib.loft('GEO-Body', rings, 'COL_Body', skin, cap_start=True, cap_end=True, smooth=True)

# bust + butt shaping
me = torso.data
for v in me.vertices:
    x, y, z = v.co
    if y < 0.02 and 1.13 < z < 1.33:
        for sx in (-1.0, 1.0):
            g = math.exp(-(((x - sx * 0.068) / 0.052) ** 2 + ((z - 1.238) / 0.050) ** 2))
            v.co.y -= 0.030 * g
    if y > 0.0 and 0.815 < z < 0.965:
        g = math.exp(-(((abs(x) - 0.070) / 0.060) ** 2 + ((z - 0.890) / 0.045) ** 2))
        v.co.y += 0.020 * g
me.update()

# ---- arms ----
for side in ('L', 'R'):
    pts = spec.ARM[side]
    arm = lib.tube('GEO-Arm_' + side, pts[:3], spec.ARM_R[:3], 'COL_Body', skin, n=16, caps=True)
    # elbow/wrist smoothing
    lib.subsurf(arm, 1)

# ---- legs ----
for side in ('L', 'R'):
    pts = spec.LEG[side]
    leg = lib.tube('GEO-Leg_' + side, pts, spec.LEG_R, 'COL_Body', skin, n=16, caps=True)
    lib.subsurf(leg, 1)

# ---- feet (simple, hidden by boots) ----
for side, sx in (('L', 1), ('R', -1)):
    x = sx * 0.075
    verts = [
        (x-0.045, -0.14, 0.005), (x+0.045, -0.14, 0.005), (x+0.045, 0.06, 0.005), (x-0.045, 0.06, 0.005),
        (x-0.042, -0.12, 0.075), (x+0.042, -0.12, 0.075), (x+0.042, 0.05, 0.095), (x-0.042, 0.05, 0.095),
    ]
    faces = [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    ft = lib.new_obj('GEO-Foot_' + side, verts, faces, 'COL_Body', skin, smooth=True)
    lib.subsurf(ft, 1)

print('BODY_OK verts=%d' % len(torso.data.vertices))
for ob in bpy.data.objects:
    if ob.type == 'MESH' and ob.name.startswith('GEO-'):
        print(ob.name, 'z[%.3f,%.3f]' % (min(v.co.z for v in ob.data.vertices), max(v.co.z for v in ob.data.vertices)))
