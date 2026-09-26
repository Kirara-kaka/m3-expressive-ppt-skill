"""
Archetype 06: Feature Matrix / Multi-Column Feature Cards Slide.
Balanced 3-column or 4-column cards highlighting core pillars and system capabilities.
"""

from pptx.util import Inches
from core.tokens import M3Theme
from core.icon_manager import get_recolored_icon_png
from engine.components import M3Components
from engine.typography import create_textbox, add_styled_paragraph, SCALE_HEADLINE, SCALE_TITLE, SCALE_BODY, SCALE_BODY_SMALL
from archetypes.base import apply_slide_canvas, render_standard_header, render_standard_footer

def render_feature_list(slide, theme: M3Theme, data: dict):
    """
    Render Feature List / Matrix Slide.
    
    Data Schema:
      - category, title, subtitle
      - features: list of 3-4 dicts:
          - tag: "PILLAR 01"
          - icon: "auto_awesome"
          - title: "动态感知色彩系统"
          - subtitle: "HCT Dynamic Scheme"
          - desc: "基于 Google MCU 算法..."
          - points: ["...", "..."]
          - badge: "算法自动计算"
    """
    apply_slide_canvas(slide, theme, style="tinted", add_ambient_bloom=True)

    render_standard_header(
        slide, theme,
        category_text=data.get("category", "CORE ARCHITECTURE"),
        title_text=data.get("title", "系统三大核心能力与特性矩阵"),
        subtitle_text=data.get("subtitle", "基于 Material 3 表现力规范构建的核心技术与体验支柱"),
        category_icon=data.get("category_icon", "account_tree")
    )

    features = data.get("features", [
        {
            "tag": "PILLAR 01", "icon": "auto_awesome",
            "title": "HCT 动态感知色彩", "subtitle": "Dual-Chroma Dynamic Palette",
            "desc": "突破传统沉闷色调。通过 Google MCU 算法推导和谐高对比度的 Primary 与 Tertiary 双强调色体系。",
            "points": ["WCAG AAA 级无障碍对比度", "Light/Dark 双模式毫秒级映射", "4 套旗舰级预设调色板开箱即用"],
            "badge": "官方算法内核", "highlight": False
        },
        {
            "tag": "PILLAR 02", "icon": "grid_view",
            "title": "Bento 网格与大圆角", "subtitle": "28dp Modular Containers",
            "desc": "基于 Google Design Tokens 标准，采用 28dp 核心大容器倒角与 9999px 全胶囊药丸交互组件。",
            "points": ["DrawingML 几何曲率高保真控制", "模块化信息分舱与呼吸感留白", "多端自适应安全内边距"],
            "badge": "结构美学重构", "highlight": True
        },
        {
            "tag": "PILLAR 03", "icon": "verified",
            "title": "原生矢量与抗降级", "subtitle": "Pure DrawingML Rendering",
            "desc": "100% 原生矢量图层编译。中文排版注入双字族声明，彻底杜绝回退宋体问题，跨平台完全可二次编辑。",
            "points": ["33+ 款官方 Material Symbols 矢量", "跨设备字体渲染永不走样", "支持 PowerPoint/Keynote 拖拽编辑"],
            "badge": "100% 原生可编辑", "highlight": False
        }
    ])

    num_cols = len(features)
    total_w = 11.733
    start_x = 0.8
    gap = 0.24
    col_w = (total_w - ((num_cols - 1) * gap)) / num_cols
    card_y = 2.05
    card_h = 4.7

    for i, f in enumerate(features):
        x = start_x + (i * (col_w + gap))
        is_hl = f.get("highlight", False)

        variant = "filled" if is_hl else "elevated"
        bg_role = "primary_container" if is_hl else "surface_container_lowest"
        text_role = "on_primary_container" if is_hl else "on_surface"
        accent_role = "primary"

        card_res = M3Components.create_card(
            slide, theme,
            left=Inches(x), top=Inches(card_y),
            width=Inches(col_w), height=Inches(card_h),
            variant=variant, color_role=bg_role, corner_dp=28, padding=0.26
        )
        inner = card_res.inner_bounds

        # Icon and Tag Pill
        icon_name = f.get("icon", "star")
        icon_img = get_recolored_icon_png(icon_name, theme.hex(accent_role), size=180)
        slide.shapes.add_picture(icon_img, inner.left, inner.top, Inches(0.48), Inches(0.48))

        M3Components.create_chip(
            slide, theme,
            left=inner.left + Inches(0.65), top=inner.top + Inches(0.06),
            text=f.get("tag", f"PILLAR 0{i+1}"), icon_name="bolt",
            color_role="primary" if is_hl else "surface_container_highest",
            on_color_role="on_primary" if is_hl else "on_surface",
            height=0.32
        )

        # Title & Subtitle
        tb_t = create_textbox(slide, inner.left, inner.top + Inches(0.62), inner.width, Inches(0.85))
        add_styled_paragraph(tb_t.text_frame, f.get("title", ""), size_pt=SCALE_HEADLINE, bold=True,
                             color_rgb=theme.rgb(text_role))
        add_styled_paragraph(tb_t.text_frame, f.get("subtitle", ""), size_pt=10.5, bold=True,
                             color_rgb=theme.rgb(accent_role), space_before_pt=2)

        # Description (Body text with standard variant tone)
        desc_color = "on_primary_container" if is_hl else "on_surface_variant"
        tb_d = create_textbox(slide, inner.left, inner.top + Inches(1.52), inner.width, Inches(0.92))
        add_styled_paragraph(tb_d.text_frame, f.get("desc", ""), size_pt=SCALE_BODY_SMALL, bold=False,
                             color_rgb=theme.rgb(desc_color))

        # Nested Sub-Card Container for Points (Card-in-Card design with high contrast text)
        sub_card_bg = "surface_container_lowest" if is_hl else "surface_container_low"
        sub_res = M3Components.create_card(
            slide, theme,
            left=inner.left, top=inner.top + Inches(2.50),
            width=inner.width, height=Inches(1.24),
            variant="filled", color_role=sub_card_bg, corner_dp=16, padding=0.12
        )
        
        # Points inside sub-card: distinct contrasting font color
        points_color = "primary" if is_hl else "on_surface"
        M3Components.create_checklist(
            slide, theme,
            left=sub_res.inner_bounds.left,
            top=sub_res.inner_bounds.top + Inches(0.04),
            width=sub_res.inner_bounds.width,
            items=f.get("points", []),
            icon_name="check",
            icon_bg_role="primary" if is_hl else "primary_container",
            icon_fg_role="on_primary" if is_hl else "primary",
            font_size_pt=10.0,
            text_color_role=points_color,
            bold_text=True,
            item_spacing_in=0.32,
            badge_size=0.18
        )

        # Bottom Badge
        badge_text = f.get("badge", "")
        if badge_text:
            M3Components.create_chip(
                slide, theme,
                left=inner.left, top=inner.top + Inches(3.86),
                text=badge_text, icon_name="verified",
                color_role="surface_container_lowest" if is_hl else "primary_container",
                on_color_role=accent_role, height=0.30
            )

    render_standard_footer(slide, theme, left_meta=data.get("footer_left", "Feature Matrix · M3 Expressive"), right_meta=data.get("footer_right", ""))
