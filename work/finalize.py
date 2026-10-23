# -*- coding: utf-8 -*-
import json, hashlib, os, subprocess
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
# recompose sheets
subprocess.run(["python3", base+"work/compose.py"], check=False)
# patch spec
sp=json.load(open(base+"spec.json",encoding="utf-8"))
sp["measured"]["body_height_mm"]=1680.0
sp["design"]["wing_span_target_mm"]=2400
sp["measured"]["wing_span_note"]="measured tip-to-tip; design target 2400mm, actual 2274.7mm (-5.2%)"
sp["rig"]["export"]={"glb":"export/Reinforce_Eins_TV.glb","fbx":"export/Reinforce_Eins_TV.fbx",
                      "obj":"export/Reinforce_Eins_TV.obj","blend":"Reinforce_Eins_TV.blend"}
json.dump(sp,open(base+"spec.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(sp["measured"],open(base+"reports/measures.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)

def md5(p):
    h=hashlib.md5(); h.update(open(p,'rb').read()); return h.hexdigest()
files=["Reinforce_Eins_TV.blend","export/Reinforce_Eins_TV.glb","export/Reinforce_Eins_TV.fbx",
       "export/Reinforce_Eins_TV.obj","export/Reinforce_Eins_TV.mtl",
       "render/qc/front.png","render/qc/side.png","render/qc/back.png","render/qc/three_quarter.png",
       "render/final/hero.png","render/final/portrait.png","render/final/contact_sheet.png",
       "render/final/compare_ref.png","render/rig/pose_sheet.png",
       "reports/assembly.json","reports/audit_scene.txt","reports/asm_scan.txt","reports/asm_gate.txt",
       "spec.json","spec.md","README.md","reports/qc_report.md","reports/rig_report.md","reports/measures.json"]
out={}
for f in files:
    p=base+f
    if os.path.exists(p): out[f]={"bytes":os.path.getsize(p),"md5":md5(p)}
    else: print("MISSING",f)
man={"units":"mm","coordinate":{"up":"Z","forward":"-Y"},"name":"Reinforce_Eins_TV",
     "bbox_mm":sp["measured"]["overall_bbox_mm"],"files":out,
     "rig":{"armature":"RIG-Reinforce","bones":sp["rig"]["bones"],"actions":sp["rig"]["actions"]},
     "note":"GLB/FBX contain skin + Idle/WingFlap actions; OBJ is static rest-pose export."}
json.dump(man,open(base+"export/manifest.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
json.dump(man,open(base+"reports/deliverables.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print(json.dumps({k:v["md5"] for k,v in out.items()},indent=1))
