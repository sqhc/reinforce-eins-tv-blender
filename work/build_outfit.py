# -*- coding: utf-8 -*-
import bpy, math, sys, os
from mathutils import Vector
WORK = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import spec, lib

for ob in list(bpy.data.objects):
    if ob.type == 'MESH' and (ob.name.startswith('GEO-Dress') or ob.name.startswith('GEO-Coat') or ob.name.startswith('GEO-Belt') or ob.name.startswith('GEO-Stocking') or ob.name.startswith('GEO-Boot') or ob.name.startswith('GEO-Glove') or ob.name.startswith('GEO-Hand') or ob.name.startswith('GEO-Finger') or ob.name.startswith('GEO-Thumb')):
        lib.delete_obj(ob.name)

dress = lib.mat('M_Dress', spec.COLORS['dress'], 0.0, 0.72, sheen=0.25)
dress2 = lib.mat('M_Dress2', spec.COLORS['dress2'], 0.0, 0.70, sheen=0.2)
white = lib.mat('M_White', spec.COLORS['white'], 0.0, 0.45)
gold = lib.mat('M_Gold', spec.COLORS['gold'], 0.85, 0.32)
stock = lib.mat('M_Stocking', spec.COLORS['stocking'], 0.0, 0.55)
boot = lib.mat('M_Boot', spec.COLORS['boot'], 0.0, 0.40)
lining = lib.mat('M_CoatLining', '#7A5C1C', 0.55, 0.45)

def torus_ring(name, loc, major, minor, scale=(1,1,1), rot=(0,0,0), matobj=None, col='COL_Dress', seg=48, mseg=8):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=seg, minor_segments=mseg, location=loc, rotation=rot)
    ob=bpy.context.active_object
    ob.name=name
    for c in list(ob.users_collection): c.objects.unlink(ob)
    bpy.data.collections[col].objects.link(ob)
    ob.scale=scale
    bpy.context.view_layer.objects.active=ob
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if matobj is not None: ob.data.materials.append(matobj)
    for pp in ob.data.polygons: pp.use_smooth=True
    return ob

skin = lib.mat('M_Skin', spec.COLORS['skin'], 0.0, 0.58)

# ---------------- bodice ----------------
bprof = [
    (0.995, 0.112, 0.090),
    (1.020, 0.108, 0.088),
    (1.060, 0.114, 0.094),
    (1.100, 0.122, 0.100),
    (1.140, 0.134, 0.109),
    (1.180, 0.146, 0.122),
    (1.220, 0.156, 0.139),
    (1.260, 0.164, 0.142),
    (1.290, 0.169, 0.129),
    (1.320, 0.166, 0.109),
    (1.350, 0.125, 0.085),
    (1.370, 0.090, 0.068),
    (1.390, 0.068, 0.058),
    (1.410, 0.062, 0.054),
]
def bp(z):
    for i in range(len(bprof)-1):
        a,b = bprof[i], bprof[i+1]
        if a[0] <= z <= b[0]:
            f = (z-a[0])/max(1e-9,b[0]-a[0])
            return (a[1]+(b[1]-a[1])*f, a[2]+(b[2]-a[2])*f)
    return bprof[-1][1], bprof[-1][2]

rings = [lib.ring(z, rx, ry, 48, flat_front=0.10) for (z,rx,ry) in bprof]
bod = lib.loft('GEO-Dress_Bodice', rings, 'COL_Dress', dress, cap_start=False, cap_end=False)
# cut armholes: sides above 1.265
me = bod.data
bm = __import__('bmesh').new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
kill=[]
for f in bm.faces:
    c=f.calc_center_median()
    if c.z > 1.278 and abs(c.x) > 0.122:
        kill.append(f)
__import__('bmesh').ops.delete(bm, geom=kill, context='FACES')
bm.to_mesh(me); bm.free(); me.update()
lib.solidify(bod, 0.003, 0.0)

# white collar piping
torus_ring('GEO-Dress_PipingCollar', (0,0,1.409), 0.062, 0.0022, scale=(1,0.054/0.062,1), matobj=white, col='COL_Dress', seg=48, mseg=8)

# ---------------- sleeves ----------------
def sleeve(side, sx):
    sh = Vector((sx*spec.SHOULDER_X, 0, spec.Z_SHOULDER))
    el = Vector((sx*0.335, 0, 1.110))
    d = (el - sh)
    pts = []
    rs = []
    for k in range(6):
        f = k/5.0*0.62
        p = sh + d*f
        pts.append((p.x, p.y, p.z))
        rs.append([0.066, 0.078, 0.082, 0.078, 0.068, 0.052][k])
    sl = lib.tube('GEO-Dress_Sleeve_'+side, pts, rs, 'COL_Dress', dress, n=20, caps=False)
    lib.solidify(sl, 0.002, 0.0)
    cuff = Vector(pts[-1]); dirc = (Vector(pts[-1])-Vector(pts[-2])).normalized()
    rotc = Vector((0,0,1)).rotation_difference(dirc).to_euler()
    torus_ring('GEO-Dress_PipingSleeve_'+side, cuff, 0.056, 0.0022, rot=rotc, matobj=white, col='COL_Dress', seg=32, mseg=6)
for side, sx in (('L',1),('R',-1)):
    sleeve(side, sx)

# ---------------- skirt ----------------
sk = [(1.005,0.120,0.096),(0.965,0.132,0.106),(0.920,0.152,0.120),(0.870,0.172,0.134),(0.820,0.190,0.148),(0.785,0.202,0.158)]
skr = [lib.ring(z,rx,ry,48,flat_front=0.06) for (z,rx,ry) in sk]
skirt = lib.loft('GEO-Dress_Skirt', skr, 'COL_Dress', dress, cap_start=False, cap_end=False)
lib.solidify(skirt, 0.003, 0.0)

# ---------------- belt ----------------
btr = [lib.ring(1.000,0.122,0.098,48),lib.ring(1.024,0.126,0.101,48),lib.ring(1.048,0.124,0.099,48)]
belt = lib.loft('GEO-Belt', btr, 'COL_Dress', dress2, cap_start=False, cap_end=False)
lib.solidify(belt, 0.003, 0.0)
for zz in (1.003, 1.045):
    torus_ring('GEO-Belt_Trim_%d'%int(zz*1000), (0,0,zz), 0.126, 0.0026, scale=(1,0.101/0.126,1), matobj=gold, col='COL_Dress', seg=48, mseg=6)
# studs
for i in range(6):
    x = -0.075 + 0.030*i
    zz = 1.024
    rx, ry = 0.126, 0.101
    yy = -ry*math.sqrt(max(0.0,1-(x/rx)**2)) - 0.002
    lib.tube('GEO-Belt_Stud_%d'%i, [(x,yy+0.004,zz),(x,yy-0.004,zz)], 0.0055, 'COL_Dress', gold, n=10, caps=True)

# ---------------- gold chest X trim ----------------
def bfront(x,z):
    rx, ry = bp(z)
    q = max(0.0, 1-(x/rx)**2)
    return -ry*math.sqrt(q)*(1-0.10) - 0.001
lines = [
    [(-0.100,1.300),(0.060,1.020)],
    [(0.100,1.300),(-0.060,1.020)],
    [(0.0,1.300),(0.0,1.020)],
]
for li,(a,b) in enumerate(lines):
    if li == 2:
        verts=[]
        for k in range(11):
            f=k/10.0
            z=1.300+(1.020-1.300)*f
            y=bfront(0.0,z)-0.0006
            verts.append((0.0032,y,z)); verts.append((-0.0032,y,z))
        faces=[]
        for k in range(10):
            faces.append((2*k,2*k+1,2*k+3,2*k+2))
        ob=lib.new_obj('GEO-Dress_TrimX_2', verts, faces, 'COL_Dress', gold, smooth=True)
        lib.solidify(ob, 0.0012, 0.0)
    else:
        pts=[]
        for k in range(11):
            f=k/10.0
            x=a[0]+(b[0]-a[0])*f
            z=a[1]+(b[1]-a[1])*f
            pts.append((x,bfront(x,z),z))
        lib.tube('GEO-Dress_TrimX_%d'%li, pts, 0.0032, 'COL_Dress', gold, n=8, caps=True)

# ---------------- coat tails ----------------
def panel(name, grid, outer, inner, thick=0.0025):
    nu=len(grid); nv=len(grid[0])
    verts=[]; 
    for row in grid:
        for p in row: verts.append(p)
    faces=[]
    for i in range(nu-1):
        for j in range(nv-1):
            a=i*nv+j; b=a+1; c=(i+1)*nv+j+1; d=(i+1)*nv+j
            faces.append((a,b,c,d))
    ob=lib.new_obj(name, verts, faces, 'COL_Dress', outer, smooth=True)
    ob.data.materials.append(inner)
    import bmesh as _bm, mathutils as _mu
    bm=_bm.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
    for f in bm.faces:
        c=f.calc_center_median(); n=f.normal
        radial=_mu.Vector((c.x,c.y,0.0))
        if radial.length>1e-6 and n.dot(radial)<0:
            f.normal_flip()
    bm.to_mesh(ob.data); bm.free(); ob.data.update()
    lib.solidify(ob, thick, 0.0, mat_offset=1)
    return ob

for side,sx in (('L',1),('R',-1)):
    grid=[]
    for i in range(12):
        u=i/11.0
        row=[]
        for j in range(6):
            v=j/5.0
            x=sx*((0.018+0.085*v)+(0.060+0.150*v)*u)
            z=1.000-0.820*u
            y=0.105+0.050*u+0.018*math.sin(math.pi*v)
            row.append((x,y,z))
        grid.append(row)
    panel('GEO-Coat_Back_'+side, grid, dress, lining)
    grid=[]
    for i in range(10):
        u=i/9.0
        row=[]
        for v in (0.0,1.0):
            x=sx*((0.128+0.045*v)+(0.055+0.080*v)*u)
            z=1.000-0.820*u
            y=0.035+0.045*u
            row.append((x,y,z))
        grid.append(row)
    panel('GEO-Coat_Side_'+side, grid, dress, lining, thick=0.0025)

# ---------------- high collar ----------------
col_rings = []
for z,rx,ry in [(1.398,0.064,0.060),(1.420,0.060,0.057),(1.442,0.057,0.054),(1.458,0.055,0.052)]:
    col_rings.append(lib.ring(z,rx,ry,40,flat_front=0.06))
collar = lib.loft('GEO-Dress_Collar', col_rings, 'COL_Dress', dress, cap_start=False, cap_end=False)
lib.solidify(collar, 0.0025, 0.0)
torus_ring('GEO-Dress_PipingCollarTop', (0,0,1.457), 0.055, 0.0020, scale=(1,0.052/0.055,1), matobj=white, col='COL_Dress', seg=40, mseg=6)

# ---------------- stockings ----------------
def leg_x(z, sx):
    # linear between hip 0.09@0.87 and knee 0.085@0.448 and ankle 0.075@0.06
    if z>=0.448:
        f=(0.87-z)/(0.87-0.448); return sx*(0.090+(0.085-0.090)*f)
    f=(0.448-z)/(0.448-0.06); return sx*(0.085+(0.075-0.085)*f)
for side,sx in (('L',1),('R',-1)):
    pts=[]; rs=[]
    for z,r in [(0.640,0.097),(0.580,0.092),(0.520,0.083),(0.460,0.071),(0.420,0.074),(0.380,0.079),(0.360,0.081)]:
        pts.append((leg_x(z,sx),0.004,z)); rs.append(r)
    st=lib.tube('GEO-Stocking_'+side, pts, rs, 'COL_Legs', stock, n=20, caps=False)
    lib.solidify(st,0.0015,0.0)

# ---------------- boots ----------------
for side,sx in (('L',1),('R',-1)):
    prof=[(0.360,0.070,0.072,0.004),(0.310,0.064,0.066,0.004),(0.260,0.057,0.060,0.002),
          (0.210,0.051,0.057,0.000),(0.150,0.047,0.060,-0.004),(0.100,0.048,0.077,-0.020),
          (0.055,0.051,0.096,-0.045),(0.020,0.052,0.104,-0.055),(0.002,0.048,0.098,-0.055)]
    rings=[]
    for (z,rx,ry,cy) in prof:
        rings.append(lib.ring(z,rx,ry,24,cx=sx*0.075,cy=cy))
    bo=lib.loft('GEO-Boot_'+side,rings,'COL_Legs',boot,cap_start=False,cap_end=True)
    lib.solidify(bo,0.003,0.0)
    # gold top band
    torus_ring('GEO-Boot_Trim_'+side, (sx*0.075,0.004,0.352), 0.083, 0.0030, matobj=gold, col='COL_Legs', seg=32, mseg=6)
    # sole
    vs=[(sx*0.030,-0.160,0.000),(sx*0.130,-0.160,0.000),(sx*0.130,0.070,0.000),(sx*0.030,0.070,0.000),
        (sx*0.030,-0.155,0.020),(sx*0.125,-0.155,0.020),(sx*0.125,0.065,0.020),(sx*0.025,0.065,0.020)]
    fs=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    lib.new_obj('GEO-Boot_Sole_'+side, vs, fs, 'COL_Legs', boot, smooth=False)

# ---------------- gloves ----------------
for side,sx in (('L',1),('R',-1)):
    elbow=Vector((sx*0.335,0,1.110)); wrist=Vector((sx*0.475,0,0.905))
    d=(wrist-elbow)
    pts=[]; rs=[]
    for k in range(5):
        f=k/4.0
        p=elbow+d*(0.55+0.45*f)
        pts.append((p.x,p.y,p.z)); rs.append(0.040-0.008*f)
    gl=lib.tube('GEO-Glove_'+side, pts, rs, 'COL_Arms', boot, n=16, caps=False)
    lib.solidify(gl,0.002,0.0)
    # gold cuff ring at wrist
    wv=Vector(pts[-1]); dg=(Vector(pts[-1])-Vector(pts[-2])).normalized()
    rotg=Vector((0,0,1)).rotation_difference(dg).to_euler()
    torus_ring('GEO-Glove_Trim_'+side, wv, 0.033, 0.0022, rot=rotg, matobj=gold, col='COL_Arms', seg=24, mseg=6)

print('OUTFIT_OK')
for ob in bpy.data.objects:
    if ob.type=='MESH' and (ob.name.startswith('GEO-Dress') or ob.name.startswith('GEO-Coat') or ob.name.startswith('GEO-Boot') or ob.name.startswith('GEO-Belt')):
        print(ob.name, len(ob.data.vertices))
