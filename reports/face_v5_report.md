# 面部系统 v5 · 实现与测试报告

日期：2026-11-11 · Blender 5.2.2 · RIG-Reinforce

## 1. 目标
把 v4 的扁平贴面眼升级为：
- 有体积的眼球/虹膜
- 4 根眼睑骨 + 2 根视线骨
- 可眨眼的形态键
- 嘴部 smile/open 形态键

## 2. 最终实现（不是 Kimi 脚本）
Kimi 的 improve_face_v5.py 未采用：它会直接删眼、用 torus 当眼睑、把眼球中心算错、并在没有 Basis 的对象上创建形态键，且 Blender 5.x 的 ops 上下文会失败。

最终实现：work/build_face_v5.py，使用 bpy/bmesh 直接构建封闭实体。

| 对象 | 数量 | 作用 |
|---|---|---|
| GEO-Eyeball_L/R | 2 | 椭球眼球（约 48×27×16 mm），白 sclera |
| GEO-Iris_L/R | 2 | 贴合眼球前表面的虹膜/瞳孔薄盘；无高光 |
| GEO-Eyelid_Up/Dn_L/R | 4 | 肤色眼睑；上眼睑带黑睫毛边 |
| GEO-BlinkLid_L/R | 2 | 隐藏式眨眼盖；blink 形变到眼前 |
| GEO-Lash_Up_L/R | 2 | 上睫毛线 |

新增骨（6）：
- Pupil_L/R：眼球 + 虹膜盘 100%
- Lid_Up_L/R / Lid_Dn_L/R：眼睑 100%

形态键（7 个对象）：
- 眼睑：squint、wide_open
- 眨眼盖：blink
- 嘴：smile、open

## 3. 测试
- 6 格：render/final/expression_sheet_v5.png（neutral / blink / surprise / squint / smile / 3/4）。
- blink：眨眼盖 blink=1，眼闭合，黑睫毛边保留。
- 视线：旋转 Pupil_L/R，虹膜盘跟随。
- squint/wide_open：眼睑片位移。
- 嘴：GEO-Mouth 的 smile/open。
- GLB 重导入：175 GEO mesh、89 骨、5 Action、7 morph 对象。

## 4. 验收
- audit_scene 175 件 pass（0 自交/0 非流形/0 退化）。
- asm_scan 175 件 pass（1884 候选，clash=0/float=0/unresolved=0，716 allow）。
- asm_gate pass，export_allowed=true。

## 5. 限制
- 3D 眼球从侧面仍有体积，不是原画纯平面眼；属于风格化取舍。
- blink 是隐藏眨眼盖 morph，不是连续眼睑皮肤；眼睑 4 骨可以旋转，但还没有连续的皮肤滑动。
- squint/wide_open 是眼睑片整体位移；没有精细眼睑肌肉。
- 嘴只有 smile/open 两个简单 morph；无牙齿/口腔内部/音素口型。
- 无眼睑碰撞、眼泪、腮红。
- GLB 的 morph 动画需要自行 K 帧；当前骨骼 Action 是 FaceDemoV5。

## 6. 复现
- work/build_face_v5.py
- work/add_face_action.py
- work/render_face_v5.py
- work/compose_face_v5.py
