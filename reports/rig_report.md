# 绑定报告 · RIG-Reinforce（v5）

## 1. 骨架
- 名称：RIG-Reinforce
- 骨数：**89**（v4 的 83 + 6 表情/视线骨）
- rest pose：A-pose
- 175 个 mesh 全部有 Armature 修改器。

### 新增骨
| 骨 | 父级 | 用途 | 权重 |
|---|---|---|---|
| Pupil_L / Pupil_R | head | 视线（眼球/虹膜整体旋转） | Eyeball_L/R + Iris_L/R 100% |
| Lid_Up_L / Lid_Up_R | head | 上眼睑 | Eyelid_Up_L/R 100% |
| Lid_Dn_L / Lid_Dn_R | head | 下眼睑 | Eyelid_Dn_L/R 100% |

原有 jaw、brow_L/R、IK 控制、手指/裙/翼/发/外套骨保留。

## 2. 面部系统与权重
| 对象 | 内容 | 权重 |
|---|---|---|
| GEO-Eyeball_L/R | 椭球眼球，白 sclera | Pupil_L/R |
| GEO-Iris_L/R | 贴合眼球的虹膜/瞳孔薄盘 | Pupil_L/R |
| GEO-Eyelid_Up/Dn_L/R | 4 片肤色眼睑，上眼睑带黑睫毛边 | Lid_Up/Dn_L/R |
| GEO-BlinkLid_L/R | 隐藏式眨眼盖（blink 形变到眼前） | Lid_Up_L/R |
| GEO-Lash_Up_L/R | 上睫毛线 | Lid_Up_L/R |
| GEO-Mouth | 嘴，smile/open 形态键 | jaw + head |

## 3. 蒙皮
| 指标 | 数值 |
|---|---|
| mesh 对象 | 175 |
| 顶点 | 33,760 |
| 未加权顶点 | **0** |
| 每顶点最大影响 | **3** |
| 面部 | 眼球/虹膜 100% Pupil；眼睑 100% Lid；眨眼盖 100% Lid_Up |
| 躯干/衣服/腿/翼/羽片 | 同 v4 程序化分区 |

## 4. 动画与形态键
| Action | 帧 | 内容 |
|---|---|---|
| Idle | 1–72 | 呼吸/翼/发/外套 |
| WingFlap | 1–31 | 拍翼 |
| FaceDemo | 1–48 | v4 jaw/brow |
| FaceDemoV5 | 1–42 | jaw/brow/Pupil/Lid 示例 |
| SecondaryFlow | 1–96 | 弹簧-阻尼二次物理 |

形态键（7 个对象）：
- 眼睑：squint、wide_open
- 眨眼盖：blink
- 嘴：smile、open

注意：GLB 含 morph targets；形态键动画需要在 Blender/引擎中自行 K 帧。FaceDemoV5 主要驱动骨骼，不驱动 morph。

## 5. 测试
- 面部 6 格：render/final/expression_sheet_v5.png。
- blink：眨眼盖 blink=1；眼闭合，黑睫毛边保留。
- squint/wide_open：眼睑片位移；surprise 用 jaw/Pupil/brow 组合。
- 视线：Pupil_L/R 旋转，虹膜盘跟随。
- 8 格全身：render/rig/pose_sheet.png（含 IK 深蹲/过顶）。

## 6. 导出复验
- export/Reinforce_Eins_TV.glb：175 GEO mesh、89 骨、5 Action、7 morph 对象；重导入一致。
- FBX 19 MB；OBJ 4.3 MB 静态 A-pose。
- 不含 IK/驱动器；引擎内 IK 需先 Bake。

## 7. 限制与后续
- 眼睑骨存在并有权重，但 blink 主要靠眨眼盖 morph；连续眼睑皮肤变形尚未做。
- squint/wide_open 是整体位移，不是精细肌肉；无眼睑碰撞/眼泪/腮红。
- 嘴只有 smile/open 两个形态键，无牙齿/口腔内部/音素口型。
- 3D 眼从侧面仍有体积，是风格化取舍。
- 后续可做：真实眼睑权重/形态键、口型音素、blink 动画 Action、二次物理碰撞。
