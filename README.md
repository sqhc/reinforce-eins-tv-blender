# Reinforce Eins（TV版）· DSH × Blender 建模交付（v5：球面眼 / 眼睑 / 视线 / 口型）

这是用 **Blender 5.2.2 + dsh-blender-plugin v3.0.6** 从零制作的《魔法少女リリカルなのはA's》角色 **Reinforce Eins（リインフォース）TV版** 风格化 3D 展示模型。

- v2：补回双手/手指，加腿/手 IK 控制、20 根手指/拇指骨、4 根裙骨。
- v3：黑高跟踝鞋（非靴）+ 角色左短右长不对称袜。
- v4：70 根独立羽毛 + 4 片翼底膜；jaw/brow 表情骨；弹簧-阻尼二次物理；8 格 IK 手调。
- v5：球面眼球 + 虹膜/瞳孔盘 + 4 片眼睑 + 2 片眨眼盖 + 上睫毛线；Pupil_L/R 视线骨 + Lid_Up/Dn_L/R 眼睑骨；blink / squint / wide_open / smile / open 形态键；新增 FaceDemoV5 动作。

> 设计取向：TV 版（头侧羽饰、无高光红瞳、两对黑羽、黑裙金边）。不是 Movie 2nd A's，也不是 Reinforce II。

## 1. 先看什么

| 文件 | 内容 |
|---|---|
| render/final/expression_sheet_v5.png | 6 格面部测试：neutral / blink / surprise / squint / smile / 3/4 |
| render/face/v5_neutral.png 等 | 单张 900×900 面部测试 |
| render/final/expression.png | 中性面部主图（900×900） |
| render/final/portrait.png / hero.png | 半身/主视觉（已更新 v5 眼睛） |
| render/final/contact_sheet.png | 四视图拼图 |
| render/final/lower_body.png | 鞋/不对称袜特写 |
| render/rig/pose_sheet.png | 8 格绑定测试（含 IK 深蹲/过顶） |
| render/anim/turntable.mp4 | 2s 转台 |
| render/anim/secondary.mp4 | 2s 头发/外套/裙二次物理 |
| Reinforce_Eins_TV.blend | 可编辑工程（175 网格、89 骨、5 段 Action、7 个 morph 对象） |
| export/Reinforce_Eins_TV.glb | 175 GEO mesh、89 骨、5 Action、7 个带形态键对象 |
| export/Reinforce_Eins_TV.fbx / .obj / .mtl | FBX / 静态 OBJ |
| spec.json / spec.md | 尺寸、部件、绑定、面部规格 |
| reports/face_v5_report.md | 面部系统实现与测试记录 |
| reports/ | audit / asm_scan / asm_gate 回执、QC、绑定报告、md5 |
| work/ | 可重跑脚本 |

## 2. 打开与使用

1. 用 Blender 5.2.x 打开 Reinforce_Eins_TV.blend。
2. 选中 RIG-Reinforce，进入 Pose Mode。
3. Action Editor：Idle / WingFlap / FaceDemo / FaceDemoV5 / SecondaryFlow。
4. 第 1 帧是接近 rest 的 A-pose；网格都有 Armature 修改器。

### 骨架（89 骨）
- 原有 83 骨：躯干、手臂、腿、翼、头发、外套、裙、手指、jaw、brow_L/R、IK 控制。
- v5 新增：
  - Pupil_L / Pupil_R：视线骨（眼球 + 虹膜盘 100% 权重）
  - Lid_Up_L / Lid_Up_R / Lid_Dn_L / Lid_Dn_R：眼睑骨（上/下眼睑 100% 权重）
- FaceDemoV5 对 jaw/brow/Pupil/Lid 骨做 1–42 帧表情示例。

### 眼睛系统（v5）
- GEO-Eyeball_L/R：椭球眼球（约 48×27×16 mm），白 sclera。
- GEO-Iris_L/R：贴合眼球前表面的虹膜/瞳孔薄盘；红色虹膜 + 黑色瞳孔，无高光（TV 版）。
- GEO-Eyelid_Up/Dn_L/R：4 片贴合眼球的肤色眼睑；上眼睑带黑色睫毛边。
- GEO-BlinkLid_L/R：2 片隐藏式眨眼盖；平时藏在头内，blink 形变到眼前，闭合眼睛。
- GEO-Lash_Up_L/R：上睫毛线。
- 形态键：
  - 眼睑：squint、wide_open
  - 眨眼盖：blink
  - 嘴：smile、open
- 手动调法：
  - 眨眼：GEO-BlinkLid_L/R 的 blink = 1。
  - 眯眼：眼睑的 squint = 1。
  - 睁大：眼睑的 wide_open = 1。
  - 微笑/张口：GEO-Mouth 的 smile / open。
  - 视线：旋转 Pupil_L/R。
  - 眼睑骨：旋转 Lid_Up/Dn_L/R。

### 导出
- GLB/FBX 含 5 段 Action 与 7 个 morph 对象（blink/squint/wide_open/smile/open）。
- OBJ 是静态 A-pose。
- GLB/FBX 不含 IK/驱动器；需要引擎内 IK 时先 Bake。

## 3. 规格与验收

- 身高 1680 mm，头高 224 mm，7.5 头身；翼展约 2249 mm。
- **175 个网格对象，33,760 顶点 / 66,916 三角面；89 骨；0 未加权顶点；每顶点最多 3 影响。**
- 面部：2 眼球 + 2 虹膜盘 + 4 眼睑 + 2 眨眼盖 + 2 睫毛线；6 根新骨；7 个 morph 对象。
- audit_scene：**pass**（175 件；boundary/nonmanifold/degenerate/loose/self-intersections=0；法线 0 朝内）。
- asm_scan：**pass**（175 件 / 1884 候选；clash=0、contained=0、float=0、unresolved=0；716 对组级 allow、contact=5、gap=1163）。
- asm_gate：**pass**，export_allowed=true。
- GLB 重导入：175 GEO mesh、89 骨、5 Action（FaceDemo / FaceDemoV5 / Idle / SecondaryFlow / WingFlap）、7 个 morph 对象。
- 回执在 reports/audit_scene.txt、reports/asm_scan.txt、reports/asm_gate.txt。

> 组级 allow 覆盖发根、翼根、羽片互叠、眼睑/眼球、眼睫毛、鞋袜等设计内交叠；它证明没有未登记 clash/float，不等于逐对三角面工艺复核。

## 4. 复现

环境：Blender 5.2.2、dsh-blender-plugin 3.0.6、macOS。work/ 顺序：

1. build_body.py / build_head.py / build_hair.py
2. build_outfit.py → fix_legwear.py
3. build_hands.py / build_wings.py / build_feathers.py
4. build_rig.py / add_shoulders.py / rig_upgrade.py / reweight.py
5. anim.py
6. add_face.py（jaw/brow）
7. build_face_v5.py（眼球/眼睑/视线骨/形态键）
8. add_face_action.py（FaceDemoV5）
9. add_secondary.py
10. render_final.py / render_poses.py / render_face_v5.py / compose.py / compose_face_v5.py
11. render_turntable.py / render_secondary.py
12. make_manifest.py / export_assets_final.py / write_spec.py / finalize.py

注意：Kimi 提供的 work/improve_face_v5.py 未作为最终实现（其 API/骨架位置/形态键逻辑会失败）；最终实现是 build_face_v5.py。

## 5. 限制（诚实说明）

- 眼睛是风格化 3D 椭球，不是写实解剖眼球；从侧面仍能看到眼球体积，不是原画的纯平面眼。
- blink 用隐藏式眨眼盖形态键实现，不是眼睑皮肤连续变形；眼睑 4 骨存在并有权重，但 FaceDemoV5 主要是示例姿态。
- squint/wide_open 是眼睑片的整体位移，不是精细眼睑肌肉；极端表情仍需手调。
- 嘴只有 smile/open 两个简单形态键，没有牙齿/口腔内部/口型音素；面部无眼睑碰撞/眼泪/腮红。
- GLB 中含 morph 目标，但动画仍以骨骼 Action 为主；形态键动画需在引擎/Blender 中自行 K 帧。
- 头发/外套/裙二次物理是弹簧-阻尼，不是碰撞布料；深蹲仍可能穿插。
- 逐根羽毛是程序化实体叶片，不是羽枝级写实羽毛。
- 外部 glTF-Validator 仍未跑通（插件 runner 返回空 info），使用 Blender glTF 重导入替代。
- 参考图仅个人同人练习；请勿商用或二次分发角色版权素材。

## 6. 角色判定依据

网上资料（アニヲタWiki「リインフォース」）记载：TV 版保留头部羽饰、瞳孔无高光；剧场版去掉头部羽饰并给瞳孔加高光。因此按 TV 版处理：头侧羽饰、无高光红瞳、两对黑羽、黑裙金边、白包边、长外套金内衬、无指手套、不对称袜（角色左短右长）、黑色高跟踝鞋（非靴）。来源：https://w.atwiki.jp/aniwotawiki/pages/27595.html
