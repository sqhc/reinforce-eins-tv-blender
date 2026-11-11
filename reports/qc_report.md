# QC / 验收报告 · Reinforce Eins（TV版）v5

日期：2026-11-11 · Blender 5.2.2 · dsh-blender-plugin 3.0.6

## 1. 结论
- audit_scene：**pass**（175 个 mesh，0 缺陷）
- asm_scan：**pass**（175 件 / 1884 候选）
- asm_gate：**pass**，export_allowed=true
- GLB 重导入：175 GEO mesh、89 骨、5 Action、7 个 morph 对象
- 面部：2 眼球 + 2 虹膜盘 + 4 眼睑 + 2 眨眼盖 + 2 睫毛线；6 根新骨；blink/squint/wide_open/smile/open

## 2. 网格体检（audit_scene，175 个 mesh）
| 指标 | 数值 |
|---|---|
| objects | 175 |
| triangles | 66,916 |
| vertices | 33,760 |
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

v5 眼球/虹膜/眨眼盖用封闭实体，避免 v4 之前的 solidify 自交：虹膜盘为前后双面 + 外圈；眨眼盖为前后薄盘；眼睑片单独 solidify。当前 175 件 0 自交。

## 3. 装配扫描（asm_scan，manifest=reports/assembly.json）
| 指标 | 数值 |
|---|---|
| objects | 175 |
| 候选对 / 测试对 | 1884 / 1884 |
| clash | **0** |
| contained | **0** |
| float | **0** |
| unresolved | **0** |
| contact | 5 |
| gap | 1163 |
| hidden_ok（组级 allow） | 716 |
| verdict | **pass** |

回执：reports/asm_scan.txt

## 4. 装配门（asm_gate）
| 门 | 状态 | 说明 |
|---|---|---|
| mesh_health | pass | 175 件，0 缺陷 |
| normals | pass | 175 个闭合件法线朝外 |
| clash_all | pass | clash=0/contained=0/float=0/unresolved=0 |
| floaters | pass | 8 个 part 全部可达 |
| interfaces | pass | 7 条接口全部 contact |
| measure | pass | 7 个接口期望在 12 mm 公差内 |
| **总 verdict** | **pass** | **export_allowed=true** |

回执：reports/asm_gate.txt；清单：reports/assembly.json。

### allow 口径
- 8 个逻辑组；组级 allow max_depth 120 mm / max_volume 2e7。
- 新增眼睑/眼球/虹膜/眨眼盖/睫毛的互叠登记在 P-Head 组内；证明没有未登记 clash/float，不是逐对工艺证书。

## 5. 导出复验
- GLB：175 GEO mesh、89 骨、1 skin、5 段 animation（FaceDemo/FaceDemoV5/Idle/SecondaryFlow/WingFlap）、7 个 morph 对象；重导入后 89 骨、5 Action、7 morph 均在；18 材质。
- 角色 bbox：x ±1124.5 mm，y -182.7..+363.0，z 0..2176.3。
- 重导入时 glTF importer 会额外生成骨骼显示 Icosphere helper；不在 175 GEO mesh 内。
- FBX 19 MB，OBJ 4.3 MB + MTL 3.3 KB；md5 见 export/manifest.json。
- glTF-Validator：插件 runner 返回 ok=false、info=null，外部 validator 未跑通；用 Blender 重导入替代。

## 6. 视觉/面部 QC
- 6 格面部：render/final/expression_sheet_v5.png（neutral / blink / surprise / squint / smile / 3/4 profile）。
- 单张：render/face/v5_*.png；中性主图：render/final/expression.png。
- 四视图/hero/portrait 已用 v5 眼睛重渲；转台/二次物理 MP4 也已重渲。
- 绑定 8 格：render/rig/pose_sheet.png。

### 视觉限制
- 3D 眼从侧面有眼球体积，不是原画纯平面；风格化取舍。
- blink 是隐藏眨眼盖 morph，不是连续眼睑皮肤；4 眼睑骨有权重但示例动作有限。
- squint/wide_open 为眼睑片整体位移；嘴角只有 simple smile/open morph，无口腔内部。
- 极端 IK 姿态仍有少量裙/鞋/袜穿插；二次物理无碰撞。
- 背面头发高光偏整块。

## 7. 复现
见 README.md §4 与 work/；数字对应 spec.json、reports/measures.json、reports/assembly.json、audit/scan/gate 回执、export/manifest.json。
