"""
Google Material 3 Typography & Text Styling Engine.
Ensures crisp modern geometric sans-serif across all platforms by injecting
DrawingML East Asian (<a:ea>) and Latin (<a:latin>) typeface declarations.
"""

from typing import Optional
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml import parse_xml

# Default Cross-Platform Font Stacks
FONT_DISPLAY_LATIN = "Segoe UI Variable Display"
FONT_BODY_LATIN = "Segoe UI Variable Text"
FONT_EAST_ASIAN = "Noto Sans SC"

# Typography Scale Presets (pt) - 25% Enlarged for High Readability
SCALE_DISPLAY_LARGE = 36
SCALE_DISPLAY_MEDIUM = 26
SCALE_HEADLINE = 20
SCALE_TITLE = 16
SCALE_BODY = 13.5
SCALE_BODY_SMALL = 11.5
SCALE_LABEL = 10.5

def style_run(run, 
              text: str, 
              size_pt: float = SCALE_BODY, 
              bold: bool = False, 
              color_rgb: Optional[RGBColor] = None,
              font_latin: Optional[str] = None,
              font_ea: Optional[str] = None):
    """
    Format a text run with explicit Latin and East Asian DrawingML font tags.
    - Large and small titles (>= 16pt): Segoe UI Variable Display (Office ribbon displays
      Segoe UI Variable Display, Latin/numbers render in Display, Chinese renders in Noto Sans SC Bold
      preventing SimSun fallback).
    - Body text (< 16pt): Noto Sans SC (Office ribbon displays Noto Sans SC).
    """
    is_title = size_pt >= SCALE_TITLE

    if font_latin is None:
        font_latin = FONT_DISPLAY_LATIN if is_title else FONT_EAST_ASIAN
    if font_ea is None:
        font_ea = FONT_EAST_ASIAN

    run.text = text
    run.font.name = font_latin
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    if color_rgb:
        run.font.color.rgb = color_rgb

    # Inject DrawingML typeface tags into rPr
    rPr = run._r.get_or_add_rPr()
    for child in list(rPr):
        if child.tag.endswith('ea') or child.tag.endswith('latin'):
            rPr.remove(child)

    latin_el = parse_xml(f'<a:latin xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="{font_latin}"/>')
    ea_el = parse_xml(f'<a:ea xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="{font_ea}"/>')
    rPr.append(latin_el)
    rPr.append(ea_el)

def style_paragraph(paragraph,
                    text: str,
                    size_pt: float = SCALE_BODY,
                    bold: bool = False,
                    color_rgb: Optional[RGBColor] = None,
                    align: Optional[PP_ALIGN] = None,
                    space_before_pt: float = 0,
                    space_after_pt: float = 0,
                    font_latin: Optional[str] = None,
                    font_ea: str = FONT_EAST_ASIAN):
    """Style an entire paragraph with a single run and paragraph spacing/alignment."""
    paragraph.text = ""
    if align is not None:
        paragraph.alignment = align
    if space_before_pt > 0:
        paragraph.space_before = Pt(space_before_pt)
    if space_after_pt > 0:
        paragraph.space_after = Pt(space_after_pt)

    run = paragraph.add_run()
    style_run(run, text, size_pt, bold, color_rgb, font_latin, font_ea)
    return paragraph

def add_styled_paragraph(text_frame,
                         text: str,
                         size_pt: float = SCALE_BODY,
                         bold: bool = False,
                         color_rgb: Optional[RGBColor] = None,
                         align: Optional[PP_ALIGN] = None,
                         space_before_pt: float = 0,
                         space_after_pt: float = 0,
                         font_latin: Optional[str] = None,
                         font_ea: str = FONT_EAST_ASIAN):
    """Add a new paragraph to a text_frame and style it."""
    # If the first paragraph is completely empty, reuse it
    if len(text_frame.paragraphs) == 1 and text_frame.paragraphs[0].text == "":
        p = text_frame.paragraphs[0]
    else:
        p = text_frame.add_paragraph()
    return style_paragraph(p, text, size_pt, bold, color_rgb, align, space_before_pt, space_after_pt, font_latin, font_ea)

def create_textbox(slide, left: float, top: float, width: float, height: float, 
                   margin_zero: bool = True, vertical_anchor: Optional[MSO_ANCHOR] = None):
    """Create a clean textbox with optional zero-margin padding and vertical anchor."""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    if margin_zero:
        tf.margin_left = 0
        tf.margin_right = 0
        tf.margin_top = 0
        tf.margin_bottom = 0
    if vertical_anchor is not None:
        tf.vertical_anchor = vertical_anchor
    return tb
