# Reinforce Eins（TV版）· 设计规格（spec v4）

## 1. 身份与版本
- 角色：Reinforce Eins（リインフォース），《魔法少女リリカルなのはA's》TV 版。
- 不是 Movie 2nd A's 版、不是 Reinforce II、不是 A's PORTABLE 游戏版。
- TV 版特征：头侧羽饰、红瞳无高光、两对（4）黑羽、黑裙金边、白包边、长外套金内衬、无指手套、不对称袜（角色左短右长）、黑色高跟踝鞋（非靴）。
- 姿态：A-pose；附 Idle / WingFlap / FaceDemo / SecondaryFlow 四段 Action。

## 2. 单位与坐标
- 1 Blender Unit = 1 m；unit_settings.scale_length=1；设计尺寸用 mm 记录，脚本内 /1000。
- +Z 上，-Y 前，角色面朝 -Y。

## 3. 尺寸（mm）
| 部位 | 设计值 | 实测/备注 |
|---|---|---|
| 总高 | 1680 | 1680（脚底 0 → 头顶 1680） |
| 头高 | 224 | 224（下巴 1456 → 头顶 1680） |
| 头身比 | 7.5 | 7.5 |
| 肩宽 | 330 | 由身体/袖子外轮廓量 |
| 胸/腰/臀宽 | 300 / 210 / 320 | 设计目标 |
| 头顶/下巴/肩/胸/腰/胯/膝/踝 | 1680/1456/1344/1232/1008/840/448/45 | spec 关键高度 |
| 发梢 | ≈ 950 | 后发到腰 |
| 外套下摆 | 180 | 侧/后片 |
| 右长筒袜口 / 左短袜口 / 鞋口 | 640 / 300 / 195 | 角色右腿长筒袜、左腿短袜；高跟踝鞋 |
| 翼展（tip-to-tip） | 2400 目标 | **实测 2249**（-6.3%，逐根羽片后略收） |
| 总包络（含翼） | — | x ±1124.5 mm，y -182.7..+363.0，z 0..2176.3 |

## 4. 色板（sRGB，脚本内转线性）
| 用途 | hex |
|---|---|
| 皮肤 | #F0D2C1 |
| 头发 | #D7DCE4（渲染调为更银的线性 0.46/0.50/0.57） |
| 裙/外套 | #16171D / #1C1D24 |
| 白包边 | #E8E8EA |
| 金饰 | #D8B24A |
| 外套内衬 | #7A5C1C（深金，减少正面金色面积） |
| 袜 / 鞋 | #0E0F14 / #0B0C10 |
| 翼 / 覆羽 | #14131B / #1B1A24 |
| 虹膜 / 瞳孔 / 睫毛 | #B01F2B / #26080C / #17171A |
| 眼白 / 嘴 | #F7F4F0 / #8A4348 |

## 5. 部件分组（165 个 GEO mesh）
| 组 | 内容 |
|---|---|
| P-Body | GEO-Body、GEO-Arm_L/R、GEO-Leg_L/R |
| P-Head | GEO-Head、GEO-Eye_L/R、GEO-Brow_L/R、GEO-Mouth |
| P-Hair | Hair_Cap、Bang_0..5、Side_L/R_0..1、Back_0..6、Front_L/R、Feather_0..2 |
| P-Dress | Bodice、Collar、PipingCollar/Top、PipingSleeve_L/R、Sleeve_L/R、Skirt、Belt、Belt_Trim×2、Stud×6、TrimX×3、Shoulder_L/R |
| P-Coat | Coat_Back_L/R、Coat_Side_L/R |
| P-Arms | Glove_L/R、Glove_Trim_L/R、Hand_L/R、Finger_L/R_0..3、Thumb_L/R |
| P-Legs | Stocking_Long_R、Sock_Short_L、Shoe_L/R、Shoe_Cuff_L/R、Shoe_CuffGold_L/R、Shoe_Heel_L/R、Shoe_Toe_L/R、Shoe_ToeGold_L/R |
| P-Wings | 每侧上翼 13 主羽 + 6 覆羽、下翼 11 + 5，共 70 根；4 片底膜；共 74 件 |

合计 165 个 mesh，26,280 顶点，51,996 三角面。

## 6. 接口与 allow（装配门）
7 条接口（manifest reports/assembly.json）：Body↔Head、Head↔Hair、Body↔Dress、Body↔Arms、Body↔Legs、Dress↔Coat、Body↔Wings；tol 12 mm（翼根 40 mm）。
- 8 个逻辑子装配组；组级 allow 用 max_depth_mm=120、max_volume_mm3=2e7，覆盖发根、翼根、羽片互叠、眼片、手指、鞋袜、手/肩补片、外套/腰带等设计内交叠。
- 分类见 reports/asm_scan.txt：clash=0、contained=0、float=0、unresolved=0；hidden_ok=711、contact=3、gap=1121。

## 7. 骨架（RIG-Reinforce，83 骨）
- 躯干：root、pelvis、spine_01、spine_02、chest、neck、head。
- 手臂：clavicle/upperarm/forearm/hand ×2。
- 腿：thigh/shin/foot ×2。
- 翼：wing_up_L/R_01..03、wing_low_L/R_01..03。
- 头发：hair_back_01..03、hair_side_L/R_01..02。
- 外套：coat_back_L/R_01..02、coat_side_L/R_01..02。
- 裙：skirt_F/B/L/R。
- 手指：finger_L/R_0..3_01..02、thumb_L/R_01..02（20 骨）。
- 表情：jaw、brow_L、brow_R（3 骨；jaw 主要驱动下巴/嘴，brow 驱动眉）。
- IK 控制（非变形）：CTRL-foot_IK_L/R、CTRL-knee_pole_L/R、CTRL-hand_IK_L/R、CTRL-elbow_pole_L/R（8 骨）。
- IK：腿 shin chain=2，pole angle=-90°；手 forearm chain=2，无 pole（保持 rest 干净）。
- 权重：程序化分区 + 关节 blend；0 未加权顶点；最大 3 影响/顶点；165 个 mesh 全部有 Armature 修改器。

## 8. 动画与二次物理
| Action | 帧 | fps | 内容 |
|---|---|---|---|
| Idle | 1–72 | 24 | 呼吸/头/双臂/翼/后发/外套轻摆 |
| WingFlap | 1–31 | 24 | 翼根 ±28°、羽片跟随、头/发/外套轻摆 |
| FaceDemo | 1–48 | 24 | jaw 开合 + 眉毛抬/压 |
| SecondaryFlow | 1–96 | 24 | 头发/外套/裙的弹簧-阻尼数值积分（非碰撞布料） |

- Idle/WingFlap 默认 Idle 播放；四段 Action 都存 fake user，并各建 NLA track。
- 第 1 帧接近 rest A-pose。
- 指/裙/表情骨可继续手动 K。

## 9. 交付与验收
- Reinforce_Eins_TV.blend、export/*.glb/.fbx/.obj/.mtl、render/**、reports/**、spec.json。
- audit_scene pass；asm_scan pass；asm_gate pass（export_allowed=true）。
- GLB：165 个 GEO mesh、83 骨、4 段 Action。
- 已知偏差：翼展比目标窄 6.3%；逐根羽片是程序化实体叶片；表情只有 jaw/brow；二次物理是弹簧-阻尼非碰撞布料；IK 极限姿态手工调过 8 格；面部/手部仍是风格化简化。

## 10. 设计例外记录
- catalog 没有“角色生成/绑定/表情/物理”op；按 skill §1.6 用 bpy/bmesh 建几何/骨架/动画，验收仍全部走 audit/asm/gate。
- 组级 allow 是“逻辑子装配”的粗粒度声明，不是逐对工艺证书；它保证没有未登记 clash/float。
