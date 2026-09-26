"""
Integration test for Phase 2: DrawingML Geometry & Component Engine.
Generates an advanced Material 3 Expressive slide using the component library.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

from core.tokens import get_preset_theme
from core.icon_manager import get_recolored_icon_png
from engine.geometry import generate_scallop_badge_png
from engine.typography import (
    add_styled_paragraph, 
    create_textbox, 
    SCALE_DISPLAY_LARGE, 
    SCALE_HEADLINE, 
    SCALE_TITLE, 
    SCALE_BODY, 
    SCALE_BODY_SMALL,
    SCALE_LABEL
)
from engine.components import M3Components, M3BentoGrid, M3Canvas

def test_build_expressive_slide():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 1. Load Theme: Indigo & Coral Glow
    theme = get_preset_theme("indigo_coral", is_dark=False)

    # 2. Canvas Background (Theme-unified tinted tone + ambient bloom)
    M3Canvas.apply_background(slide, theme, style="tinted", add_ambient_bloom=True)

    # 3. Header Section with Category Chip
    M3Components.create_chip(
        slide, theme, 
        left=Inches(0.8), top=Inches(0.52), 
        text="MATERIAL 3 EXPRESSIVE · ENGINE V2", 
        icon_name="ai", 
        color_role="tertiary_container", 
        on_color_role="on_tertiary_container",
        height=0.36
    )

    # Main Title
    tb_header = create_textbox(slide, Inches(0.8), Inches(0.98), Inches(11.7), Inches(0.85))
    add_styled_paragraph(tb_header.text_frame, "Google 原生矢量组件与表现力几何引擎", 
                         size_pt=24, bold=True, color_rgb=theme.rgb("on_surface"))
    add_styled_paragraph(tb_header.text_frame, "全量接入 Google Material Symbols 官方矢量库 · 28dp Bento 容器 · 有机花瓣徽章与抗降级排版", 
                         size_pt=12, bold=False, color_rgb=theme.rgb("on_surface_variant"), space_before_pt=4)

    # 4. Bento Grid Layout
    b_hero, b_top, b_bot_left, b_bot_right = M3BentoGrid.layout_1_hero_3_sub(
        x=0.8, y=2.05, w=11.733, h=4.7, gap=0.24
    )

    # -------------------------------------------------------------
    # CARD 1: Hero Card (Primary Container)
    # -------------------------------------------------------------
    hero_res = M3Components.create_card(
        slide, theme,
        left=Inches(b_hero.left), top=Inches(b_hero.top),
        width=Inches(b_hero.width), height=Inches(b_hero.height),
        variant="filled", color_role="primary_container", corner_dp=28
    )
    
    # Official Material Symbol Icon
    icon_ai = get_recolored_icon_png("ai", theme.hex("primary"), size=256)
    slide.shapes.add_picture(icon_ai, hero_res.inner_bounds.left, hero_res.inner_bounds.top, Inches(0.55), Inches(0.55))

    M3Components.create_chip(
        slide, theme,
        left=hero_res.inner_bounds.left + Inches(0.72), top=hero_res.inner_bounds.top + Inches(0.08),
        text="OFFICIAL VECTOR", icon_name="verified",
        color_role="primary", on_color_role="on_primary", height=0.32
    )

    tb_hero = create_textbox(slide, hero_res.inner_bounds.left, hero_res.inner_bounds.top + Inches(0.8), 
                             hero_res.inner_bounds.width, Inches(1.8))
    add_styled_paragraph(tb_hero.text_frame, "官方矢量图标与算法色调", size_pt=SCALE_HEADLINE, bold=True, 
                         color_rgb=theme.rgb("on_primary_container"))
    add_styled_paragraph(tb_hero.text_frame, "Google Material Symbols Rounded System", size_pt=11, bold=True, 
                         color_rgb=theme.rgb("primary"), space_before_pt=2, space_after_pt=6)
    add_styled_paragraph(tb_hero.text_frame, 
                         "完全摆脱草图轮廓。直接通过 Google 官方静态 CDN 与本地缓存集成 33+ 款纯矢量图标，毫秒级动态重着色并以 1200+ DPI 嵌入 DrawingML 图层。", 
                         size_pt=SCALE_BODY, bold=False, color_rgb=theme.rgb("on_primary_container"))

    # Hero Nested Metric Box
    M3Components.create_hero_metric(
        slide, theme,
        left=hero_res.inner_bounds.left, top=hero_res.inner_bounds.top + Inches(2.7),
        width=hero_res.inner_bounds.width, height=Inches(1.4),
        metric_value="100%", metric_label="纯正 Google 官方矢量与算法覆盖度",
        trend_str="+4.8x 质感跃迁", color_role="primary", bg_role="surface_container_lowest"
    )

    # -------------------------------------------------------------
    # CARD 2: Top Right Bento Card (Surface Container)
    # -------------------------------------------------------------
    c2_res = M3Components.create_card(
        slide, theme,
        left=Inches(b_top.left), top=Inches(b_top.top),
        width=Inches(b_top.width), height=Inches(b_top.height),
        variant="outlined", color_role="surface_container", corner_dp=28
    )
    icon_bento = get_recolored_icon_png("bento", theme.hex("on_surface"), size=256)
    slide.shapes.add_picture(icon_bento, c2_res.inner_bounds.left, c2_res.inner_bounds.top, Inches(0.48), Inches(0.48))

    tb_c2 = create_textbox(slide, c2_res.inner_bounds.left + Inches(0.65), c2_res.inner_bounds.top, 
                           c2_res.inner_bounds.width - Inches(0.65), Inches(0.85))
    add_styled_paragraph(tb_c2.text_frame, "BentoGrid 算子与 28dp 大圆角", size_pt=SCALE_TITLE, bold=True, 
                         color_rgb=theme.rgb("on_surface"))
    add_styled_paragraph(tb_c2.text_frame, "基于 M3BentoGrid 算法自动计算多舱边界，卡片内外边距严格依循 16/24/28dp 黄金律。", 
                         size_pt=SCALE_BODY_SMALL, bold=False, color_rgb=theme.rgb("on_surface_variant"), space_before_pt=3)

    # 3 mini preview chips inside Card 2
    M3Components.create_chip(slide, theme, left=c2_res.inner_bounds.left + Inches(0.65), top=c2_res.inner_bounds.top + Inches(1.05),
                            text="28dp Container", icon_name="grid_view", color_role="primary_container", on_color_role="on_primary_container", height=0.28)
    M3Components.create_chip(slide, theme, left=c2_res.inner_bounds.left + Inches(2.15), top=c2_res.inner_bounds.top + Inches(1.05),
                            text="Pill 9999px", icon_name="bolt", color_role="tertiary_container", on_color_role="on_tertiary_container", height=0.28)
    M3Components.create_chip(slide, theme, left=c2_res.inner_bounds.left + Inches(3.45), top=c2_res.inner_bounds.top + Inches(1.05),
                            text="Tonal Elevation", icon_name="layers", color_role="surface_container_high", on_color_role="on_surface", height=0.28)

    # -------------------------------------------------------------
    # CARD 3: Bottom Right Left (Tertiary Expressive Card with Scallop)
    # -------------------------------------------------------------
    c3_res = M3Components.create_card(
        slide, theme,
        left=Inches(b_bot_left.left), top=Inches(b_bot_left.top),
        width=Inches(b_bot_left.width), height=Inches(b_bot_left.height),
        variant="filled", color_role="tertiary_container", corner_dp=24
    )
    
    # Generate and place iconic M3 Expressive Scallop Badge
    scallop_png = "assets/icons/rendered/scallop_tertiary.png"
    generate_scallop_badge_png(scallop_png, size=256, petals=12, fill_hex=theme.hex("tertiary"))
    slide.shapes.add_picture(scallop_png, c3_res.inner_bounds.left, c3_res.inner_bounds.top, Inches(0.55), Inches(0.55))
    
    # White icon inside scallop badge
    icon_bolt = get_recolored_icon_png("bolt", "#FFFFFF", size=128)
    slide.shapes.add_picture(icon_bolt, c3_res.inner_bounds.left + Inches(0.12), c3_res.inner_bounds.top + Inches(0.12), Inches(0.31), Inches(0.31))

    tb_c3 = create_textbox(slide, c3_res.inner_bounds.left, c3_res.inner_bounds.top + Inches(0.65), 
                           c3_res.inner_bounds.width, Inches(1.2))
    add_styled_paragraph(tb_c3.text_frame, "+3.4x", size_pt=26, bold=True, color_rgb=theme.rgb("tertiary"))
    add_styled_paragraph(tb_c3.text_frame, "有机表现力花瓣", size_pt=12, bold=True, color_rgb=theme.rgb("on_tertiary_container"))
    add_styled_paragraph(tb_c3.text_frame, "Scallop 徽章打破平直呆板。", size_pt=9.5, color_rgb=theme.rgb("on_tertiary_container"))

    # -------------------------------------------------------------
    # CARD 4: Bottom Right Right (Elevated Pure White)
    # -------------------------------------------------------------
    c4_res = M3Components.create_card(
        slide, theme,
        left=Inches(b_bot_right.left), top=Inches(b_bot_right.top),
        width=Inches(b_bot_right.width), height=Inches(b_bot_right.height),
        variant="elevated", color_role="surface_container_lowest", corner_dp=24
    )
    icon_check = get_recolored_icon_png("check", theme.hex("primary"), size=256)
    slide.shapes.add_picture(icon_check, c4_res.inner_bounds.left, c4_res.inner_bounds.top, Inches(0.42), Inches(0.42))

    tb_c4 = create_textbox(slide, c4_res.inner_bounds.left, c4_res.inner_bounds.top + Inches(0.55), 
                           c4_res.inner_bounds.width, Inches(1.3))
    add_styled_paragraph(tb_c4.text_frame, "抗降级排版栈", size_pt=13, bold=True, color_rgb=theme.rgb("on_surface"))
    
    bullets = ["DrawingML 双字族注入", "中文字体锁定现代无衬线", "任意缩放 100% 可编辑"]
    for b in bullets:
        add_styled_paragraph(tb_c4.text_frame, f"• {b}", size_pt=9.0, color_rgb=theme.rgb("on_surface_variant"), space_before_pt=2)

    # 5. Footer
    tb_footer = create_textbox(slide, Inches(0.8), Inches(6.95), Inches(11.733), Inches(0.35))
    add_styled_paragraph(tb_footer.text_frame, 
                         "Google Material 3 Expressive Engine · Phase 2 Architecture · 100% Native Vector DrawingML", 
                         size_pt=8.5, color_rgb=theme.rgb("outline"))

    os.makedirs("tests/output", exist_ok=True)
    out_pptx = safe_save_pptx(prs, "tests/output/m3_expressive_cards.pptx")
    print(f"[PASS] Successfully generated {out_pptx}!")
    return out_pptx

def safe_save_pptx(prs, target_path):
    try:
        prs.save(target_path)
        return target_path
    except PermissionError:
        base, ext = os.path.splitext(target_path)
        for i in range(1, 20):
            cand = f"{base}_v{i}{ext}"
            try:
                prs.save(cand)
                print(f"Notice: {target_path} is locked by PowerPoint. Saved to {cand} instead.")
                return cand
            except PermissionError:
                continue
        raise PermissionError(f"Could not save {target_path} in any version.")

if __name__ == "__main__":
    test_build_expressive_slide()
