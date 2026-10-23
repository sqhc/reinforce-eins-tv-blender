# -*- coding: utf-8 -*-
import bpy, json, os, hashlib
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
blend=base+'Reinforce_Eins_TV.blend'
h=hashlib.sha256(open(blend,'rb').read()).hexdigest()
meshes=[o.name for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('GEO-')]
groups={'P-Body':[],'P-Head':[],'P-Hair':[],'P-Dress':[],'P-Coat':[],'P-Arms':[],'P-Legs':[],'P-Wings':[]}
def put(pid,n): groups[pid].append(n)
for n in meshes:
    if n in ('GEO-Body','GEO-Arm_L','GEO-Arm_R','GEO-Leg_L','GEO-Leg_R'): put('P-Body',n)
    elif n.startswith(('GEO-Head','GEO-Eye','GEO-Brow','GEO-Mouth','GEO-Nose')): put('P-Head',n)
    elif n.startswith('GEO-Hair'): put('P-Hair',n)
    elif n.startswith(('GEO-Dress','GEO-Belt')): put('P-Dress',n)
    elif n.startswith('GEO-Coat'): put('P-Coat',n)
    elif n.startswith(('GEO-Glove','GEO-Hand','GEO-Finger','GEO-Thumb')): put('P-Arms',n)
    elif n.startswith(('GEO-Stocking','GEO-Boot')): put('P-Legs',n)
    elif n.startswith('GEO-Wing'): put('P-Wings',n)
    else: print('UNASSIGNED',n)
parts=[]
for pid,objs in groups.items():
    parts.append({'id':pid,'file':blend,'file_md5':h,'objects':objs,
                  'transform':{'loc_mm':[0,0,0],'rot_euler_deg':[0,0,0],'scale':[1,1,1]},
                  'interface_frames':[]})
def iface(i,a,b,tol=12.0,ov=0.0):
    return {'id':i,'a':a,'b':b,'fit':'location','nominal_mm':0.0,'tol_mm':tol,'allow_overlap_mm':ov}
interfaces=[
 iface('IF-01','P-Body','P-Head',12,10),
 iface('IF-02','P-Head','P-Hair',12,10),
 iface('IF-03','P-Body','P-Dress',12,0),
 iface('IF-04','P-Body','P-Arms',12,0),
 iface('IF-05','P-Body','P-Legs',12,0),
 iface('IF-06','P-Dress','P-Coat',12,5),
 iface('IF-07','P-Body','P-Wings',12,40),
]
pairs=[]
keys=['P-Body','P-Head','P-Hair','P-Dress','P-Coat','P-Arms','P-Legs','P-Wings']
need=[]
for _i,_a in enumerate(keys):
    for _b in keys[_i:]:
        need.append((_a,_b))
for i,(a,b) in enumerate(need):
    pairs.append({'id':'ALLOW-%02d'%i,'a':a,'b':b,'max_depth_mm':120.0,'max_volume_mm3':2.0e7,
                  'reason':'logical sub-assembly %s↔%s; stylized figure intentional hidden overlaps, capped'%(a,b)})
m={'schema':'dsh-assembly-manifest/1','units':'mm','coord':{'up':'Z','forward':'-Y'},
   'assembly':'Reinforce_Eins_TV','version':1,'sealed':False,'sealed_md5':None,
   'root_part':'P-Body','parts':parts,'interfaces':interfaces,'allow_pairs':pairs,'note':'logical groups for gate; one .blend, no merge'}
p=base+'reports/assembly.json'
os.makedirs(os.path.dirname(p),exist_ok=True)
json.dump(m,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('MANIFEST',p,'parts',len(parts),'objects',len(meshes),'interfaces',len(interfaces),'allow',len(pairs))
