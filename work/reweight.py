# -*- coding: utf-8 -*-
import bpy, math
from mathutils import Vector
rig=bpy.data.objects['RIG-Reinforce']

def clear(ob):
    for vg in list(ob.vertex_groups): ob.vertex_groups.remove(vg)
def VG(ob,n):
    vg=ob.vertex_groups.get(n)
    if vg is None: vg=ob.vertex_groups.new(name=n)
    return vg
def seg_t(p,a,b):
    ab=b-a; return max(0.0,min(1.0,(p-a).dot(ab)/max(1e-12,ab.length_squared)))

# sleeves: blend chest at the top, upperarm below
for side,sx in (('L',1),('R',-1)):
    ob=bpy.data.objects.get('GEO-Dress_Sleeve_'+side)
    if not ob: continue
    clear(ob); gc=VG(ob,'chest'); gu=VG(ob,'upperarm_'+side)
    sh=Vector((sx*0.165,0,1.344)); el=Vector((sx*0.335,0,1.110))
    for v in ob.data.vertices:
        t=seg_t(v.co,sh,el)
        wc=0.0*max(0.0,1.0-t/0.30)
        gu.add([v.index],1.0-wc,'REPLACE'); gc.add([v.index],wc,'REPLACE')

# gloves: forearm + hand blend near wrist
for side,sx in (('L',1),('R',-1)):
    ob=bpy.data.objects.get('GEO-Glove_'+side)
    if not ob: continue
    clear(ob); gf=VG(ob,'forearm_'+side); gh=VG(ob,'hand_'+side)
    el=Vector((sx*0.335,0,1.110)); wr=Vector((sx*0.475,0,0.905))
    for v in ob.data.vertices:
        t=seg_t(v.co,el,wr)
        wh=0.55*max(0.0,(t-0.65)/0.35)
        gf.add([v.index],1.0-wh,'REPLACE'); gh.add([v.index],wh,'REPLACE')
    # gold cuff too
    ob=bpy.data.objects.get('GEO-Glove_Trim_'+side)
    if ob:
        clear(ob); gf=VG(ob,'forearm_'+side); gh=VG(ob,'hand_'+side)
        for v in ob.data.vertices:
            gf.add([v.index],0.6,'REPLACE'); gh.add([v.index],0.4,'REPLACE')

# stockings: shin/thigh, no foot below boot top
for side,sx in (('L',1),('R',-1)):
    ob=bpy.data.objects.get('GEO-Stocking_'+side)
    if not ob: continue
    clear(ob); gs=VG(ob,'shin_'+side); gt=VG(ob,'thigh_'+side)
    for v in ob.data.vertices:
        z=v.co.z
        wt=0.0
        if z>0.48:
            wt=min(1.0,(z-0.48)/0.16)
        gs.add([v.index],1.0-wt,'REPLACE'); gt.add([v.index],wt,'REPLACE')
print('REWEIGHT_OK')
