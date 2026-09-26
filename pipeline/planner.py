"""
Intelligent Planner and Archetype Mapper for M3 Expressive presentation generation.
Translates structured outlines into fully populated DeckPlans with optimal Archetype selection.
"""

from typing import Dict, Any, List, Optional
import re
from pipeline.schema import DeckConfig, SlidePlan, DeckPlan, VALID_ARCHETYPES

# Keyword triggers for archetype detection
ARCHETYPE_TRIGGERS = {
    "cover_hero": [
        "封面", "cover", "title", "intro", "发布", "演讲", "主讲", "主题", "开篇"
    ],
    "process_roadmap": [
        "路线图", "里程碑", "阶段", "规划", "演进", "roadmap", "timeline", "process", 
        "phase", "milestone", "schedule", "步骤", "推进"
    ],
    "dual_contrast": [
        "对比", "比对", "对照", "versus", "vs", "comparison", "传统 vs", "方案对比",
        "优劣", "升级前后", "差异"
    ],
    "kpi_metrics": [
        "指标", "数据", "量化", "成果", "kpi", "metrics", "benchmark", "performance",
        "大屏", "增长率", "时延", "转化率", "sla", "数据看板"
    ],
    "feature_list": [
        "特性", "支柱", "核心功能", "能力矩阵", "pillar", "features", "capabilities",
        "三大", "四大支柱", "功能特性", "核心支柱"
    ],
    "quote_takeaway": [
        "观点", "哲学", "引言", "结语", "金句", "总结", "寄语", "quote", "takeaway",
        "philosophy", "vision", "愿景", "核心洞察"
    ],
    "team_showcase": [
        "团队", "成员", "人物", "组织", "专家", "顾问", "team", "people", "members",
        "architects", "leadership", "人才"
    ],
    "bento_grid": [
        "全景", "概览", "架构", "看板", "总览", "overview", "dashboard", "bento",
        "architecture", "系统", "全貌", "便当盒"
    ]
}

class PlanMapper:
    """Classifies content and maps to best M3 Archetype."""

    @staticmethod
    def infer_archetype(slide_data: Dict[str, Any], page_index: int = 1, total_pages: int = 1) -> str:
        # Explicit archetype override takes precedence
        if "archetype" in slide_data and slide_data["archetype"] in VALID_ARCHETYPES:
            return slide_data["archetype"]
        if "layout" in slide_data and slide_data["layout"] in VALID_ARCHETYPES:
            return slide_data["layout"]

        # First slide defaults to cover_hero
        if page_index == 1:
            return "cover_hero"

        # Check structural signatures
        content = slide_data.get("content", slide_data)
        if "phases" in content or "roadmap" in content:
            return "process_roadmap"
        if "left_plan" in content or "right_plan" in content or "left" in content:
            return "dual_contrast"
        if "metrics" in content or "kpis" in content:
            return "kpi_metrics"
        if "features" in content or "pillars" in content:
            if "quote_text" in content:
                return "quote_takeaway"
            return "feature_list"
        if "quote_text" in content or "quote" in content:
            return "quote_takeaway"
        if "members" in content or "team" in content:
            return "team_showcase"
        if "hero_card" in content or "bento" in content:
            return "bento_grid"

        # Text matching on title, category, subtitle
        search_corpus = " ".join([
            str(slide_data.get("title", "")),
            str(slide_data.get("subtitle", "")),
            str(slide_data.get("category", "")),
            str(content.get("title", "")),
            str(content.get("category", ""))
        ]).lower()

        for arch, keywords in ARCHETYPE_TRIGGERS.items():
            for kw in keywords:
                if kw in search_corpus:
                    return arch

        # Fallback default
        return "bento_grid"

    @staticmethod
    def normalize_slide_content(archetype: str, raw_content: Dict[str, Any], page_num: int, total_pages: int) -> Dict[str, Any]:
        """Ensures all archetype-specific slots exist with reasonable fallbacks and clean formatting."""
        data = dict(raw_content)

        # Standard footers and headers
        page_str = f"Page {page_num:02d} / {total_pages:02d}"
        if "footer_right" not in data:
            data["footer_right"] = page_str
        if "footer_left" not in data:
            data["footer_left"] = f"Material 3 Expressive Deck · {archetype.replace('_', ' ').title()}"

        if "category" not in data:
            data["category"] = "SYSTEM ARCHITECTURE"
        if "title" not in data:
            data["title"] = f"Slide Title {page_num}"
        if "subtitle" not in data:
            data["subtitle"] = "Material 3 Expressive presentation modular design system."

        # Archetype specific defaults
        if archetype == "cover_hero":
            data.setdefault("speaker", "主讲人 · 架构专家")
            data.setdefault("date", "2026 年秋季发布")
            data.setdefault("org", "Google Technology Group")
            data.setdefault("hero_highlight", "M3 EXP")
            data.setdefault("hero_badge_text", "全场景演示系统")

        elif archetype == "bento_grid":
            if "hero_card" not in data:
                data["hero_card"] = {
                    "chip": "CORE PILLAR", "icon": "auto_awesome",
                    "title": "动态感知色彩与双强调色", "subtitle": "Dual-Chroma Dynamic Palette",
                    "desc": "基于 Google MCU 算法推导和谐高对比度的色彩体系。",
                    "metric_val": "86.4%", "metric_label": "核心转化率", "trend": "+3.4x 跃迁"
                }
            if "card_top" not in data:
                data["card_top"] = {
                    "icon": "grid_view", "title": "BentoGrid 空间算子",
                    "desc": "卡片内外边距严格依循 16/24/28dp 黄金律。",
                    "chips": ["28dp 容器", "9999px 胶囊", "色调浸润底色"]
                }
            if "card_bot_left" not in data:
                data["card_bot_left"] = {
                    "icon": "bolt", "stat": "+4.8x",
                    "title": "表现力跃迁", "desc": "有机花瓣徽章打破平直呆板。"
                }
            if "card_bot_right" not in data:
                data["card_bot_right"] = {
                    "icon": "verified", "title": "原生矢量交付",
                    "bullets": ["DrawingML 纯净编译", "抗字体降级体系", "100% 自由编辑修改"]
                }

        elif archetype == "process_roadmap":
            if "phases" not in data or not data["phases"]:
                data["phases"] = [
                    {"phase_num": "01", "name": "阶段一：探索", "time": "Q1", "status": "COMPLETED", "icon": "check", "deliverables": ["需求调研", "技术验证"], "kpi_chip": "100% 就绪"},
                    {"phase_num": "02", "name": "阶段二：开发", "time": "Q2", "status": "COMPLETED", "icon": "bolt", "deliverables": ["核心组件库", "排版规范"], "kpi_chip": "引擎就绪"},
                    {"phase_num": "03", "name": "阶段三：整合", "time": "Q3", "status": "ACTIVE", "icon": "layers", "deliverables": ["版式矩阵", "自动化流水线"], "kpi_chip": "进行中"},
                    {"phase_num": "04", "name": "阶段四：交付", "time": "Q4", "status": "UPCOMING", "icon": "rocket", "deliverables": ["全量上线", "用户验收"], "kpi_chip": "待启动"},
                ]

        elif archetype == "dual_contrast":
            if "left_plan" not in data:
                data["left_plan"] = {
                    "chip": "BASELINE", "title": "传统基线方案", "desc": "传统静态表格与沉闷直角设计。",
                    "points": ["低对比度冷灰色系", "缺乏视觉视觉锚点", "回退到系统字体"],
                    "metric_val": "34.5%", "metric_label": "信息留存率", "trend": "行业基准"
                }
            if "right_plan" not in data:
                data["right_plan"] = {
                    "chip": "RECOMMENDED", "title": "M3 表现力演进", "desc": "高活力双强调色感知架构与全胶囊交互。",
                    "points": ["28dp 核心容器倒角", "HCT 双强调色碰撞", "DrawingML 原生矢量图层"],
                    "metric_val": "86.4%", "metric_label": "信息留存率", "trend": "+2.5x 提升"
                }

        elif archetype == "kpi_metrics":
            if "metrics" not in data or not data["metrics"]:
                data["metrics"] = [
                    {"value": "99.9%", "label": "系统高可用", "trend": "+0.1% 达标", "icon": "shield", "desc": "高韧性架构", "highlight": False},
                    {"value": "12 ms", "label": "推理时延", "trend": "-60% 压缩", "icon": "speed", "desc": "编译加速优化", "highlight": True},
                    {"value": "4.5x", "label": "交付吞吐", "trend": "+350% 提速", "icon": "rocket", "desc": "自动化管线", "highlight": False},
                    {"value": "90%", "label": "用户满意度", "trend": "+20% 提升", "icon": "star", "desc": "体验全新升级", "highlight": False}
                ]
            data.setdefault("takeaway_badge", "KEY TAKEAWAY")
            data.setdefault("takeaway_text", "核心指标均实现量化突破，为系统规模化运行奠定坚实基础。")

        elif archetype == "feature_list":
            if "features" not in data or not data["features"]:
                data["features"] = [
                    {"tag": "PILLAR 01", "icon": "auto_awesome", "title": "HCT 动态感知色彩", "subtitle": "Dynamic Palette", "desc": "基于 Google MCU 算法推导的高对比度双强调色体系。", "points": ["WCAG AAA 级无障碍", "Light/Dark 双模式"], "badge": "算法内核", "highlight": False},
                    {"tag": "PILLAR 02", "icon": "grid_view", "title": "Bento 网格与大圆角", "subtitle": "28dp Modular Containers", "desc": "28dp 核心大容器倒角与 9999px 全胶囊药丸。", "points": ["DrawingML 几何高保真", "呼吸感留白"], "badge": "结构美学", "highlight": True},
                    {"tag": "PILLAR 03", "icon": "verified", "title": "原生矢量与抗降级", "subtitle": "DrawingML Rendering", "desc": "100% 原生矢量图层编译，跨平台自由编辑。", "points": ["33+ 款矢量图标", "永不走样降级"], "badge": "原生交付", "highlight": False}
                ]

        elif archetype == "quote_takeaway":
            data.setdefault("quote_text", "“设计不仅是视觉的外表，更是信息传达的秩序。Material 3 Expressive 将感知色彩与结构表现力融合，让每一个关键决策洞察都获得最清晰的共鸣。”")
            data.setdefault("quote_author", "Google Material Design Core Team")
            data.setdefault("quote_role", "Design Principles & Systems Architecture")
            if "pillars" not in data or not data["pillars"]:
                data["pillars"] = [
                    {"icon": "auto_awesome", "title": "高对比度聚焦", "desc": "以 Primary + Tertiary 形成双视觉锚点。"},
                    {"icon": "grid_view", "title": "便当盒模块化分舱", "desc": "采用 28dp 容器大倒角与呼吸感间距。"},
                    {"icon": "verified", "title": "100% 原生矢量可编辑", "desc": "基于 DrawingML 纯净编译，自由缩放编辑。"}
                ]

        elif archetype == "team_showcase":
            if "members" not in data or not data["members"]:
                data["members"] = [
                    {"name": "Elena Vance", "role": "CHIEF ARCHITECT", "icon": "psychology", "desc": "主导 M3 Expressive HCT 感知色彩与 DrawingML 动态编译引擎。", "tags": ["HCT 算法", "DrawingML"]},
                    {"name": "Marcus Zhang", "role": "DESIGN SYSTEMS LEAD", "icon": "palette", "desc": "负责 28dp Bento 容器美学、有机花瓣与排版规范设计。", "tags": ["Bento 架构", "M3 Tokens"]},
                    {"name": "Sarah Lin", "role": "ENGINEERING PRINCIPAL", "icon": "account_tree", "desc": "专注于高性能跨平台文档编译与矢量重着色管线。", "tags": ["矢量引擎", "工业化落地"]}
                ]

        return data

def auto_plan_from_outline(raw_data: Dict[str, Any]) -> DeckPlan:
    """
    Takes an input dictionary (from user JSON or structured outline)
    and constructs a fully-validated, normalized DeckPlan.
    """
    cfg_data = raw_data.get("config", {})
    if "title" not in cfg_data and "title" in raw_data:
        cfg_data["title"] = raw_data["title"]
    if "preset_theme" not in cfg_data and "preset_theme" in raw_data:
        cfg_data["preset_theme"] = raw_data["preset_theme"]
    if "seed_color" not in cfg_data and "seed_color" in raw_data:
        cfg_data["seed_color"] = raw_data["seed_color"]
    if "is_dark" not in cfg_data and "is_dark" in raw_data:
        cfg_data["is_dark"] = raw_data["is_dark"]

    config = DeckConfig.from_dict(cfg_data)

    raw_slides = raw_data.get("slides", [])
    total_pages = len(raw_slides) if raw_slides else 1
    config.total_pages = total_pages

    slides: List[SlidePlan] = []
    for idx, slide_item in enumerate(raw_slides, start=1):
        # Extract archetype or infer it
        arch = PlanMapper.infer_archetype(slide_item, page_index=idx, total_pages=total_pages)
        raw_content = slide_item.get("content", slide_item)
        
        # Pull top-level metadata if present
        for key in ["category", "title", "subtitle", "footer_left", "footer_right"]:
            if key in slide_item and key not in raw_content:
                raw_content[key] = slide_item[key]

        normalized_content = PlanMapper.normalize_slide_content(arch, raw_content, page_num=idx, total_pages=total_pages)
        slides.append(SlidePlan(archetype=arch, content=normalized_content, page_num=idx))

    return DeckPlan(config=config, slides=slides)
