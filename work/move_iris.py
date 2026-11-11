import io
p=r"/Users/shenqing/Desktop/Deepseek Harness/Model_test/work/build_face_v5.py"; s=io.open(p,encoding='utf-8').read()
start=s.index("def make_iris("); end=s.index("# mouth shape keys")
block=s[start:end]
s=s[:start]+s[end:]
s=s.replace("for side,sx in (('L',1),('R',-1)):", block+"\nfor side,sx in (('L',1),('R',-1)):")
io.open(p,'w',encoding='utf-8').write(s); print('moved',len(block))
