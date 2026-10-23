# -*- coding: utf-8 -*-
import bpy, math, sys, os
from mathutils import Vector
WORK = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import spec, lib

for ob in list(bpy.data.objects):
    if ob.type=='MESH' and (ob.name.startswith('GEO-Hand') or ob.name.startswith('GEO-Finger') or ob.name.startswith('GEO-Thumb')):
        lib.delete_obj(ob.name)
skin = lib.mat('M_Skin', spec.COLORS['skin'], 0.0, 0.58)
glove = lib.mat('M_Boot', spec.COLORS['boot'], 0.0, 0.40)

def hand(side, sx):
    elbow = Vector((sx*0.335, 0, 1.110))
    wrist = Vector((sx*0.475, 0, 0.905))
    fwd = (wrist - elbow).normalized()
    sidev = Vector((0,1,0))
    sidev = (sidev - fwd*sidev.dot(fwd)).normalized()
    nrm = fwd.cross(sidev).normalized()
    base = wrist + fwd*0.005
    # palm loft along fwd
    rings=[]
    for t,w,th in [(0.0,0.056,0.024),(0.045,0.064,0.028),(0.080,0.060,0.024),(0.095,0.050,0.020)]:
        c = base + fwd*t
        ring=[]
        for k in range(16):
            a = lib.TAU*k/16
            v = c + sidev*(math.cos(a)*w*0.5) + nrm*(math.sin(a)*th*0.5)
            ring.append((v.x,v.y,v.z))
        rings.append(ring)
    palm = lib.loft('GEO-Hand_'+side, rings, 'COL_Arms', glove, cap_start=True, cap_end=True, smooth=True)
    # fingers
    end = base + fwd*0.092
    for i,off in enumerate([-0.024,-0.008,0.008,0.024]):
        p0 = end + sidev*off
        direction = (fwd + nrm*0.10).normalized()
        length = 0.052 if i in (1,2) else 0.046
        p1 = p0 + direction*length*0.55
        p2 = p0 + direction*length + nrm*0.004
        lib.tube('GEO-Finger_%s_%d'%(side,i), [p0,p1,p2], [0.0075,0.0068,0.0045], 'COL_Arms', skin, n=8, caps=True)
    # thumb
    t0 = base + fwd*0.035 - sidev*0.032 + nrm*0.002
    td = (fwd*0.4 - sidev*0.8 + nrm*0.2).normalized()
    t1 = t0 + td*0.03
    t2 = t0 + td*0.048
    lib.tube('GEO-Thumb_'+side, [t0,t1,t2], [0.0085,0.0075,0.0050], 'COL_Arms', skin, n=8, caps=True)

for side, sx in (('L',1),('R',-1)):
    hand(side, sx)
print('HANDS_OK')
for ob in bpy.data.objects:
    if ob.type=='MESH' and (ob.name.startswith('GEO-Hand') or ob.name.startswith('GEO-Finger') or ob.name.startswith('GEO-Thumb')):
        print(ob.name, len(ob.data.vertices))
