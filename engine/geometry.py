"""
Google Material 3 Expressive Geometry & DrawingML Manipulation Engine.
Manages corner radius, pill capsules, ambient shadows, and organic expressive shapes.
"""

import math
import os
from pptx.oxml import parse_xml
import resvg_py

from core.shapes_tokens import calculate_drawingml_adj, M3_CORNER_EXTRA_LARGE, M3_CORNER_FULL

def set_corner_radius(shape, adj_val: int):
    """
    Directly set DrawingML adjustment value for a rounded rectangle.
    adj_val ranges from 0 (sharp 90 deg) to 50000 (complete 50% pill/capsule).
    """
    prstGeom = shape._element.spPr.prstGeom
    for child in list(prstGeom):
        if child.tag.endswith('avLst'):
            prstGeom.remove(child)
    new_av = parse_xml(
        f'<a:avLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:gd name="adj" fmla="val {adj_val}"/>'
        f'</a:avLst>'
    )
    prstGeom.append(new_av)

def apply_dp_corner(shape, width_in: float, height_in: float, corner_dp: int = M3_CORNER_EXTRA_LARGE):
    """Apply Google M3 standard corner radius in dp (default 28dp Extra-Large)."""
    adj = calculate_drawingml_adj(width_in, height_in, corner_dp)
    set_corner_radius(shape, adj)

def apply_pill_corner(shape):
    """Make the shape a 100% full capsule pill."""
    set_corner_radius(shape, 50000)

def apply_ambient_shadow(shape, hex_color: str = "00105C", alpha_val: str = "9000", blur_rad: str = "200000", dist: str = "32000"):
    """
    Inject subtle, elegant tinted ambient shadow into DrawingML shape.
    Replaces harsh dark shadows with Google M3 tinted elevation.
    """
    clean_hex = hex_color.lstrip("#").upper()
    spPr = shape._element.spPr
    for child in list(spPr):
        if child.tag.endswith('effectLst'):
            spPr.remove(child)
    effectLst = parse_xml(
        f'<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        f'<a:outerShdw blurRad="{blur_rad}" dist="{dist}" dir="5400000" algn="b" rotWithShape="0">'
        f'<a:srgbClr val="{clean_hex}"><a:alpha val="{alpha_val}"/></a:srgbClr>'
        f'</a:outerShdw>'
        f'</a:effectLst>'
    )
    spPr.append(effectLst)

def generate_scallop_badge_png(output_path: str, size: int = 512, petals: int = 12, 
                               fill_hex: str = "#FFD9E2", stroke_hex: str = None) -> str:
    """
    Generate Google Material 3 Expressive iconic Scallop / Asterisk flower badge
    and render as a high-DPI transparent PNG.
    """
    cx, cy = size / 2.0, size / 2.0
    r_outer = size * 0.46
    r_inner = size * 0.38
    
    # Construct smooth organic multi-petal wave path
    points = []
    num_steps = petals * 16
    for i in range(num_steps):
        angle = (2 * math.pi * i) / num_steps
        # Smooth sinusoidal radius between r_inner and r_outer
        wave = math.sin(petals * angle)
        r = r_inner + (r_outer - r_inner) * (0.5 + 0.5 * wave)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    
    d_path = f"M {points[0][0]:.2f} {points[0][1]:.2f} " + " ".join([f"L {x:.2f} {y:.2f}" for x, y in points[1:]]) + " Z"
    stroke_attr = f'stroke="{stroke_hex}" stroke-width="6"' if stroke_hex else ''
    
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f'<path d="{d_path}" fill="{fill_hex}" {stroke_attr}/>'
        f'</svg>'
    )
    png_bytes = resvg_py.svg_to_bytes(svg, width=size, height=size)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(png_bytes)
    return output_path

def generate_asymmetric_card_png(output_path: str, width_px: int, height_px: int, 
                                 r_large: int = 40, r_small: int = 12, 
                                 fill_hex: str = "#D8E2FF", stroke_hex: str = None) -> str:
    """
    Generate an M3 Expressive Asymmetric Card
    (e.g., Top-Left & Bottom-Right large radius, Top-Right & Bottom-Left small radius).
    """
    w, h = width_px, height_px
    # Path with diagonal asymmetric corner radii:
    # TL: r_large, TR: r_small, BR: r_large, BL: r_small
    d_path = (
        f"M {r_large} 0 "
        f"L {w - r_small} 0 A {r_small} {r_small} 0 0 1 {w} {r_small} "
        f"L {w} {h - r_large} A {r_large} {r_large} 0 0 1 {w - r_large} {h} "
        f"L {r_small} {h} A {r_small} {r_small} 0 0 1 0 {h - r_small} "
        f"L 0 {r_large} A {r_large} {r_large} 0 0 1 {r_large} 0 Z"
    )
    stroke_attr = f'stroke="{stroke_hex}" stroke-width="2"' if stroke_hex else ''
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f'<path d="{d_path}" fill="{fill_hex}" {stroke_attr}/>'
        f'</svg>'
    )
    png_bytes = resvg_py.svg_to_bytes(svg, width=w, height=h)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(png_bytes)
    return output_path
