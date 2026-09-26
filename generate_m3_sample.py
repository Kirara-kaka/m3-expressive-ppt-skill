import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

def set_corner_radius(shape, adj_val):
    """Set DrawingML adjustment value for roundRect (0 to 50000)."""
    prstGeom = shape._element.spPr.prstGeom
    for child in list(prstGeom):
        if child.tag.endswith('avLst'):
            prstGeom.remove(child)
    new_av = parse_xml(f'<a:avLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:gd name="adj" fmla="val {adj_val}"/></a:avLst>')
    prstGeom.append(new_av)

def set_soft_shadow(shape, hex_color="00105C", alpha_val="10000", blur_rad="200000", dist="35000"):
    """Inject subtle, elegant tinted shadow into DrawingML shape."""
    spPr = shape._element.spPr
    effectLst = parse_xml(
        f'<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:outerShdw blurRad="{blur_rad}" dist="{dist}" dir="5400000" algn="b" rotWithShape="0">'
        f'<a:srgbClr val="{hex_color}"><a:alpha val="{alpha_val}"/></a:srgbClr>'
        f'</a:outerShdw>'
        f'</a:effectLst>'
    )
    spPr.append(effectLst)

def style_text(paragraph, text, font_name="Segoe UI Variable Display", ea_font="Microsoft YaHei UI", 
               size_pt=12, bold=False, color_rgb=None, align=None, space_after=0, space_before=0):
    """Ensure both Latin and East Asian (Chinese) text render with clean modern sans-serif."""
    paragraph.text = text
    if align:
        paragraph.alignment = align
    if space_after:
        paragraph.space_after = Pt(space_after)
    if space_before:
        paragraph.space_before = Pt(space_before)
    
    for run in paragraph.runs:
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        if color_rgb:
            run.font.color.rgb = color_rgb
        
        # Inject DrawingML East Asian font tag
        rPr = run._r.get_or_add_rPr()
        for child in list(rPr):
            if child.tag.endswith('ea'):
                rPr.remove(child)
        ea_el = parse_xml(f'<a:ea xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="{ea_font}"/>')
        rPr.append(ea_el)

def create_icon_badge(filename, bg_color_rgb, symbol_type, size=256):
    """Generate crisp, high-DPI Material Symbol icons as PNG."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, size-8, size-8], fill=bg_color_rgb)
    
    white = (255, 255, 255, 255)
    center = size // 2
    
    if symbol_type == "sparkle":
        r_out = size * 0.32
        r_in = size * 0.09
        pts = [
            (center, center - r_out),
            (center + r_in, center - r_in),
            (center + r_out, center),
            (center + r_in, center + r_in),
            (center, center + r_out),
            (center - r_in, center + r_in),
            (center - r_out, center),
            (center - r_in, center - r_in),
        ]
        draw.polygon(pts, fill=white)
    elif symbol_type == "bento":
        margin = size * 0.28
        w = size * 0.18
        gap = size * 0.06
        draw.rounded_rectangle([margin, margin, margin + w, margin + w * 2.2], radius=size*0.04, fill=white)
        draw.rounded_rectangle([margin + w + gap, margin, margin + w * 2.2 + gap, margin + w], radius=size*0.04, fill=white)
        draw.rounded_rectangle([margin + w + gap, margin + w + gap, margin + w * 2.2 + gap, margin + w * 2.2], radius=size*0.04, fill=white)
    elif symbol_type == "trending":
        pts = [
            (size * 0.25, size * 0.68),
            (size * 0.45, size * 0.48),
            (size * 0.60, size * 0.60),
            (size * 0.75, size * 0.32),
        ]
        draw.line(pts, fill=white, width=int(size * 0.08), joint="curve")
        draw.polygon([
            (size * 0.78, size * 0.30),
            (size * 0.60, size * 0.30),
            (size * 0.78, size * 0.48),
        ], fill=white)
    elif symbol_type == "verified":
        pts = [
            (size * 0.30, size * 0.52),
            (size * 0.44, size * 0.68),
            (size * 0.72, size * 0.35),
        ]
        draw.line(pts, fill=white, width=int(size * 0.09), joint="curve")
        
    img.save(filename, 'PNG')

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Material 3 Expressive Tokens
    C_SURFACE = hex_to_rgb("F8F9FE")
    C_ON_SURFACE = hex_to_rgb("191C20")
    C_ON_SURFACE_VAR = hex_to_rgb("44474F")
    C_OUTLINE_VAR = hex_to_rgb("C4C6D0")

    # Primary (Indigo)
    C_PRIMARY = hex_to_rgb("005AC1")
    C_PRIMARY_CONTAINER = hex_to_rgb("D8E2FF")
    C_ON_PRIMARY_CONTAINER = hex_to_rgb("001A41")

    # Expressive Tertiary (Vibrant Coral / Peach)
    C_TERTIARY = hex_to_rgb("984061")
    C_TERTIARY_CONTAINER = hex_to_rgb("FFD9E2")
    C_ON_TERTIARY_CONTAINER = hex_to_rgb("3E001D")

    # Containers
    C_SURFACE_CONTAINER = hex_to_rgb("EEF2F8")
    C_SURFACE_CONTAINER_HIGH = hex_to_rgb("E7EDF4")
    C_SURFACE_CONTAINER_LOWEST = hex_to_rgb("FFFFFF")

    FONT_ENG = "Segoe UI Variable Display"
    FONT_ZH = "Microsoft YaHei UI"

    # Slide Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_SURFACE
    bg.line.fill.background()

    # Generate Icons
    os.makedirs("temp_icons", exist_ok=True)
    icon_sparkle = "temp_icons/icon_sparkle.png"
    icon_bento = "temp_icons/icon_bento.png"
    icon_trending = "temp_icons/icon_trending.png"
    icon_verified = "temp_icons/icon_verified.png"
    
    create_icon_badge(icon_sparkle, (0, 90, 193, 255), "sparkle")
    create_icon_badge(icon_bento, (68, 71, 79, 255), "bento")
    create_icon_badge(icon_trending, (152, 64, 97, 255), "trending")
    create_icon_badge(icon_verified, (0, 106, 96, 255), "verified")

    # 1. Slide Header
    # Category Pill
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.55), Inches(3.2), Inches(0.36))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_TERTIARY_CONTAINER
    badge.line.fill.background()
    set_corner_radius(badge, 50000)
    style_text(badge.text_frame.paragraphs[0], "✦  MATERIAL 3 EXPRESSIVE", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=10.5, bold=True, 
               color_rgb=C_ON_TERTIARY_CONTAINER, align=PP_ALIGN.CENTER)

    # Main Title & Subtitle Box
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.98), Inches(11.7), Inches(0.85))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    style_text(tf.paragraphs[0], "下一代演示架构：感知色彩与 Bento 便当盒网格", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=24, bold=True, color_rgb=C_ON_SURFACE)
    
    p2 = tf.add_paragraph()
    style_text(p2, "融合 Google HCT 双强调色动态色调、28dp 大圆角容器与 100% 原生矢量可编辑特性", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=12, bold=False, color_rgb=C_ON_SURFACE_VAR, space_before=4)

    # Bento Grid Top Y
    GRID_Y = Inches(2.05)

    # -------------------------------------------------------------
    # CARD 1: Hero Card (Left, Primary Container)
    # -------------------------------------------------------------
    c1_left, c1_top, c1_w, c1_h = Inches(0.8), GRID_Y, Inches(5.6), Inches(4.7)
    card1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c1_left, c1_top, c1_w, c1_h)
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_PRIMARY_CONTAINER
    card1.line.fill.background()
    set_corner_radius(card1, 8000)
    set_soft_shadow(card1, hex_color="001A41", alpha_val="10000", blur_rad="220000", dist="40000")

    slide.shapes.add_picture(icon_sparkle, c1_left + Inches(0.4), c1_top + Inches(0.38), Inches(0.55), Inches(0.55))

    c1_chip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c1_left + Inches(1.1), c1_top + Inches(0.44), Inches(1.8), Inches(0.32))
    c1_chip.fill.solid()
    c1_chip.fill.fore_color.rgb = C_PRIMARY
    c1_chip.line.fill.background()
    set_corner_radius(c1_chip, 50000)
    style_text(c1_chip.text_frame.paragraphs[0], "CORE PILLAR · 01", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=9.5, bold=True, 
               color_rgb=hex_to_rgb("FFFFFF"), align=PP_ALIGN.CENTER)

    tb1 = slide.shapes.add_textbox(c1_left + Inches(0.4), c1_top + Inches(1.15), Inches(4.8), Inches(1.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
    
    style_text(tf1.paragraphs[0], "双强调色高对比度体系", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=19, bold=True, color_rgb=C_ON_PRIMARY_CONTAINER)
    
    p = tf1.add_paragraph()
    style_text(p, "Dual-Chroma High Contrast System", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=11, bold=True, color_rgb=C_PRIMARY, space_before=2, space_after=8)

    p = tf1.add_paragraph()
    style_text(p, "打破早期 Material 沉闷的单强调色束缚。M3 Expressive 将主调色 (Primary) 与高活力的第三强调色 (Expressive Tertiary) 并置，使核心结论与数据跃然而出，获得极佳的层次跃迁。", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=11, bold=False, color_rgb=hex_to_rgb("2A3555"))

    # Nested Metric Card
    nest = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c1_left + Inches(0.4), c1_top + Inches(3.05), Inches(4.8), Inches(1.25))
    nest.fill.solid()
    nest.fill.fore_color.rgb = C_SURFACE_CONTAINER_LOWEST
    nest.line.fill.background()
    set_corner_radius(nest, 12000)
    set_soft_shadow(nest, hex_color="001A41", alpha_val="8000", blur_rad="150000", dist="30000")

    tb_nest = slide.shapes.add_textbox(c1_left + Inches(0.65), c1_top + Inches(3.18), Inches(4.3), Inches(1.0))
    tfn = tb_nest.text_frame
    tfn.word_wrap = True
    tfn.margin_left = tfn.margin_right = tfn.margin_top = tfn.margin_bottom = 0
    style_text(tfn.paragraphs[0], "86.4%", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=32, bold=True, color_rgb=C_PRIMARY)
    
    p2 = tfn.add_paragraph()
    style_text(p2, "信息传达与视觉聚焦效率提升 (Visual Engagement Index)", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=9.5, bold=False, color_rgb=C_ON_SURFACE_VAR)

    # -------------------------------------------------------------
    # CARD 2: Top Right (Bento Container Card)
    # -------------------------------------------------------------
    c2_left, c2_top, c2_w, c2_h = Inches(6.65), GRID_Y, Inches(5.88), Inches(2.15)
    card2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c2_left, c2_top, c2_w, c2_h)
    card2.fill.solid()
    card2.fill.fore_color.rgb = C_SURFACE_CONTAINER
    card2.line.color.rgb = C_OUTLINE_VAR
    card2.line.width = Pt(0.75)
    set_corner_radius(card2, 9000)

    slide.shapes.add_picture(icon_bento, c2_left + Inches(0.35), c2_top + Inches(0.3), Inches(0.48), Inches(0.48))

    tb2 = slide.shapes.add_textbox(c2_left + Inches(1.0), c2_top + Inches(0.28), Inches(4.6), Inches(1.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0
    
    style_text(tf2.paragraphs[0], "Bento 便当盒架构与 28dp 大圆角", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=16, bold=True, color_rgb=C_ON_SURFACE)

    p = tf2.add_paragraph()
    style_text(p, "严格遵循 Google Design Tokens 标准：Extra-Large (28px) 容器外廓与 9999px 胶囊药丸交互组件，彻底告别死板直角，呈现秩序井然的便当盒分舱美学。", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=10.5, bold=False, color_rgb=C_ON_SURFACE_VAR, space_before=4)

    tags = [("Corner 28dp", C_PRIMARY_CONTAINER, C_ON_PRIMARY_CONTAINER),
            ("Pill 9999px", C_TERTIARY_CONTAINER, C_ON_TERTIARY_CONTAINER),
            ("Surface Tint", C_SURFACE_CONTAINER_HIGH, C_ON_SURFACE)]
    tx = c2_left + Inches(1.0)
    for tag_text, tag_bg, tag_fg in tags:
        t_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx, c2_top + Inches(1.5), Inches(1.35), Inches(0.3))
        t_shape.fill.solid()
        t_shape.fill.fore_color.rgb = tag_bg
        t_shape.line.fill.background()
        set_corner_radius(t_shape, 50000)
        style_text(t_shape.text_frame.paragraphs[0], tag_text, 
                   font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=8.5, bold=True, 
                   color_rgb=tag_fg, align=PP_ALIGN.CENTER)
        tx += Inches(1.45)

    # -------------------------------------------------------------
    # CARD 3: Bottom Right Left (Tertiary Accent Card)
    # -------------------------------------------------------------
    c3_left, c3_top, c3_w, c3_h = Inches(6.65), GRID_Y + Inches(2.35), Inches(2.82), Inches(2.35)
    card3 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c3_left, c3_top, c3_w, c3_h)
    card3.fill.solid()
    card3.fill.fore_color.rgb = C_TERTIARY_CONTAINER
    card3.line.fill.background()
    set_corner_radius(card3, 11000)
    set_soft_shadow(card3, hex_color="3E001D", alpha_val="9000", blur_rad="160000", dist="30000")

    slide.shapes.add_picture(icon_trending, c3_left + Inches(0.3), c3_top + Inches(0.28), Inches(0.42), Inches(0.42))

    tb3 = slide.shapes.add_textbox(c3_left + Inches(0.3), c3_top + Inches(0.82), Inches(2.3), Inches(1.35))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0
    
    style_text(tf3.paragraphs[0], "+3.4x", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=28, bold=True, color_rgb=C_TERTIARY)

    p = tf3.add_paragraph()
    style_text(p, "Expressive 焦点转化", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=12, bold=True, color_rgb=C_ON_TERTIARY_CONTAINER, space_before=2)

    p = tf3.add_paragraph()
    style_text(p, "通过暖珊瑚跃迁色锁定重点视线，形成天然阅读动线。", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=9.5, bold=False, color_rgb=hex_to_rgb("532C3A"), space_before=2)

    # -------------------------------------------------------------
    # CARD 4: Bottom Right Right (Elevated White Container)
    # -------------------------------------------------------------
    c4_left, c4_top, c4_w, c4_h = Inches(9.67), GRID_Y + Inches(2.35), Inches(2.86), Inches(2.35)
    card4 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c4_left, c4_top, c4_w, c4_h)
    card4.fill.solid()
    card4.fill.fore_color.rgb = C_SURFACE_CONTAINER_LOWEST
    card4.line.color.rgb = hex_to_rgb("E0E4EC")
    card4.line.width = Pt(0.75)
    set_corner_radius(card4, 11000)
    set_soft_shadow(card4, hex_color="00105C", alpha_val="7000", blur_rad="180000", dist="30000")

    slide.shapes.add_picture(icon_verified, c4_left + Inches(0.3), c4_top + Inches(0.28), Inches(0.42), Inches(0.42))

    tb4 = slide.shapes.add_textbox(c4_left + Inches(0.3), c4_top + Inches(0.82), Inches(2.3), Inches(1.35))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    tf4.margin_left = tf4.margin_right = tf4.margin_top = tf4.margin_bottom = 0
    
    style_text(tf4.paragraphs[0], "100% 原生矢量", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=14, bold=True, color_rgb=C_ON_SURFACE)

    bullets = [
        "DrawingML 纯矢量编译",
        "文字/度数均可直接修改",
        "无缝适配深色/浅色模式",
        "跨设备排版永不位移"
    ]
    for b in bullets:
        p = tf4.add_paragraph()
        style_text(p, f"• {b}", font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=9.2, bold=False, color_rgb=C_ON_SURFACE_VAR, space_before=2)

    # 6. Slide Footer
    ft_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(6.0), Inches(0.35))
    style_text(ft_left.text_frame.paragraphs[0], 
               "Google Material Design 3 Expressive Specification · Automated Skill Architecture", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=8.5, bold=False, color_rgb=hex_to_rgb("8E919A"))

    ft_right = slide.shapes.add_textbox(Inches(9.0), Inches(6.95), Inches(3.53), Inches(0.35))
    style_text(ft_right.text_frame.paragraphs[0], 
               "Slide Archetype · Bento Grid Dashboard", 
               font_name=FONT_ENG, ea_font=FONT_ZH, size_pt=8.5, bold=False, color_rgb=hex_to_rgb("8E919A"), align=PP_ALIGN.RIGHT)

    output_pptx = "material_3_expressive_sample.pptx"
    prs.save(output_pptx)
    print(f"Generated {output_pptx} with perfect East Asian fonts successfully!")

if __name__ == "__main__":
    build_presentation()
