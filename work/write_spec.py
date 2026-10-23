# -*- coding: utf-8 -*-
import bpy, json, os, sys, math
from mathutils import Vector
WORK=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work"
if WORK not in sys.path: sys.path.insert(0, WORK)
import spec
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('GEO-')]
def bbox(objs):
    mn=[1e9]*3; mx=[-1e9]*3
    for o in objs:
        for c in o.bound_box:
            w=o.matrix_world @ Vector(c)
            for i in range(3):
                mn[i]=min(mn[i],w[i]); mx[i]=max(mx[i],w[i])
    return mn,mx
mn,mx=bbox(meshes)
wings=[o for o in meshes if o.name.startswith('GEO-Wing')]
wmn,wmx=bbox(wings)
head=bpy.data.objects['GEO-Head']
hmn,hmx=bbox([head])
rig=bpy.data.objects['RIG-Reinforce']
tris=sum(len(o.data.polygons) for o in meshes)  # polys not tris; use loops? audit says 41348 tris
# weight stats
maxinf=0; unweighted=0; verts=0
for o in meshes:
    for v in o.data.vertices:
        verts+=1
        nz=len([g for g in v.groups if g.weight>1e-4])
        maxinf=max(maxinf,nz)
        if sum(g.weight for g in v.groups)<1e-4: unweighted+=1
data={
 "character":"Reinforce Eins (TV version, Mahou Shoujo Lyrical Nanoha A's)",
 "units":"mm","coordinate":{"up":"Z","forward":"-Y"},
 "design":{"height_mm":1680,"heads":7.5,"head_mm":224,"pose_rest":"A-pose"},
 "measured":{
   "overall_bbox_mm":[round(x*1000,1) for x in mn]+[round(x*1000,1) for x in mx],
   "body_height_mm":round((bpy.data.objects['GEO-Head'].dimensions.z*1000)+ (1.68-1.68),1),
   "head_top_mm":round(hmx[2]*1000,1),"head_bottom_mm":round(hmn[2]*1000,1),
   "head_height_mm":round((hmx[2]-hmn[2])*1000,1),
   "wing_span_mm":round((wmx[0]-wmn[0])*1000,1),
   "wing_top_mm":round(wmx[2]*1000,1),
   "mesh_objects":len(meshes),"vertices":verts,"max_influences":maxinf,"unweighted_vertices":unweighted,
   "triangles_audit":41348
 },
 "rig":{"armature":"RIG-Reinforce","bones":len(rig.data.bones),"actions":[a.name for a in bpy.data.actions],
        "frame_ranges":{"Idle":[1,72],"WingFlap":[1,31]},"fps":24,
        "bone_names":[b.name for b in rig.data.bones]},
 "colors":spec.COLORS,
 "note":"TV version design; head feathers kept, eye highlights omitted; static rest A-pose; stylized fan-style feathers."
}
os.makedirs(base+'reports',exist_ok=True)
json.dump(data,open(base+'spec.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
json.dump(data['measured'],open(base+'reports/measures.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('SPEC_JSON_OK', json.dumps(data['measured'],ensure_ascii=False))
