"""
Google Material 3 Shape & Layout Design Tokens.
Directly aligned with Google Material Design 3 specifications (md-sys-shape).
"""

# Google M3 Corner Radii (dp)
M3_CORNER_NONE = 0
M3_CORNER_EXTRA_SMALL = 4
M3_CORNER_SMALL = 8
M3_CORNER_MEDIUM = 12
M3_CORNER_LARGE = 16
M3_CORNER_EXTRA_LARGE = 28  # 28dp: The iconic M3 Expressive card radius
M3_CORNER_FULL = 9999       # Full Pill / Capsule radius

# Google M3 Spacing Tokens (dp)
M3_SPACE_COMPACT = 8
M3_SPACE_MEDIUM = 16
M3_SPACE_LARGE = 24
M3_SPACE_EXTRA_LARGE = 32

# Slide Dimensions (16:9 widescreen in Inches)
SLIDE_WIDTH_INCHES = 13.333
SLIDE_HEIGHT_INCHES = 7.5

def calculate_drawingml_adj(width, height, target_corner_dp):
    """
    Calculate the exact DrawingML adjustment value (val 0..50000)
    for a rounded rectangle (roundRect) based on container dimensions and target dp.
    
    Robust against both raw inch floats (e.g. 5.6) and python-pptx EMU Lengths (e.g. 5120640).
    """
    if target_corner_dp >= M3_CORNER_FULL:
        return 50000
    
    # Auto-detect EMU vs Inches: If value > 500, it's definitely in EMUs (1 inch = 914400 EMUs)
    w_in = (width / 914400.0) if width > 500 else float(width)
    h_in = (height / 914400.0) if height > 500 else float(height)
    
    min_side = min(w_in, h_in)
    if min_side <= 0:
        return 0
    
    # In a 13.333" x 7.5" slide (1920x1080 equivalent):
    # 28dp in a 1080p canvas corresponds to ~0.25 - 0.35 inches of visual curve.
    # DrawingML formula: radius = min_side * (adj / 100000)
    # Target radius for 28dp: ~0.36 inches
    target_radius_in = (target_corner_dp / 72.0) * 0.95
    
    adj = int((target_radius_in / min_side) * 100000)
    # Ensure prominent, visible Expressive rounded corners
    return max(4000, min(50000, adj))
