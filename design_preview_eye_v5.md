# 眼部系统 v5 · 设计预览与最终实现

## 初始预期（Kimi 版）
- 球面眼 + 眼睑 4 骨 + 视线骨 + 5 个 shapekeys
- 用 torus 做眼睑、删除旧眼、直接建 UV Sphere
- 该方案没有处理眼球与面部的位置/深度、眼睑开口、形态键 Basis，实际运行失败

## 最终实现（v5）
- 2 个椭球眼球（白 sclera）
- 2 个虹膜/瞳孔薄盘（红虹膜 + 黑瞳孔，无高光）
- 4 片眼睑（上/下 × L/R；上眼睑带黑睫毛边）
- 2 片隐藏式眨眼盖（blink morph 到眼前）
- 2 条上睫毛线
- 6 根新骨：Pupil_L/R、Lid_Up_L/R、Lid_Dn_L/R
- 7 个 morph 对象：眼睑 squint/wide_open、眨眼盖 blink、嘴 smile/open

## 结果
- 175 网格 / 33,760 顶点 / 66,916 三角面
- 89 骨；0 未加权；最大 3 影响
- audit/scan/gate 全 pass
- GLB：175 GEO、89 骨、5 Action、7 morph
- 6 格面部测试：render/final/expression_sheet_v5.png

## 诚实限制
- 3D 眼有体积，非原画纯平面。
- blink 用眨眼盖 morph，不是连续眼睑。
- 嘴只有 simple morph，无口腔内部/音素。
- 无眼睑碰撞/眼泪/腮红。

详见 reports/face_v5_report.md。
