# Reinforce Eins（TV版）· 设计规格（spec v5）

## 1. 身份与版本
- 角色：Reinforce Eins（リインフォース），《魔法少女リリカルなのはA's》TV 版。
- 不是 Movie 2nd A's、不是 Reinforce II、不是游戏版。
- TV 版特征：头侧羽饰、红瞳无高光、两对（4）黑羽、黑裙金边、白包边、长外套金内衬、无指手套、不对称袜（角色左短右长）、黑色高跟踝鞋（非靴）。
- 姿态：A-pose；5 段 Action（Idle / WingFlap / FaceDemo / FaceDemoV5 / SecondaryFlow）。

## 2. 单位与坐标
- 1 BU = 1 m；设计尺寸用 mm；+Z 上，-Y 前，角色面朝 -Y。

## 3. 尺寸（mm）
| 部位 | 设计值 | 实测/备注 |
|---|---|---|
| 总高 | 1680 | 1680 |
| 头高 | 224 | 224（下巴 1456 → 头顶 1680） |
| 头身比 | 7.5 | 7.5 |
| 右长筒袜口 / 左短袜口 / 鞋口 | 640 / 300 / 195 | 角色右长左短 |
| 翼展（tip-to-tip） | 2400 目标 | 实测 2249（-6.3%） |
| 总包络 | — | x ±1124.5，y -182.7..+363.0，z 0..2176.3 |

## 4. 色板（sRGB）
| 用途 | hex |
|---|---|
| 皮肤 | #F0D2C1 |
| 头发 | #D7DCE4 |
| 裙/外套 | #16171D / #1C1D24 |
| 白包边 | #E8E8EA |
| 金饰 | #D8B24A |
| 外套内衬 | #7A5C1C |
| 袜 / 鞋 | #0E0F14 / #0B0C10 |
| 翼 / 覆羽 | #14131B / #1B1A24 |
| 虹膜 / 瞳孔 / 睫毛 | #B01F2B / #26080C / #17171A |
| 眼白 / 嘴 | #F7F4F0 / #8A4348 |

## 5. 部件分组（175 个 GEO mesh）
| 组 | 内容 |
|---|---|
| P-Body | Body、Arm_L/R、Leg_L/R |
| P-Head | Head、Eyeball_L/R、Iris_L/R、Eyelid_Up/Dn_L/R、BlinkLid_L/R、Lash_Up_L/R、Brow_L/R、Mouth |
| P-Hair | Hair_Cap、Bang_0..5、Side_L/R_0..1、Back_0..6、Front_L/R、Feather_0..2 |
| P-Dress | Bodice、Collar、Piping、Sleeve_L/R、Skirt、Belt、Studs、TrimX、Shoulder_L/R |
| P-Coat | Coat_Back_L/R、Coat_Side_L/R |
| P-Arms | Glove、Glove_Trim、Hand、Finger_L/R_0..3、Thumb_L/R |
| P-Legs | Stocking_Long_R、Sock_Short_L、Shoe_L/R、Cuff、CuffGold、Heel、Toe、ToeGold |
| P-Wings | 70 根独立羽片 + 4 片底膜 |

合计 175 个 mesh，33,760 顶点，66,916 三角面。

## 6. 面部系统（v5）
- 眼球：2 个椭球 GEO-Eyeball_L/R，约 48×27×16 mm；白 sclera。
- 虹膜/瞳孔：2 个薄盘 GEO-Iris_L/R，贴合眼球前表面；红虹膜 + 黑瞳孔，无高光。
- 眼睑：4 片 GEO-Eyelid_Up/Dn_L/R，贴合眼球；上眼睑带黑睫毛边。
- 眨眼盖：2 片 GEO-BlinkLid_L/R，平时藏在头内，blink 形变到眼前。
- 睫毛线：2 条 GEO-Lash_Up_L/R。
- 新骨（6）：
  - Pupil_L/R：眼球/虹膜 100% 权重，控制视线。
  - Lid_Up_L/R、Lid_Dn_L/R：上/下眼睑 100% 权重。
- 形态键：
  - 眼睑：squint、wide_open
  - 眨眼盖：blink
  - 嘴：smile、open
- 共 7 个带形态键对象；权重点最大 3。

## 7. 骨架（RIG-Reinforce，89 骨）
- 躯干、手臂、腿、翼、头发、外套、裙、手指、jaw/brow、IK 控制同 v4。
- v5 新增 Pupil_L/R、Lid_Up_L/R、Lid_Dn_L/R。
- 权重：0 未加权；最大 3 影响/顶点；所有 175 个 mesh 有 Armature 修改器。

## 8. 动画
| Action | 帧 | fps | 内容 |
|---|---|---|---|
| Idle | 1–72 | 24 | 呼吸/翼/发/外套轻摆 |
| WingFlap | 1–31 | 24 | 翼根 ±28°、羽片跟随 |
| FaceDemo | 1–48 | 24 | jaw 开合 + 眉毛（v4 旧） |
| FaceDemoV5 | 1–42 | 24 | jaw/brow/Pupil/Lid 示例姿态 |
| SecondaryFlow | 1–96 | 24 | 头发/外套/裙弹簧-阻尼 |

- 形态键动画需在引擎/Blender 自行 K 帧；GLB 提供 morph targets。

## 9. 交付与验收
- blend、GLB/FBX/OBJ/MTL、render、reports、spec。
- audit pass（175/66,916/33,760）；asm_scan pass（1884 候选、716 allow）；asm_gate pass。
- GLB：175 GEO mesh、89 骨、5 Action、7 morph 对象。
- 已知限制：3D 眼从侧面仍有体积；blink 为眨眼盖 morph；嘴只有 simple shape keys；无眼睑碰撞；二次物理非碰撞布料；逐根羽片非羽枝级。

## 10. 设计例外
- 面部系统用 bpy/bmesh 直接建；Kimi 的 improve_face_v5.py 未采用（API/骨位/形态键逻辑不成立），最终实现为 build_face_v5.py。
- 组级 allow 是粗粒度声明，不等于逐对工艺证书。
