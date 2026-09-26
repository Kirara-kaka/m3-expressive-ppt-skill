# Google Material 3 Expressive Presentation Skill (`m3-expressive-ppt`)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Design System](https://img.shields.io/badge/Design%20System-Google%20Material%203%20Expressive-4285F4.svg)](https://m3.material.io/)
[![100% Native Vector](https://img.shields.io/badge/Format-Native%20Editable%20PPTX-0F9D58.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An industrial-grade AI Presentation Generation Skill that creates 100% native, editable `.pptx` slides conforming strictly to Google's official **Material 3 Expressive** design guidelines.

---

## Highlights & Visual Guarantees

* **Google MCU HCT Perception Engine**: Dynamic tonal palettes derived using Google's `materialyoucolor` (`SchemeExpressive`), featuring Primary & Tertiary dual-chroma high-contrast pairings and brand-tinted canvas with ambient halos.
* **Bento Grid & Expressive Geometry**: 28dp extra-large container radii, 9999px full-pill capsules, organic 12-lobed scallop badges, and pure tonal containers replacing dirty black drop shadows.
* **DrawingML Anti-Fallback Typography**: Dual-font declarations (`<a:latin typeface="Segoe UI Variable Display">` + `<a:ea typeface="Noto Sans SC">`) on every text run, completely eliminating fallback to SimSun on Windows.
* **Five Immutable Layout Golden Rules**:
  1. **Middle Vertical Centering**: Mandatory `vertical_anchor = MSO_ANCHOR.MIDDLE` and mathematical center-line alignment for micro-badges.
  2. **Dual-Typeface Stack**: `Segoe UI Variable Display` for headlines/titles, `Noto Sans SC` for body/bullets.
  3. **De-cluttering & Breathing Space**: Zero useless progress bars, concise 1-2 line punchy summaries, generous vertical margins.
  4. **Card-in-Card Symmetry**: Dynamic checklist height derivation guaranteeing identical top/bottom margins, and strict tonal differentiation between nested and parent containers.
  5. **Standardized Archetypes**: 8 pre-engineered, keynote-grade slide archetypes.

---

## The 8 Slide Archetypes

| Archetype ID | Category | Best Used For |
|---|---|---|
| `cover_hero` | 封面主视觉 | 演讲开篇、产品发布、峰会主旨（28dp 巨幅卡片 + 12 叶花瓣徽章） |
| `bento_grid` | 便当盒全景看板 | 架构总览、系统全景、业务分舱（2:1:1 Bento 多舱分舱 + 独立悬浮药丸） |
| `process_roadmap` | 演进路线与里程碑 | 规划周期、阶段推进、实施路线（4 阶段推进 + 14pt 清单直排） |
| `dual_contrast` | 双强调色深度对比 | 传统 vs 新一代、方案比选（分舱包裹 + 高反差深色底座 + 中心 VS 药丸） |
| `kpi_metrics` | 量化成果大屏 | 核心指标、SLA 达标（4 联排大数字 + 趋势胶囊 + 无进度条遮挡） |
| `feature_list` | 三大支柱矩阵 | 产品特性、核心支柱（3 联排竖向支柱卡片 + 高亮主推卡片） |
| `quote_takeaway` | 观点洞察与寄语 | 领袖寄语、设计哲学（巨幅引言高光卡片 + 双引号花瓣徽章） |
| `team_showcase` | 专家团队与人才 | 团队介绍、专家团队（3 联排专家卡片 + 2×2 自适应技能标签网格） |

---

## 4 Curated Expressive Presets

* **`indigo_coral`** (默认旗舰): Deep Indigo (`#315DA8`) + Electric Mint / Coral (`#006C4A`)
* **`electric_mint`** (极客前沿 / 智算云): Deep Teal (`#006C4A`) + Vibrant Berry (`#984061`)
* **`digital_lavender`** (数字未来 / AI 原生): Deep Amethyst (`#6E5676`) + Cyan Glow (`#006874`)
* **`warm_amber`** (商业领袖 / 活力创新): Warm Cognac (`#8C5000`) + Electric Ocean (`#006399`)
* **Custom Hex Seed**: Pass any 6-digit hex color (`#0A66C2`, `#EA4335`, etc.) to dynamically derive a full 20+ token palette.

---

## Quick Start

### 1. Installation
```bash
git clone https://github.com/Kirara-kaka/m3-expressive-ppt-skill.git
cd m3-expressive-ppt-skill
pip install -r requirements.txt
```

### 2. Generate a Deck
```bash
python generate_deck.py --input examples/sample_outline.json --output my_presentation.pptx
```

### 3. Generate and Export 1080P PNGs (Windows)
```powershell
python generate_deck.py --input examples/sample_outline.json --output my_presentation.pptx --export-png
```

---

## AI Agent Integration (Skill)

This repository is designed as a native skill for Google Antigravity and Agentic AI workflows.
See [`.agents/skills/m3-expressive-ppt/SKILL.md`](.agents/skills/m3-expressive-ppt/SKILL.md) for complete instructions, prompt contracts, and JSON schema definitions.

---

## License

MIT License. Feel free to use in commercial and personal projects.
