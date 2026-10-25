# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import os
base = r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"

def sheet(items, out, cell=(500,750), cols=2, bg=(24,28,40)):
    rows=(len(items)+cols-1)//cols
    W=cell[0]*cols; H=cell[1]*rows
    canvas=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(canvas)
    for i,(p,label) in enumerate(items):
        im=Image.open(p).convert('RGB')
        im.thumbnail((cell[0]-20,cell[1]-50))
        x=(i%cols)*cell[0]+(cell[0]-im.width)//2
        y=(i//cols)*cell[1]+10
        canvas.paste(im,(x,y))
        d.text(((i%cols)*cell[0]+20,(i//cols)*cell[1]+cell[1]-30),label,fill=(230,230,240))
    canvas.save(out)
    print('WROTE',out,canvas.size)

sheet([(base+'render/qc/front.png','FRONT'),(base+'render/qc/side.png','SIDE'),
       (base+'render/qc/back.png','BACK'),(base+'render/qc/three_quarter.png','3/4')],
      base+'render/final/contact_sheet.png')
sheet([(base+'render/rig/pose_1_rest.png','REST A-POSE'),(base+'render/rig/pose_2_arms.png','ARMS UP (FK)'),
       (base+'render/rig/pose_3_crouch.png','CROUCH (FK)'),(base+'render/rig/pose_4_flap.png','WING FLAP'),
       (base+'render/rig/pose_5_ik.png','IK ARMS + LEGS'),(base+'render/rig/pose_6_finger_skirt.png','FINGERS + SKIRT'),
       (base+'render/rig/pose_7_ik_crouch.png','IK CROUCH (TUNED)'),(base+'render/rig/pose_8_ik_reach.png','IK REACH (TUNED)')],
      base+'render/rig/pose_sheet.png', cell=(480,620), cols=4)

ref=Image.open(base+'Model_test_ref.png') if os.path.exists(base+'Model_test_ref.png') else Image.open(r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/ca43c8f8d8527eaec30a053605c2027d.jpg")
ren=Image.open(base+'render/qc/front.png')
H=900
ref=ref.convert('RGB'); ref.thumbnail((600,H)); ren=ren.convert('RGB'); ren.thumbnail((700,H))
canvas=Image.new('RGB',(ref.width+ren.width+40,H+50),(24,28,40)); d=ImageDraw.Draw(canvas)
canvas.paste(ref,(10,40)); canvas.paste(ren,(ref.width+30,40))
d.text((10,10),'REFERENCE (TV art)',fill=(230,230,240)); d.text((ref.width+30,10),'3D MODEL (front)',fill=(230,230,240))
canvas.save(base+'render/final/compare_ref.png')
print('WROTE compare',canvas.size)
