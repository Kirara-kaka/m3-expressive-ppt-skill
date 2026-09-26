"""
Archetype 07: Quote & Key Takeaway Slide.
Editorial statement layout with prominent quote text, author attribution, and supporting takeaways.
"""

from pptx.util import Inches
from pptx.enum.text import MSO_ANCHOR
from core.tokens import M3Theme
from core.icon_manager import get_recolored_icon_png
from engine.components import M3Components
from engine.geometry import generate_scallop_badge_png
from engine.typography import create_textbox, add_styled_paragraph, SCALE_HEADLINE, SCALE_TITLE, SCALE_BODY_SMALL
from archetypes.base import apply_slide_canvas, render_standard_header, render_standard_footer

def render_quote_takeaway(slide, theme: M3Theme, data: dict):
    """
    Render Quote & Key Takeaway Slide.
    
    Data Schema:
      - category, title, subtitle
      - quote_text: str (Giant pull-quote)
      - quote_author: str (Attribution)
      - quote_role: str (Title/Role)
      - pillars: list of 3 dicts:
          - icon: "lightbulb"
          - title: "原则 01"
          - desc: "..."
    """
    apply_slide_canvas(slide, theme, style="tinted", add_ambient_bloom=True)

    render_standard_header(
        slide, theme,
        category_text=data.get("category", "EXECUTIVE TAKEAWAY"),
        title_text=data.get("title", "核心观点与战略共识"),
        subtitle_text=data.get("subtitle", "下一代演示体验的底层逻辑：秩序、活力与无损表达"),
        category_icon=data.get("category_icon", "lightbulb")
    )

    # -------------------------------------------------------------
    # HERO QUOTE CARD (Upper section, height: 2.3 inches)
    # -------------------------------------------------------------
    quote_card = M3Components.create_card(
        slide, theme,
        left=Inches(0.8), top=Inches(2.05),
        width=Inches(11.733), height=Inches(2.4),
        variant="filled", color_role="primary_container", corner_dp=28, padding=0.3
    )
    q_inner = quote_card.inner_bounds

    # Giant decorative quotation mark
    scallop_png = "assets/icons/rendered/quote_scallop.png"
    generate_scallop_badge_png(scallop_png, size=256, petals=12, fill_hex=theme.hex("primary"))
    slide.shapes.add_picture(scallop_png, q_inner.left, q_inner.top, Inches(0.7), Inches(0.7))

    icon_quote = get_recolored_icon_png("ai", "#FFFFFF", size=180)
    slide.shapes.add_picture(icon_quote, q_inner.left + Inches(0.15), q_inner.top + Inches(0.15), Inches(0.4), Inches(0.4))

    # Pull Quote Text
    quote_text = data.get("quote_text", 
        "“设计不仅是视觉的外表，更是信息传达的秩序。Material 3 Expressive 将感知色彩与结构表现力融合，让每一个关键决策洞察都获得最清晰的共鸣。”"
    )
    tb_q = create_textbox(slide, q_inner.left + Inches(0.95), q_inner.top, q_inner.width - Inches(1.1), Inches(1.3))
    add_styled_paragraph(tb_q.text_frame, quote_text, size_pt=17.5, bold=True, 
                         color_rgb=theme.rgb("on_primary_container"))

    # Author Attribution Pill
    author = data.get("quote_author", "Google Material Design Team")
    role = data.get("quote_role", "Design Principles & Systems")
    M3Components.create_chip(
        slide, theme,
        left=q_inner.left + Inches(0.95), top=q_inner.top + Inches(1.4),
        text=f"— {author} · {role}", icon_name="verified",
        color_role="surface_container_lowest", on_color_role="primary", height=0.32
    )

    # -------------------------------------------------------------
    # 3 SUPPORTING ACTION PILLARS (Lower section, height: 2.0 inches)
    # -------------------------------------------------------------
    pillars = data.get("pillars", [
        {
            "icon": "auto_awesome", "title": "高对比度聚焦",
            "desc": "以 Primary + Tertiary 形成视觉重心，彻底杜绝单调冷灰对注意力的稀释。"
        },
        {
            "icon": "grid_view", "title": "便当盒模块化分舱",
            "desc": "采用 28dp 容器大倒角与呼吸感间距，建立严密清晰的信息层级骨架。"
        },
        {
            "icon": "verified", "title": "100% 原生矢量可编辑",
            "desc": "基于 DrawingML 纯净编译，跨平台自由缩放编辑，文字永不发生降级走样。"
        }
    ])

    pil_y = 4.65
    pil_h = 2.05
    total_w = 11.733
    start_x = 0.8
    gap = 0.24
    col_w = (total_w - (2 * gap)) / 3.0

    for i, p in enumerate(pillars):
        x = start_x + (i * (col_w + gap))
        card_p = M3Components.create_card(
            slide, theme,
            left=Inches(x), top=Inches(pil_y),
            width=Inches(col_w), height=Inches(pil_h),
            variant="elevated", color_role="surface_container_lowest", corner_dp=24, padding=0.22
        )
        p_in = card_p.inner_bounds

        # Mini icon
        ic_img = get_recolored_icon_png(p.get("icon", "lightbulb"), theme.hex("primary"), size=140)
        slide.shapes.add_picture(ic_img, p_in.left, p_in.top, Inches(0.38), Inches(0.38))

        # Title vertically centered with icon
        tb_pt = create_textbox(slide, p_in.left + Inches(0.5), p_in.top, p_in.width - Inches(0.5), Inches(0.38),
                               vertical_anchor=MSO_ANCHOR.MIDDLE)
        add_styled_paragraph(tb_pt.text_frame, p.get("title", ""), size_pt=SCALE_TITLE, bold=True,
                             color_rgb=theme.rgb("on_surface"))

        # Desc
        tb_pd = create_textbox(slide, p_in.left, p_in.top + Inches(0.52), p_in.width, Inches(1.1))
        add_styled_paragraph(tb_pd.text_frame, p.get("desc", ""), size_pt=SCALE_BODY_SMALL,
                             color_rgb=theme.rgb("on_surface_variant"), space_before_pt=2)

    render_standard_footer(slide, theme, left_meta=data.get("footer_left", "Quote & Key Takeaway · M3 Expressive"), right_meta=data.get("footer_right", ""))
