import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml import parse_xml

from core.tokens import get_preset_theme
from engine.components import M3Components
from engine.typography import create_textbox, add_styled_paragraph

theme = get_preset_theme("electric_violet", is_dark=False)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
slide = prs.slides.add_slide(prs.slide_layouts[6])

# Let's test aligning a circle badge and a line of text at a defined centerline Y.
# If row centerline is at Y = mid_y:
# Circle badge has diameter D = 0.20 in.
# Circle top = mid_y - D / 2.
# Now where should the textbox be?
# Let's test 5 configurations for the textbox:
# Config 1: tb top = mid_y - D/2, height = D, vertical_anchor = MIDDLE
# Config 2: tb top = mid_y - D/2, height = D, vertical_anchor = None (top)
# Config 3: tb top = mid_y - Pt(7), height = Pt(14), vertical_anchor = MIDDLE
# Config 4: tb top = mid_y - D/2 - Pt(1.5), height = D + Pt(3.0), vertical_anchor = MIDDLE
# Config 5: tb top = mid_y - D/2, height = 0.32, vertical_anchor = MIDDLE, with offset

mid_ys = [1.2, 2.2, 3.2, 4.2, 5.2]
badge_size = 0.20

test_configs = [
    ("Config 1: tb top = mid - D/2, height = D, anchor = MIDDLE", 
     lambda my: (my - badge_size/2, badge_size, MSO_ANCHOR.MIDDLE)),
    ("Config 2: tb top = mid - D/2, height = D, anchor = None", 
     lambda my: (my - badge_size/2, badge_size, None)),
    ("Config 3: tb top = mid - Pt(8)/72, height = Pt(16)/72, anchor = MIDDLE", 
     lambda my: (my - (8.0/72.0), 16.0/72.0, MSO_ANCHOR.MIDDLE)),
    ("Config 4: tb top = mid - Pt(6.5)/72, height = Pt(13)/72, anchor = MIDDLE", 
     lambda my: (my - (6.5/72.0), 13.0/72.0, MSO_ANCHOR.MIDDLE)),
    ("Config 5: tb top = mid - D/2 - Pt(1)/72, height = D, anchor = MIDDLE", 
     lambda my: (my - badge_size/2 - (1.0/72.0), badge_size, MSO_ANCHOR.MIDDLE)),
]

for idx, ((cfg_name, cfg_func), my) in enumerate(zip(test_configs, mid_ys)):
    # 1. Draw a thin red reference centerline across the entire row
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(my), Inches(11.5), Pt(0.75))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(255, 60, 60)
    line.line.fill.background()
    
    # 2. Draw circle badge centered on mid_y
    c_top = my - (badge_size / 2.0)
    badge = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.0), Inches(c_top), Inches(badge_size), Inches(badge_size))
    badge.fill.solid()
    badge.fill.fore_color.rgb = theme.rgb("primary_container")
    badge.line.fill.background()
    # Remove default shadow
    spPr = badge._sp.spPr
    for child in list(spPr):
        if child.tag.endswith('effectLst'):
            spPr.remove(child)
    spPr.append(parse_xml('<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
    style = badge._sp.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
    if style is not None:
        eff = style.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectRef')
        if eff is not None:
            eff.set('idx', '0')

    # Draw icon inside badge
    from core.icon_manager import get_recolored_icon_png
    icon_png = get_recolored_icon_png("verified", theme.hex("primary"), size=128)
    inner_s = badge_size * 0.58
    off = (badge_size - inner_s) / 2.0
    slide.shapes.add_picture(icon_png, Inches(1.0 + off), Inches(c_top + off), Inches(inner_s), Inches(inner_s))

    # 3. Draw Textbox according to config
    tb_top, tb_h, anchor = cfg_func(my)
    tb = create_textbox(slide, Inches(1.35), Inches(tb_top), Inches(10.0), Inches(tb_h), vertical_anchor=anchor)
    add_styled_paragraph(tb.text_frame, f"{cfg_name} · 单 Prompt 职责过载导致严重幻觉", 
                         size_pt=10.5, bold=False, color_rgb=theme.rgb("on_surface"))

os.makedirs("tests/output", exist_ok=True)
prs.save("tests/output/test_centerline.pptx")
print("Saved test_centerline.pptx")
