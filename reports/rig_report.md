# 绑定报告 · RIG-Reinforce（v4）

## 1. 骨架
- 名称：RIG-Reinforce
- 骨数：**83**
- rest pose：A-pose
- 165 个 mesh 全部有 Armature 修改器，父级为 RIG-Reinforce。

### 层级（概要）
    root
    └─ pelvis
       ├─ spine_01 → spine_02 → chest
       │              ├─ neck → head
       │              │         ├─ jaw
       │              │         ├─ brow_L / brow_R
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
- 腿：shin_L/R 上 IK 约束，chain_count=2，target=CTRL-foot_IK_*，pole=CTRL-knee_pole_*，pole_angle=-90°。rest 校验约 1 mm。
- 手：forearm_L/R 上 IK 约束，chain_count=2，target=CTRL-hand_IK_*，不挂 pole（避免 rest 偏移）。
- 控制骨 use_deform=False；GLB/FBX **不会导出 IK 约束**，只导出骨架与 Action。要交付 IK 动画，先在 Blender 烘焙到 deform 骨。
- v4 手调了 8 格姿态：IK 四肢、IK 深蹲、IK 过顶；深蹲时用 lower wing 后扫 + 小幅 skirt 旋转避开腿部。

## 3. 蒙皮
| 指标 | 数值 |
|---|---|
| mesh 对象 | 165 |
| 顶点 | 26,280 |
| 未加权顶点 | **0** |
| 每顶点最大影响 | **3** |
| 躯干/衣服 | 按高度在 pelvis/spine/chest/neck 之间线性混合 |
| 手臂/腿 | 距离衰减混合 upperarm/forearm/hand、thigh/shin/foot |
| 袖 | 100% upperarm；肩补片填缝 |
| 手套 | forearm + 腕部 hand 混合 |
| 手掌 | 100% hand；手指/拇指按 2 节骨沿指长混合 |
| 长筒袜（角色右） | shin/thigh 按高度混合；鞋内一段归 foot |
| 短袜（角色左） | foot/shin 分区（短袜在鞋口上方） |
| 鞋 | 鞋体/鞋跟/鞋头/金饰 100% foot；踝环 100% foot |
| 头发 | head + hair_back / hair_side 按高度混合 |
| 外套 | coat_back/side 两节 + pelvis 顶部 |
| 裙 | 顶部 pelvis + 下摆按角度分到 skirt_F/B/L/R |
| 翼/羽片 | 70 根羽片 + 4 片底膜，按距离 wing_up/wing_low 三节骨加权 |
| 面部 | head 主体；jaw 占下前脸/嘴；brow_L/R 占眉 |

## 4. 动画与二次物理
| Action | 帧 | fps | 内容 |
|---|---|---|---|
| Idle | 1–72 | 24 | 呼吸、头微转、双臂微摆、翼/后发/外套轻摆 |
| WingFlap | 1–31 | 24 | 翼根 ±28°、羽片跟随、头/发/外套轻摆 |
| FaceDemo | 1–48 | 24 | jaw 开合 + 眉毛抬/压 |
| SecondaryFlow | 1–96 | 24 | 19 根头发/外套/裙的弹簧-阻尼数值积分 |

- 四段 Action 都存 fake user，并各建同名 NLA track；默认 Idle。
- SecondaryFlow 是物理二次动力学（弹簧-阻尼），不是带碰撞的布料/毛发解算；烘焙成骨骼关键帧，GLB 可播放。
- 第 1 帧接近 rest A-pose。

## 5. 极限姿态测试（render/rig/pose_sheet.png，8 格）
1. REST A-POSE：正常，IK rest 偏差 ≤1 mm。
2. ARMS UP (FK)：袖子跟 upperarm，肩补片填缝。
3. CROUCH (FK)：腿/鞋/袜跟随；裙主要由 pelvis/裙骨控制。
4. WING FLAP：3 节翼骨链 + 逐根羽片跟随。
5. IK ARMS + LEGS：脚不强制离地，手前伸，验证 IK。
6. FINGERS + SKIRT：手指骨弯曲、裙骨小幅摆动。
7. IK CROUCH (TUNED)：pelvis 下压 0.20 m，脚 IK 固定，lower wing 后扫 55°，skirt 小幅让位。
8. IK REACH (TUNED)：双手 IK 上移 0.78 m，左腿前伸，验证肩/肘/膝极限。

## 6. 导出复验
- export/Reinforce_Eins_TV.glb：165 个 GEO mesh、83 骨、1 skin、4 段 Action；重导入后 83 骨与 Idle/WingFlap/FaceDemo/SecondaryFlow 均在。
- export/Reinforce_Eins_TV.fbx：带骨架/蒙皮/动作（16 MB）。
- export/Reinforce_Eins_TV.obj：静态 A-pose，无骨架（查看/打印前处理用）。
- 注意：GLB/FBX 不含 IK 约束；如果引擎里需要 IK 效果，先在 Blender 用 IK 摆姿并 Bake Action 到 deform 骨，再导出。

## 7. 限制与后续
- 面部：只有 jaw + brow_L/R；没有眼睑/眨眼、口型、面部 blend shape；眼睛是独立贴片。
- 二次物理：无碰撞/自碰撞；深蹲/抬臂时裙/外套/腿仍可能穿插，需要手调姿态或后续加碰撞。
- 羽片：程序化实体叶片；可继续加羽枝/羽小枝或做 UV 贴图。
- IK：腿 pole angle=-90°、手无 pole 是 rest 干净的折中；更极端动作需要加 IK 限制/校正骨。
- 手/脚权重是程序化近似；精细抓握/脚趾需要手动 weight paint。
