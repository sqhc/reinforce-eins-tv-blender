# -*- coding: utf-8 -*-
import bpy, math, sys, os
WORK = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import spec, lib

for ob in list(bpy.data.objects):
    if ob.type == 'MESH' and ob.name.startswith('GEO-Hair'):
        lib.delete_obj(ob.name)

hair_m = lib.mat('M_Hair', spec.COLORS['hair'], 0.05, 0.32, sheen=0.15)
hair_dark = lib.mat('M_HairShade', '#AEB5C2', 0.0, 0.45)
feather_m = lib.mat('M_HeadFeather', '#EDEFF4', 0.0, 0.35)

CHIN = spec.Z_CHIN; HH = spec.HEAD_H
prof = [
    (0.000,0.006,0.010),(0.030,0.026,0.036),(0.060,0.040,0.052),(0.100,0.052,0.066),
    (0.150,0.062,0.076),(0.210,0.071,0.083),(0.280,0.078,0.088),(0.350,0.082,0.091),
    (0.420,0.084,0.093),(0.500,0.085,0.095),(0.580,0.085,0.096),(0.660,0.083,0.097),
    (0.740,0.080,0.096),(0.810,0.075,0.092),(0.870,0.066,0.085),(0.920,0.054,0.073),
    (0.960,0.039,0.056),(0.985,0.022,0.034),(1.000,0.005,0.010)]
CY = 0.004; FLAT = 0.14

def hwd(z):
    t = max(0.0, min(1.0, (z - CHIN) / HH))
    for i in range(len(prof)-1):
        a,b = prof[i], prof[i+1]
        if a[0] <= t <= b[0]:
            f = (t-a[0])/max(1e-9,b[0]-a[0])
            return (a[1]+(b[1]-a[1])*f, a[2]+(b[2]-a[2])*f)
    return prof[-1][1], prof[-1][2]

def face_y(x,z):
    w,d = hwd(z)
    q = max(0.0, 1.0-(x/max(1e-6,w))**2)
    return CY - d*(1.0-FLAT)*math.sqrt(q)

# ---------- hair cap ----------
cap_rings = []
for t in [0.02,0.06,0.10,0.16,0.22,0.28,0.35,0.42,0.50,0.58,0.66,0.74,0.82,0.89,0.94,0.97,1.0]:
    z = CHIN + t*HH
    w,d = hwd(z)
    cap_rings.append(lib.ring(z, w+0.005, d+0.005, 48, cy=CY, flat_front=0.10))
cap = lib.loft('GEO-Hair_Cap', cap_rings, 'COL_Head', hair_m, cap_start=False, cap_end=True)
# cut face opening: front-lower faces
me = cap.data
bm = __import__('bmesh').new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
kill = []
for f in bm.faces:
    c = f.calc_center_median()
    if c.y < -0.012 and c.z < 1.622:
        kill.append(f)
__import__('bmesh').ops.delete(bm, geom=kill, context='FACES')
bm.to_mesh(me); bm.free(); me.update()
lib.solidify(cap, 0.004, 0.0)

# ---------- elliptical lock ----------
def lock(name, pts, ws, hs, out, matobj=hair_m, n=10, col='COL_Head', cap_start=True, cap_end=True, smooth=True):
    pts = [__import__('mathutils').Vector(p) for p in pts]
    out = __import__('mathutils').Vector(out).normalized()
    rings = []
    for i,p in enumerate(pts):
        if i == 0: t = (pts[1]-pts[0]).normalized()
        elif i == len(pts)-1: t = (pts[-1]-pts[-2]).normalized()
        else: t = (pts[i+1]-pts[i-1]).normalized()
        side = t.cross(out)
        if side.length < 1e-6: side = __import__('mathutils').Vector((1,0,0))
        side.normalize()
        nrm = side.cross(t).normalized()
        w = ws[i]; h = hs[i]
        ring = []
        for k in range(n):
            a = lib.TAU*k/n
            v = p + side*(math.cos(a)*w) + nrm*(math.sin(a)*h)
            ring.append((v.x,v.y,v.z))
        rings.append(ring)
    return lib.loft(name, rings, col, matobj, cap_start=cap_start, cap_end=cap_end, smooth=smooth)

# ---------- bangs ----------
# 6 locks across the forehead, center part
bang_defs = [
    (-0.068, 1.645, 1.588, -0.026, 0.020),
    (-0.042, 1.658, 1.572, -0.016, 0.023),
    (-0.014, 1.662, 1.563, -0.006, 0.024),
    ( 0.014, 1.662, 1.561,  0.006, 0.024),
    ( 0.042, 1.658, 1.570,  0.016, 0.023),
    ( 0.068, 1.645, 1.586,  0.026, 0.020),
]
for i,(x0,z0,z1,dx,w0) in enumerate(bang_defs):
    pts = []
    for k in range(6):
        f = k/5.0
        x = x0 + dx*f + 0.010*math.sin(math.pi*f)
        z = z0 + (z1-z0)*f
        y = face_y(x,z) - 0.006 - 0.006*math.sin(math.pi*f)
        pts.append((x,y,z))
    ws = [w0*0.50, w0*0.85, w0, w0*0.72, w0*0.42, 0.002]
    hs = [0.004,0.005,0.006,0.005,0.004,0.0015]
    lock('GEO-Hair_Bang_%d'%i, pts, ws, hs, (0,-1,0))

# ---------- side locks ----------
for side,sx in (('L',1),('R',-1)):
    for j,off in enumerate([0.0, 0.022]):
        pts = []
        for k in range(7):
            f = k/6.0
            x = sx*(0.082 + off) + sx*0.012*math.sin(math.pi*f)
            z = 1.610 - 0.46*f
            y = -0.010 - 0.020*f + 0.010*math.sin(math.pi*f)
            pts.append((x,y,z))
        ws = [0.014,0.018,0.020,0.018,0.015,0.010,0.003]
        hs = [0.004,0.005,0.006,0.006,0.005,0.004,0.0015]
        lock('GEO-Hair_Side_%s_%d'%(side,j), pts, ws, hs, (sx,-0.4,0))

# ---------- back mass ----------
back_defs = [
    (-0.105, 0.052, 0.980), (-0.070, 0.060, 0.950), (-0.035, 0.066, 0.935),
    ( 0.000, 0.070, 0.930), ( 0.035, 0.066, 0.935), ( 0.070, 0.060, 0.950), ( 0.105, 0.052, 0.980),
]
for i,(x0,wmax,zend) in enumerate(back_defs):
    pts = []
    for k in range(9):
        f = k/8.0
        x = x0*(1.0+0.10*f)
        z = 1.655 - (1.655-zend)*f
        y = 0.072 + 0.060*math.sin(math.pi*f) + 0.018*f
        pts.append((x,y,z))
    ws = [0.020,0.030,0.036,0.040,0.042,0.040,0.034,0.022,0.003]
    hs = [0.006,0.008,0.009,0.010,0.010,0.009,0.008,0.006,0.0015]
    lock('GEO-Hair_Back_%d'%i, pts, ws, hs, (0,1,0))

# ---------- front shoulder locks ----------
for side,sx in (('L',1),('R',-1)):
    pts = []
    for k in range(7):
        f = k/6.0
        x = sx*(0.092 + 0.010*f)
        z = 1.600 - 0.44*f
        y = -0.030 - 0.015*f
        pts.append((x,y,z))
    ws = [0.013,0.017,0.019,0.017,0.014,0.009,0.002]
    hs = [0.004,0.005,0.005,0.005,0.004,0.003,0.0015]
    lock('GEO-Hair_Front_'+side, pts, ws, hs, (sx,-0.6,0))

# ---------- head feather ornament (TV trait, her right = -X) ----------
import mathutils as _mu
froot = _mu.Vector((-0.084, 0.004, 1.642))
for i,(ang,length,w0) in enumerate([(-0.45,0.125,0.022),(0.10,0.145,0.024),(0.62,0.115,0.018)]):
    d = _mu.Vector((-0.55*math.cos(ang), 0.10, math.cos(ang))).normalized()
    d = _mu.Vector((-0.45, 0.05, 1.0)).normalized() if False else d
    pts=[]
    for k in range(5):
        f=k/4.0
        p = froot + d*(length*f) + _mu.Vector((0.0, 0.020*f, 0.012*math.sin(math.pi*f)))
        pts.append((p.x,p.y,p.z))
    ws=[w0,w0*1.1,w0*0.95,w0*0.55,0.002]
    hs=[0.003,0.004,0.0035,0.0025,0.001]
    lock('GEO-Hair_Feather_%d'%i, pts, ws, hs, (0,0,1), matobj=feather_m, n=8)

print('HAIR_OK')