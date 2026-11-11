from PIL import Image, ImageDraw
base=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/"
items=[('v5_neutral.png','NEUTRAL'),('v5_blink.png','BLINK'),('v5_surprise.png','SURPRISE'),('v5_squint.png','SQUINT'),('v5_smile.png','SMILE'),('v5_profile.png','3/4 PROFILE')]
cell=(600,640); cols=3; rows=2
canvas=Image.new('RGB',(cell[0]*cols,cell[1]*rows),(24,28,40)); d=ImageDraw.Draw(canvas)
for i,(fn,label) in enumerate(items):
    im=Image.open(base+'render/face/'+fn).convert('RGB'); im.thumbnail((cell[0]-20,cell[1]-50))
    x=(i%cols)*cell[0]+(cell[0]-im.width)//2; y=(i//cols)*cell[1]+10
    canvas.paste(im,(x,y)); d.text(((i%cols)*cell[0]+20,(i//cols)*cell[1]+cell[1]-30),label,fill=(230,230,240))
canvas.save(base+'render/final/expression_sheet_v5.png')
Image.open(base+'render/face/v5_neutral.png').convert('RGB').save(base+'render/final/expression.png')
print('SHEET',canvas.size)
