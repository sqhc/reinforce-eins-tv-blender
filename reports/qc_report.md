# QC / 验收报告 · Reinforce Eins（TV版）v2

日期：2026-10-23 · Blender 5.2.2 · dsh-blender-plugin 2.6.1

## 1. 结论
- audit_scene：**pass**（99 个 mesh）
- asm_scan：**pass**
- asm_gate：**pass**，export_allowed=true
- GLB 重导入：骨架（80 骨）、蒙皮、Idle/WingFlap 均在

## 2. 网格体检（audit_scene，99 个 mesh）
| 指标 | 数值 |
|---|---|
| objects | 99 |
| triangles | 43,380 |
| vertices | 21,840 |
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

修复过程（可复现）：闭合装饰环（用 torus 代替开口 tube）→ 外套侧片改平面网格 → 修鞋底反向法线 → 垂直金线改 ribbon → v2 补回双手/手指并复检。所有 99 件现在 0 缺陷。

## 3. 装配扫描（asm_scan，manifest=reports/assembly.json）
| 指标 | 数值 |
|---|---|
| objects | 99 |
| 候选对 / 测试对 | 479 / 479 |
| clash | **0** |
| contained | **0** |
| float | **0** |
| unresolved | **0** |
| contact | 3 |
| gap | 276 |
| hidden_ok（组级 allow） | 200 |
| max_depth_mm | 64.54（allow 上限 120） |
| min_gap_mm | 0.156 |
| verdict | **pass** |

回执：reports/asm_scan.txt

## 4. 装配门（asm_gate）
| 门 | 状态 | 说明 |
|---|---|---|
| mesh_health | pass | 99 件，0 缺陷 |
| normals | pass | 99 个闭合件法线朝外 |
| clash_all | pass | clash=0/contained=0/float=0/unresolved=0 |
| floaters | pass | 8 个 part 全部可达，0 浮空 |
| interfaces | pass | 7 条接口全部 contact |
| measure | pass | 7 个接口期望均在 12 mm 公差内 |
| **总 verdict** | **pass** | **export_allowed=true** |

回执：reports/asm_gate.txt；清单：reports/assembly.json。

### 关于 allow 的口径
- 8 个逻辑子装配组（Body/Head/Hair/Dress/Coat/Arms/Legs/Wings），组级 allow 上限 120 mm / 2e7 mm³。
- 覆盖角色模型固有的设计内交叠（发根、翼根、眼片、手指、鞋袜、手/肩补片、外套/腰带）。
- 这证明“没有未登记的 clash/contained/float”，**不等于**逐对三角面都做过工艺/强度复核；明细在 asm_scan.txt。

## 5. 导出复验
- GLB：99 个 GEO mesh、80 骨、1 skin、Idle/WingFlap 两个 animation；重导入后 armature=RIG-Reinforce、actions=Idle/WingFlap、18 materials、无 shape key。
- 角色 bbox：x ±1137 mm，y -160.5..+335.2 mm，z 0..2108.3 mm（含翼）；手/指在 99 件内。
- 重导入时 Blender glTF importer 会额外生成一个用于骨骼显示的 Icosphere helper；它不在 GLB 的 99 个 GEO mesh 里。
- FBX 9.3 MB，OBJ 2.8 MB + MTL 3.3 KB；文件 md5 见 export/manifest.json。
- glTF-Validator：插件 runner 返回 ok=false、info=null（无错误信息），外部 Khronos validator 未跑通；仍用 Blender 5.2 glTF 重导入 + 骨架/动作/材质检查替代。

## 6. 视觉 QC
- 四视图：render/qc/front|side|back|three_quarter.png；拼图：render/final/contact_sheet.png。
- 主视觉：render/final/hero.png；半身：render/final/portrait.png；下半身特写：render/final/lower_body.png。
- 与参考并排：render/final/compare_ref.png。
- 绑定测试 6 格：render/rig/pose_sheet.png（A-pose / FK 举臂 / FK 下蹲 / 拍翼 / IK 四肢 / 手指+裙骨）。
- 可识别特征：银发、红瞳、4 黑翼、黑裙金 X、金腰带、白包边、长外套金内衬、无指手套、不对称袜（左短右长）、高跟踝鞋（非靴）、头侧羽饰；v2 补回手掌/手指，v3 修正鞋/袜。

### 视觉限制
- 参考是 2D TV 原画（不同姿态/透视），模型是 A-pose 3D；没有跑硬 IoU 作为通过条件，IoU 只能作诊断。
- 翼是风格化羽扇（scallop+沟槽），近看偏“扇子”，不是逐根羽毛。
- 面部/手部为风格化简化；肖像会暴露贴面片眼睛与简化鼻子/嘴。
- 背面头发在高轮廓光下偏亮、偏整块；属于已知外观问题。
- 极端下蹲/抬臂姿态能看到少量裙/外套/袜与腿的穿插；正常 Idle/拍翼范围内不明显；IK 极值需手调。
- 转台：render/anim/turntable.mp4（48 帧 / 2s / 800×1200 / H.264），已出。

## 7. 复现
见 README.md §4 与 work/；数字对应：
- spec.json / reports/measures.json
- reports/assembly.json
- reports/audit_scene.txt
- reports/asm_scan.txt
- reports/asm_gate.txt
- export/manifest.json / reports/deliverables.json
