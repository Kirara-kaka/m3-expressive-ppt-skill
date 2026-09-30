# HANDOVER.md — M3 Expressive PPT Skill 交接文档

> **文档版本**: v1.0
> **最后更新**: 2026-09-30
> **代码版本**: `ffbbb52` (main)
> **仓库**: [Kirara-kaka/m3-expressive-ppt-skill](https://github.com/Kirara-kaka/m3-expressive-ppt-skill)

---

## 一、系统概览

### 定位

一个工业级 AI 演示文稿生成引擎，生成 100% 原生可编辑的 `.pptx` 幻灯片，严格遵循 Google 官方 **Material 3 Expressive** 设计规范。

### 五层架构

```
CLI (generate_deck.py)
  → Pipeline (planner.py → schema.py → builder.py)
    → Archetypes (8 个版式渲染器, archetypes/*.py)
      → Engine (components.py, geometry.py, typography.py)
        → Core (tokens.py MCU色彩, icon_manager.py 矢量图标, shapes_tokens.py)
```

### 关键文件索引

| 路径 | 说明 |
|---|---|
| `generate_deck.py` | CLI 入口：JSON 大纲 → PPTX |
| `export_slide.ps1` | PowerPoint COM 自动化 PNG 导出 |
| `core/tokens.py` | MCU HCT 色彩引擎，5 预制 + 自定义种子，Light/Dark 双模式 |
| `engine/components.py` | M3 组件库：卡片、药丸、清单、Hero 指标、光晕、Bento 网格 |
| `engine/typography.py` | DrawingML 双字族排版 + 光学中轴对齐 |
| `engine/geometry.py` | 28dp 圆角、9999px 胶囊、有机花瓣造型 |
| `pipeline/planner.py` | 版式自动推断 + 内容标准化 |
| `pipeline/builder.py` | 版式分发 + PPTX 编译输出 |
| `pipeline/schema.py` | 数据模型 (DeckConfig / SlidePlan / DeckPlan) |
| `archetypes/*.py` | 8 个版式渲染器的具体实现 |
| `.agents/skills/m3-expressive-ppt/SKILL.md` | AI Agent Skill 规范（五大黄金律 + JSON Schema） |
| `tests/dark_mode_showcase.json` | 暗色模式 8 版式回归测试大纲 |

### 运行环境

- **Python**: 3.10+ （开发环境 `E:\Python\python.exe` Python 3.14.0）
- **依赖**: python-pptx ≥1.0.2, materialyoucolor ≥3.0.4, Pillow ≥12, resvg-py ≥0.5, requests ≥2.32
- **PNG 导出**: 需要 Windows + PowerPoint COM 自动化

---

## 二、已完成任务清单

### 评审 #1：Skill 全面深度评估（2026-09-27）

对 Skill 进行了三维评估，**总评分 88/100**：

| 维度 | 评分 | 核心结论 |
|---|---|---|
| **完整性** | 90/100 | 8 版式全覆盖、5 预制主题 + 自定义种子、完整矢量图标管线 |
| **规范性** | 85/100 | 五大黄金律严格合规，但布局参数散布硬编码、类型标注不完整 |
| **M3 还原性** | 89/100 | 色彩 100% 正品 MCU 算法、28dp/9999px 精确、零脏黑阴影 |

评估方法：
- 源码逐文件审查（5 层架构全部覆盖）
- 8 页 showcase + warm_amber 主题 PNG 逐页视觉检查
- 对照 Google M3 Expressive 官方规范逐项对比

### 评审 #2：暗色模式端到端验证（2026-09-27 ~ 28）

**验证结论：✅ 通过**

- 生成了完整的 8 版式暗色 showcase (`indigo_coral` × Dark)
- WCAG 对比度精确计算 — 8 项关键文字/背景组合全部 PASS，最低 7.2:1（达 AAA 级）
- Surface Container 五级色阶验证 — luminance 严格单调递增 (Tone 4→22)
- 亮色模式回归 — warm_amber 4 页无回归

### Bug 修复 #1：Token 完整性（2026-09-28 已提交推送）

**提交**: `ffbbb52` `fix(tokens): add missing inverse/error color roles and electric_violet preset`

修改文件与内容：

| 文件 | 修改 |
|---|---|
| `core/tokens.py` | Light/Dark 两个分支各新增 7 个 M3 色彩角色：`inverse_surface` (Light Tone 20 / Dark Tone 90)、`inverse_on_surface` (Light Tone 95 / Dark Tone 20)、`inverse_primary` (Light Tone 80 / Dark Tone 40)、`error` (Light Tone 40 / Dark Tone 80)、`on_error` (Light Tone 100 / Dark Tone 20)、`error_container` (Light Tone 90 / Dark Tone 30)、`on_error_container` (Light Tone 10 / Dark Tone 90) |
| `pipeline/schema.py` | `VALID_THEME_PRESETS` 列表补齐 `"electric_violet"`，与 `tokens.py` 中的 `PRESET_THEMES`（5 个）保持一致 |
| `tests/dark_mode_showcase.json` | 新增 8 版式暗色回归测试大纲，可作为永久回归测试用例 |

---

## 三、系统当前状态

### 功能矩阵

| 功能 | 状态 | 备注 |
|---|---|---|
| 8 大版式渲染 | ✅ 生产就绪 | cover_hero / bento_grid / process_roadmap / dual_contrast / kpi_metrics / feature_list / quote_takeaway / team_showcase |
| 5 预制主题 | ✅ 生产就绪 | indigo_coral / electric_mint / digital_lavender / warm_amber / electric_violet |
| 自定义 Hex 种子色 | ✅ 生产就绪 | 任意 `#RRGGBB` |
| Light 模式 | ✅ 已验证 | 多主题视觉样例已确认 |
| Dark 模式 | ✅ 已验证 | indigo_coral × Dark 全 8 版式已通过 |
| 矢量图标管线 | ✅ 生产就绪 | Google Material Symbols CDN → resvg 着色 → PNG 缓存 |
| DrawingML 双字族排版 | ✅ 生产就绪 | 彻底杜绝 SimSun 回退 |
| PNG 导出 | ✅ 仅限 Windows | 依赖 PowerPoint COM |
| Slide 数量限制 | ❌ 无限制 | 版式可重复使用，页码自动编号 |

### 主题 × 模式交叉验证状态

| 主题 | Light | Dark |
|---|---|---|
| `indigo_coral` | ✅ | ✅ |
| `electric_mint` | ✅ | ⬜ 未验证 |
| `digital_lavender` | ✅ | ⬜ 未验证 |
| `warm_amber` | ✅ | ⬜ 未验证 |
| `electric_violet` | ✅ | ⬜ 未验证 |

### Git 提交历史

```
ffbbb52  fix(tokens): add missing inverse/error color roles and electric_violet preset  ← 本轮修复
38d8f74  feat(layout): implement M3 Expressive constrained asymmetry & grid system
4965b28  test: add centerline and shadow alignment visual regression test scripts
3694052  fix(alignment): remove default PPT drop shadow and implement optical centerline formula
cab24d4  fix(engine): optical vertical alignment for micro-badges and high-contrast text
7696262  feat: add electric_violet preset to theme engine and SKILL.md
54f7c60  feat: initial release of Google Material 3 Expressive Presentation Skill
```

---

## 四、待优化事项 (按优先级)

### 🔴 高优先级

| # | 事项 | 说明 | 涉及文件 |
|---|---|---|---|
| 1 | **JSON 输入校验层** | 目前错误字段名（如 `arcetype` 拼写错误）不会报错，静默 fallback 到 `bento_grid`。应使用 `jsonschema` 或 Pydantic 前置校验，给出明确错误提示 | `pipeline/planner.py`, 新增 `pipeline/validator.py` |
| 2 | **布局常量统一管理** | 8 个渲染器中散布大量硬编码 `Inches(0.52)`, `Inches(0.28)` 等，应提取为统一常量模块 | 全部 `archetypes/*.py`, 新增 `engine/layout_tokens.py` |
| 3 | **feature_list 子卡片高度自适应** | 嵌套子卡片高度硬编码为 `1.24"`，长文本会被裁切。应根据 bullet point 数量动态计算 | `archetypes/feature_list.py` |

### 🟡 中优先级

| # | 事项 | 说明 | 涉及文件 |
|---|---|---|---|
| 4 | **4 款主题暗色交叉验证** | 仅验证了 `indigo_coral` 暗色，其余 4 款主题暗色模式尚未渲染测试 | `tests/` |
| 5 | **有机造型库扩展** | 目前仅实现 scallop/flower 1-2 种有机造型，M3 官方有 35 款（4-leaf clover, burst, gem 等） | `engine/geometry.py`, `core/shapes_tokens.py` |
| 6 | **字重梯度细化** | 目前只用 Bold (700) + Regular (400) 两档，M3 Emphasized 规范还需 Medium (500) / SemiBold (600) | `engine/typography.py` |
| 7 | **pytest 自动化测试** | `tests/` 目录下只有手写脚本，无 pytest 框架、无 CI 配置、无覆盖率报告 | `tests/`, 新增 `pytest.ini` / `conftest.py` |
| 8 | **暗色光晕透明度调优** | `_create_ambient_bloom_png` 的 alpha 上限 18% 在暗色背景上几乎不可见，暗色模式下可提升至 25-30% | `engine/components.py` |

### 🟢 低优先级 / 增强项

| # | 事项 | 说明 |
|---|---|---|
| 9 | **演讲者备注自动生成** | 基于 slide 内容填充 PowerPoint Notes 区域 |
| 10 | **Morph 转场动画** | PowerPoint 支持 Morph Transition，可为相邻页面添加微妙变形过渡 |
| 11 | **新增版式类型** | 如"纯图片展示页"、"数据表格页"、"时间线页"等新的 archetype |
| 12 | **CI/CD 集成** | GitHub Actions 自动运行测试 + 渲染 showcase + 发布 Release |
| 13 | **CHANGELOG 版本记录** | 维护正式版本号和变更日志 |
| 14 | **中文字符宽度精确测量** | 当前按 `0.155"` 估算，可引入 `Pillow.ImageFont.getbbox()` 精确测量 |

---

## 五、已知技术要点与注意事项

### 关键设计决策

1. **色彩算法是 100% 正品 Google MCU** — 直接调用 `materialyoucolor` 库的 `SchemeExpressive` 类，不是近似模拟
2. **零阴影设计** — `remove_shape_shadow()` 强制 `effectRef idx="0"`，层级完全通过 Surface Container 色阶梯度表达
3. **DrawingML XML 直操** — 双字族排版、阴影清理、圆角几何均通过 `lxml` 直接操作 DrawingML XML，非 python-pptx 高层 API
4. **花瓣徽章是 SVG→PNG** — 有机造型在 Python 中用数学公式生成 SVG 路径，resvg 渲染为 PNG 后插入 PPTX

### 踩坑记录

| 坑 | 说明 |
|---|---|
| PowerShell 字符串转义 | 内联 Python `-c` 命令中的花括号和引号会被 PowerShell 吃掉，必须用脚本文件 |
| `export_slide.ps1` 参数顺序 | 需用命名参数 `-PptxPath` `-OutputDir`，位置参数第二个会绑定到 `$PngPath` 而非 `$OutputDir` |
| `theme.hex()` fallback | 缺失的 Token 静默返回 `#000000` 而非报错，已补齐 inverse/error 系列 |
| GBK 编码 | Windows 终端默认 GBK，Python 脚本中不能直接 print Unicode emoji（✅❌等） |
| `sys.path` 问题 | 从 `scratch/` 或 `tests/` 子目录运行脚本时需手动 `sys.path.insert(0, ...)` |

---

## 六、测试与验证指南

### 快速冒烟测试

```bash
# 亮色模式 — 全 8 版式
python generate_deck.py --input examples/sample_outline.json --output test_light.pptx

# 暗色模式 — 全 8 版式
python generate_deck.py --input tests/dark_mode_showcase.json --output test_dark.pptx
```

### PNG 导出（仅 Windows）

```powershell
powershell -ExecutionPolicy Bypass -File export_slide.ps1 -PptxPath test_dark.pptx -OutputDir test_slides
```

### 色阶验证脚本

```bash
python scratch/verify_dark_tokens.py
```

输出 Light/Dark 全量 Token 对照表 + WCAG 对比度计算 + Surface 色阶 luminance 验证。
