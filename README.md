# Reinforce Eins（TV版）· DSH × Blender 建模交付（v4：逐根羽毛 / 表情骨 / 二次物理 / IK 手调）

这是用 **Blender 5.2.2 + dsh-blender-plugin v2.6.1** 从零制作的《魔法少女リリカルなのはA's》角色 **Reinforce Eins（リインフォース）TV版** 风格化 3D 展示模型。

- v2：补回双手/手指，加腿/手 IK 控制、20 根手指/拇指骨、4 根裙骨。
- v3：按参考图修正鞋/袜——**黑色高跟踝鞋（不是靴）**，**角色左短右长的不对称袜**。
- v4：**70 根独立羽毛 + 4 片翼底膜**替代整片羽扇；**jaw + brow_L/R 表情骨**；**头发/外套/裙的弹簧-阻尼二次物理**（烘焙到骨骼，可导出）；**8 格 IK/FK 极限姿态手调**。

> 设计取向：TV 版（保留头侧羽饰、红瞳不加高光、两对黑羽、黑裙金边）。不是 Movie 2nd A's 版，也不是 Reinforce II。参考图里的黄底黑连体衣形象判断为游戏/其他版本，只借了腿部/鞋袜比例。

## 1. 先看什么

| 文件 | 内容 |
|---|---|
| render/final/hero.png | 主视觉（1080×1920） |
| render/final/contact_sheet.png | 前/侧/后/3-4 四视图拼图 |
| render/final/compare_ref.png | 与提供的 TV 版参考并排对比 |
| render/rig/pose_sheet.png | 8 格：rest / FK 举臂 / FK 下蹲 / 拍翼 / IK / 手指+裙骨 / IK 深蹲 / IK 过顶 |
| render/final/portrait.png | 半身像 |
| render/final/lower_body.png | 下半身特写（鞋/不对称袜） |
| render/final/expression.png | 表情测试（jaw 张开 + 眉毛抬起） |
| render/anim/turntable.mp4 | 2s 转台（48 帧，800×1200） |
| render/anim/secondary.mp4 | 2s 二次物理演示（头发/外套/裙） |
| render/qc/front.png 等 | 四视图单张 |
| Reinforce_Eins_TV.blend | 可编辑工程（RIG-Reinforce、蒙皮、4 段 Action） |
| export/Reinforce_Eins_TV.glb | 带骨架（83 骨）+ 蒙皮 + Idle/WingFlap/FaceDemo/SecondaryFlow 的 GLB |
| export/Reinforce_Eins_TV.fbx | 带骨架 + 蒙皮 + 动作的 FBX |
| export/Reinforce_Eins_TV.obj / .mtl | 静态 OBJ（A-pose，无骨架） |
| spec.json / spec.md | 尺寸、色板、部件、接口、绑定规格 |
| reports/ | audit / asm_scan / asm_gate 回执、QC 与绑定报告、文件 md5 |
| work/ | 可重跑脚本（spec/lib/build_*/rig/anim/export/render） |

## 2. 打开与使用

1. 用 Blender 5.2.x 打开 Reinforce_Eins_TV.blend。
2. 选中 **RIG-Reinforce**，进入 Pose Mode。
3. 在 Action Editor 切：
   - Idle（1–72 帧，呼吸/发丝/外套/翼微动）
   - WingFlap（1–31 帧，拍翼）
   - FaceDemo（1–48 帧，jaw 开合 + 眉毛）
   - SecondaryFlow（1–96 帧，头发/外套/裙的弹簧-阻尼摆动）
4. 第 1 帧是接近 rest 的 A-pose；模型的 rest pose 也是 A-pose。
5. 动画只驱动骨架；网格都有 Armature 修改器。不要直接移动网格对象。

### 骨架（83 骨）
- 躯干：root → pelvis → spine_01 → spine_02 → chest → neck → head
- 手臂：clavicle_L/R → upperarm_L/R → forearm_L/R → hand_L/R
- 腿：thigh_L/R → shin_L/R → foot_L/R
- 翼：每翼 3 节（wing_up_* / wing_low_*），共 4 翼
- 头发：hair_back_01..03、hair_side_L/R_01..02
- 外套：coat_back_L/R_01..02、coat_side_L/R_01..02
- 裙：skirt_F/B/L/R
- 手指：finger_L/R_0..3_01..02、thumb_L/R_01..02（2 节/指）
- 表情：jaw、brow_L、brow_R
- IK 控制（非变形）：CTRL-foot_IK_L/R + CTRL-knee_pole_L/R、CTRL-hand_IK_L/R + CTRL-elbow_pole_L/R

### 怎么用 IK / 手指 / 裙骨 / 表情
- 腿：选 CTRL-foot_IK_L/R 移动脚掌；膝盖朝向由 CTRL-knee_pole 控制（腿 IK pole angle = -90°，rest 几乎无偏移）。
- 手：选 CTRL-hand_IK_L/R 移动手掌；手 IK 不挂 pole（保持 rest 干净），肘部方向由移动方向决定。
- 手指：选 finger_* / thumb_* 骨旋转；手掌+手指是独立网格，权重到对应骨。
- 裙：旋转 skirt_F/B/L/R 做裙摆；顶部仍由 pelvis 控制。
- 表情：jaw 绕 X 旋转开口/下巴；brow_L/R 抬起/压低眉毛。FaceDemo 是示例 Action。
- 注意：GLB/FBX 不导出 IK 约束；导出的是 deform 骨架与 4 段 Action。要交付 IK 动画，先在 Blender 里烘焙到 deform 骨。

### 逐根羽毛 / 二次物理
- 每侧上翼 13 根主羽 + 6 根覆羽，下翼 11 + 5；共 70 根独立羽片，另有 4 片深色底膜填缝。
- 羽片权重到对应 wing_up/wing_low 三节骨；WingFlap 会带动整组羽片。
- SecondaryFlow 是用弹簧-阻尼模型对 19 根头发/外套/裙骨做数值积分后烘焙的骨骼动画；这是“二次动力学”，不是带碰撞的布料/毛发解算。GLB 能直接播放。

### 导出
- GLB/FBX 包含 Idle / WingFlap / FaceDemo / SecondaryFlow 四段 Action。
- OBJ 是静态 A-pose，供查看/打印前处理；不带动画。

## 3. 规格与验收（结果）

- 身高 **1680 mm**，头高 **224 mm**，**7.5 头身**；翼展约 **2249 mm**（设计目标 2400，实际偏窄 6.3%，见 spec）。
- **165 个网格对象**，**26,280 顶点 / 51,996 三角面**；**83 根骨**；最大每顶点 **3 个骨骼影响**；**0 个未加权顶点**。
- 逐根羽毛：**70 根羽片 + 4 片底膜**。
- audit_scene：**pass**（165 件；boundary/nonmanifold/degenerate/loose/self-intersections=0；法线 0 个朝内）。
- asm_scan：**pass**（165 件；clash=0、contained=0、float=0、unresolved=0；711 对按组级 allow 登记为设计内隐藏交叠）。
- asm_gate：**pass**，export_allowed=true（mesh/normals/clash/floaters/interfaces/measure 全过）。
- GLB 重导入：骨架 RIG-Reinforce（83 骨）、蒙皮、4 段 Action 都在；无 shape key；18 个材质。
- 回执原文在 reports/audit_scene.txt、reports/asm_scan.txt、reports/asm_gate.txt。

> 关于 allow：装配门用 8 个逻辑子装配组（Body/Head/Hair/Dress/Coat/Arms/Legs/Wings）做组级 allow（上限 120 mm / 2e7 mm³），覆盖发根、翼根、羽片互叠、眼片、手指、鞋袜、手/肩补片等设计内交叠。它证明“没有未登记的 clash/contained/float”，**不等于**每一对三角面都经过人工强度/工艺复核。

## 4. 复现

环境：Blender 5.2.2、dsh-blender-plugin 2.6.1、macOS。work/ 下脚本按顺序：

1. build_body.py → 自定义躯干/手臂/腿
2. build_head.py → 头/眼/眉/嘴
3. build_hair.py → 发帽/刘海/长发/头羽
4. build_outfit.py → 裙/袖/领/腰/外套/旧袜靴（随后由 fix_legwear 替换）
4b. fix_legwear.py → 高跟踝鞋 + 左短/右长不对称袜
5. build_hands.py → 手/指
6. build_wings.py → 4 翼（旧羽扇，随后由 build_feathers 替换）
6b. build_feathers.py → 70 根独立羽片 + 4 片底膜
7. build_rig.py → 基础骨架 + 权重
8. add_shoulders.py → 肩部补片
9. rig_upgrade.py → IK 控制 / 手指骨 / 裙骨 / 手权重
10. reweight.py → 袖/手套/袜权重微调
11. anim.py → Idle / WingFlap
12. add_face.py → jaw + brow_L/R + FaceDemo
13. add_secondary.py → SecondaryFlow（弹簧-阻尼烘焙）
14. render_final.py、render_poses.py、compose.py → 渲染与拼图
15. render_turntable.py、render_secondary.py → 两段 MP4
16. make_manifest.py、export_assets_final.py、write_spec.py、finalize.py → 清单/导出/规格

这些是 GUI 会话脚本（blender_rt_do(file=..., auto=False)），不是独立 addon CLI；按顺序重跑即可重建。

## 5. 限制（诚实说明）

- 风格化手办/展示模型，不是照片级 CG，也不是游戏级精修角色。
- 面部：只有 jaw + brow_L/R 三根表情骨；没有眼睑/眨眼、口型、面部 blend shape，眼睛仍是贴面片。
- 二次物理：是弹簧-阻尼骨骼动力学，不是带碰撞/自碰撞的布料或毛发解算；不会处理裙/腿穿插。
- 逐根羽毛：羽片是程序化实体叶片，有独立轮廓和层叠，但不是带羽枝/羽小枝的写实羽毛；整体仍是扇形排列。
- 鞋是风格化高跟踝鞋（尖头、粗跟、踝环），不是精确鞋楦；袜的左短右长按参考图刻意做成不对称。
- IK 已做 8 格极限姿态手调；leg pole angle -90°、手 IK 无 pole 是“保持 rest 干净”的折中，更极端动作仍需手工修正。
- 手指/裙/羽片权重是程序化近似；深蹲/抬臂极值下仍有少量鞋袜/裙/外套穿插。
- 已出转台 MP4 与二次物理 MP4；外部 glTF-Validator 未跑通（插件 runner 返回空 info），用 Blender glTF 重导入替代。
- 参考图为个人同人练习使用；原始 4 张参考图未被修改；请勿商用或二次分发角色版权素材。

## 6. 角色判定依据

网上资料（アニヲタWiki「リインフォース」）记载：TV 版保留头部羽饰、瞳孔无高光；剧场版去掉头部羽饰并给瞳孔加高光。因此按 TV 版处理：头侧羽饰、无高光红瞳、两对黑羽、黑裙金边、白包边、长外套金内衬、无指手套、不对称袜（角色左短右长）、黑色高跟踝鞋（非靴）。来源：https://w.atwiki.jp/aniwotawiki/pages/27595.html
