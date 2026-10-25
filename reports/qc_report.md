# QC / 验收报告 · Reinforce Eins（TV版）v4

日期：2026-10-24 · Blender 5.2.2 · dsh-blender-plugin 2.6.1

## 1. 结论
- audit_scene：**pass**（165 个 mesh）
- asm_scan：**pass**
- asm_gate：**pass**，export_allowed=true
- GLB 重导入：83 骨、蒙皮、4 段 Action 均在
- 逐根羽毛：70 根羽片 + 4 片底膜
- 表情骨：jaw + brow_L/R（FaceDemo 1–48）
- 二次物理：SecondaryFlow 1–96（弹簧-阻尼烘焙）

## 2. 网格体检（audit_scene，165 个 mesh）
| 指标 | 数值 |
|---|---|
| objects | 165 |
| triangles | 51,996 |
| vertices | 26,280 |
| boundary_edges | 0 |
| nonmanifold_edges | 0 |
| degenerate_faces | 0 |
| loose_verts / loose_edges | 0 / 0 |
| self_intersections | 0 |
| normals_inverted | 0 |
| normals_unknown | 0 |
| analysis_incomplete | 0 |
| state | **pass** |

回执：reports/audit_scene.txt

v4 羽毛几何先做薄片 solidify 有 841 个自交；凸包版本有 234 个自交/351 个退化面；最终改为封闭锥形羽片（12 环 × 12 段 + 翻转法线），165 件 0 缺陷。羽片互叠属于 P-Wings 组内 allow，不算单件自交。

## 3. 装配扫描（asm_scan，manifest=reports/assembly.json）
| 指标 | 数值 |
|---|---|
| objects | 165 |
| 候选对 / 测试对 | 1835 / 1835 |
| clash | **0** |
| contained | **0** |
| float | **0** |
| unresolved | **0** |
| contact | 3 |
| gap | 1121 |
| hidden_ok（组级 allow） | 711 |
| verdict | **pass** |

回执：reports/asm_scan.txt

## 4. 装配门（asm_gate）
| 门 | 状态 | 说明 |
|---|---|---|
| mesh_health | pass | 165 件，0 缺陷 |
| normals | pass | 165 个闭合件法线朝外 |
| clash_all | pass | clash=0/contained=0/float=0/unresolved=0 |
| floaters | pass | 8 个 part 全部可达，0 浮空 |
| interfaces | pass | 7 条接口全部 contact |
| measure | pass | 7 个接口期望均在 12 mm 公差内 |
| **总 verdict** | **pass** | **export_allowed=true** |

回执：reports/asm_gate.txt；清单：reports/assembly.json。

### 关于 allow 的口径
- 8 个逻辑子装配组（Body/Head/Hair/Dress/Coat/Arms/Legs/Wings），组级 allow 上限 120 mm / 2e7 mm³。
- 覆盖角色模型固有的设计内交叠（发根、翼根、70 根羽片互叠、底膜、眼片、手指、鞋袜、手/肩补片、外套/腰带）。
- 这证明“没有未登记的 clash/contained/float”，**不等于**逐对三角面都做过工艺/强度复核；明细在 asm_scan.txt。

## 5. 导出复验
- GLB：165 个 GEO mesh、83 骨、1 skin、4 段 animation（Idle/WingFlap/FaceDemo/SecondaryFlow）；重导入后 83 骨与 4 段 Action 均在；18 个材质；无 shape key。
- 角色 bbox：x ±1124.5 mm，y -182.7..+363.0，z 0..2176.3（含翼）。
- 重导入时 Blender glTF importer 会额外生成一个用于骨骼显示的 Icosphere helper；它不在 GLB 的 165 个 GEO mesh 里。
- FBX 16 MB，OBJ 3.4 MB + MTL 3.3 KB；文件 md5 见 export/manifest.json。
- glTF-Validator：插件 runner 返回 ok=false、info=null（无错误信息），外部 Khronos validator 未跑通；用 Blender 5.2 glTF 重导入 + 骨架/动作/材质检查替代。

## 6. 视觉 QC
- 四视图：render/qc/front|side|back|three_quarter.png；拼图：render/final/contact_sheet.png。
- 主视觉：render/final/hero.png；半身：render/final/portrait.png；下半身：render/final/lower_body.png。
- 表情测试：render/final/expression.png（FaceDemo 第 12 帧，jaw 张开 + 眉毛抬起）。
- 绑定测试 8 格：render/rig/pose_sheet.png（rest / FK 举臂 / FK 下蹲 / 拍翼 / IK / 手指+裙骨 / IK 深蹲 / IK 过顶）。
- 转台：render/anim/turntable.mp4（48 帧 / 2s / 800×1200 / H.264）。
- 二次物理：render/anim/secondary.mp4（48 帧 / 2s / 720×900，SecondaryFlow）。
- 可识别特征：银发、红瞳、4 黑翼（逐根羽片）、黑裙金 X、金腰带、白包边、长外套金内衬、无指手套、不对称袜（左短右长）、高跟踝鞋（非靴）、头侧羽饰。

### 视觉限制
- 羽片是程序化实体叶片，有独立轮廓/层叠，但不是写实羽枝/羽小枝；整体仍扇形排列。
- 面部只有 jaw/brow 三根骨，没有眼睑/眨眼、口型、面部 blend shape；眼睛仍是贴面片。
- 二次物理是弹簧-阻尼骨骼动力学，不做碰撞/自碰撞；深蹲时裙/腿穿插仍靠手调姿态规避。
- FK 下蹲/IK 下蹲的脚未强制贴地（pose sheet 无地面），属于测试姿态，不是最终动画。
- 极端姿态仍有少量裙/外套/袜穿插；正常 Idle/拍翼范围内不明显。
- 背面头发在高轮廓光下偏亮、偏整块。

## 7. 复现
见 README.md §4 与 work/；数字对应：
- spec.json / reports/measures.json
- reports/assembly.json
- reports/audit_scene.txt
- reports/asm_scan.txt
- reports/asm_gate.txt
- export/manifest.json / reports/deliverables.json
