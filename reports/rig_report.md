# 绑定报告 · RIG-Reinforce（v2）

v3 修正：鞋改为黑色高跟踝鞋（尖头、粗跟、踝环、金色装饰），不是靴；袜按参考做成角色左短右长的不对称。

## 1. 骨架
- 名称：RIG-Reinforce
- 骨数：**80**
- rest pose：A-pose
- 99 个 mesh 全部有 Armature 修改器，父级为 RIG-Reinforce。

### 层级（概要）
    root
    └─ pelvis
       ├─ spine_01 → spine_02 → chest
       │              ├─ neck → head
       │              │         ├─ hair_back_01 → 02 → 03
       │              │         └─ hair_side_L/R_01 → 02
       │              ├─ clavicle_L → upperarm_L → forearm_L → hand_L
       │              ├─ clavicle_R → upperarm_R → forearm_R → hand_R
       │              │         └─ finger_L/R_0..3_01 → 02；thumb_L/R_01 → 02
       │              ├─ wing_up_L/R_01 → 02 → 03
       │              └─ wing_low_L/R_01 → 02 → 03
       ├─ thigh_L → shin_L → foot_L
       ├─ thigh_R → shin_R → foot_R
       ├─ coat_back_L/R_01 → 02、coat_side_L/R_01 → 02
       └─ skirt_F/B/L/R

    控制骨（非变形，父级 root）：
    CTRL-foot_IK_L/R、CTRL-knee_pole_L/R、CTRL-hand_IK_L/R、CTRL-elbow_pole_L/R

## 2. IK
- 腿：shin_L/R 上 IK 约束，chain_count=2，target=CTRL-foot_IK_*，pole=CTRL-knee_pole_*，pole_angle=-90°。rest 校验：foot tail (0.0741,-0.14,0.02) vs rest (0.075,-0.14,0.02)，约 1 mm。
- 手：forearm_L/R 上 IK 约束，chain_count=2，target=CTRL-hand_IK_*，不挂 pole（避免 rest 偏移）。rest：hand tail 与 rest 一致。
- 控制骨 use_deform=False；GLB/FBX **不会导出 IK 约束**，只导出骨架与当前 FK Action。要交付 IK 动画，先在 Blender 烘焙到 deform 骨。
- 用法：移动 CTRL-foot_IK / CTRL-hand_IK 即可；膝盖朝向由 knee_pole 控制。

## 3. 蒙皮
| 指标 | 数值 |
|---|---|
| mesh 对象 | 99 |
| 顶点 | 21,840 |
| 未加权顶点 | **0** |
| 每顶点最大影响 | **3** |
| 躯干/衣服 | 按高度在 pelvis/spine/chest/neck 之间线性混合 |
| 手臂/腿 | 距离衰减混合 upperarm/forearm/hand、thigh/shin/foot |
| 袖 | 100% upperarm（v2 修正，抬臂时袖子跟随；肩补片填缝） |
| 手套 | forearm + 腕部 hand 混合 |
| 手掌 | 100% hand；手指/拇指按 2 节骨沿指长混合 |
| 长筒袜（角色右） | shin/thigh 按高度混合；鞋内一段归 foot |
| 短袜（角色左） | foot/shin 分区（短袜在鞋口上方） |
| 鞋 | 鞋体/鞋跟/鞋头/金饰 100% foot；踝环 100% foot |
| 头发 | head + hair_back / hair_side 按高度混合 |
| 外套 | coat_back/side 两节 + pelvis 顶部 |
| 裙 | 顶部 pelvis + 下摆按角度分到 skirt_F/B/L/R |
| 翼 | 每翼 3 骨按距翼根距离加权 |

## 4. 动画
| Action | 帧 | fps | 内容 |
|---|---|---|---|
| Idle | 1–72 | 24 | 呼吸（spine/chest）、头微转、双臂微摆、翼/后发/外套轻摆 |
| WingFlap | 1–31 | 24 | 翼根 ±28°、翼中段次级、头/发/外套跟随、轻微上下浮动 |

- 两个 Action 都存 fake user，并建了同名 NLA track；默认 Idle 播放。
- 第 1 帧接近 rest A-pose。
- 手指/裙骨目前没有动画关键帧，是给后续手部/裙摆动画用的可动骨。

## 5. 极限姿态测试（render/rig/pose_sheet.png，6 格）
1. REST A-POSE：正常，IK rest 偏差 ≤1 mm。
2. ARMS UP (FK)：袖子已改为 100% upperarm，跟随抬臂；肩补片填住肩缝。
3. CROUCH (FK)：腿/鞋/袜跟随；裙主要由 pelvis/裙骨控制，深蹲时仍有少量穿插。
4. WING FLAP：3 节翼骨链正常，覆羽跟随。
5. IK ARMS + LEGS：移动 CTRL-hand_IK / CTRL-foot_IK 后可摆出抬臂+屈腿姿态；极值下膝部袜/鞋有少量皮肤露出。
6. FINGERS + SKIRT：手指骨弯曲、裙骨摆动可见；程序化权重在极值时略硬。

## 6. 导出复验
- export/Reinforce_Eins_TV.glb：99 个 GEO mesh、80 骨、1 skin、Idle/WingFlap；重导入后 80 骨与两段 Action 均在。
- export/Reinforce_Eins_TV.fbx：带骨架/蒙皮/动作（9.0 MB）。
- export/Reinforce_Eins_TV.obj：静态 A-pose，无骨架（查看/打印前处理用）。
- 注意：GLB/FBX 不含 IK 约束；如果引擎里需要 IK 效果，先在 Blender 用 IK 摆姿并 Bake Action 到 deform 骨，再导出。

## 7. 限制与后续
- 面部：无 jaw/表情骨/形态键；眼睛/眉/嘴是独立网格。
- IK：腿 pole angle=-90° 是“rest 干净”的折中；手 IK 无 pole，肘部方向由目标位置决定；极值动作建议手调。
- 手指/裙骨权重是程序化近似；精细抓握/裙摆需要手动 weight paint。
- 翼是风格化羽扇，不是逐根羽毛；如需逐根羽毛，需要重建翼几何并重分配翼骨权重。
- 外套/头发/翼是骨链驱动，没有布料/毛发物理。
