"""
Google Material Symbols (Rounded) Asset & Icon Manager.
Directly interfaces with Google Material Symbols repository / CDN to provide
pixel-perfect, dynamically recolored vector icons for PowerPoint slides.
"""

import os
import urllib.request
import re
from typing import Optional
import resvg_py

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS_CACHE_DIR = os.path.join(BASE_DIR, "assets", "icons")
RENDERED_CACHE_DIR = os.path.join(ICONS_CACHE_DIR, "rendered")

os.makedirs(ICONS_CACHE_DIR, exist_ok=True)
os.makedirs(RENDERED_CACHE_DIR, exist_ok=True)

# Google Official Static CDN endpoint for Material Symbols Rounded
GOOGLE_SYMBOLS_CDN = "https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsrounded/{name}/default/24px.svg"

# Semantic synonyms map for intuitive icon discovery
SEMANTIC_ICON_MAP = {
    # AI & Innovation
    "ai": "auto_awesome",
    "sparkle": "auto_awesome",
    "magic": "auto_awesome",
    "brain": "psychology",
    "idea": "lightbulb",
    "innovation": "lightbulb",
    "smart": "smart_toy",

    # Data & Analytics
    "chart": "insights",
    "analytics": "analytics",
    "data": "monitoring",
    "trend": "trending_up",
    "growth": "trending_up",
    "metrics": "query_stats",
    "dashboard": "dashboard",
    "bento": "grid_view",
    "grid": "grid_view",

    # Quality & Security
    "check": "verified",
    "verified": "verified",
    "security": "security",
    "shield": "shield",
    "award": "workspace_premium",
    "star": "star",

    # Execution & Strategy
    "rocket": "rocket_launch",
    "launch": "rocket_launch",
    "target": "track_changes",
    "goal": "flag",
    "speed": "speed",
    "fast": "bolt",
    "bolt": "bolt",
    "gear": "settings",
    "settings": "tune",
    "layers": "layers",
    "architecture": "account_tree",

    # People & Global
    "team": "diversity_3",
    "people": "group",
    "user": "person",
    "global": "public",
    "cloud": "cloud",
    "devices": "devices",
    "code": "code",
    "palette": "palette",
}

def resolve_icon_name(keyword_or_name: str) -> str:
    """Resolve a semantic keyword or icon name to a Google Material Symbol name."""
    clean = keyword_or_name.strip().lower().replace("-", "_").replace(" ", "_")
    return SEMANTIC_ICON_MAP.get(clean, clean)

def fetch_material_symbol_svg(icon_name: str) -> Optional[str]:
    """
    Fetch Material Symbol Rounded SVG from local cache or Google CDN.
    Returns the raw SVG XML string.
    """
    canonical_name = resolve_icon_name(icon_name)
    local_svg_path = os.path.join(ICONS_CACHE_DIR, f"{canonical_name}.svg")

    if os.path.exists(local_svg_path):
        with open(local_svg_path, "r", encoding="utf-8") as f:
            return f.read()

    # Fetch from Google CDN
    url = GOOGLE_SYMBOLS_CDN.format(name=canonical_name)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            svg_content = resp.read().decode("utf-8")
            with open(local_svg_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
            return svg_content
    except Exception as e:
        # Fallback to auto_awesome if icon not found
        if canonical_name != "auto_awesome":
            return fetch_material_symbol_svg("auto_awesome")
        return None

def get_recolored_icon_png(icon_name_or_keyword: str, hex_color: str, size: int = 512) -> str:
    """
    Get a high-DPI transparent PNG of a Google Material Symbol,
    re-colored to the specified M3 hex color.
    Returns the absolute path to the cached PNG.
    """
    canonical_name = resolve_icon_name(icon_name_or_keyword)
    clean_hex = hex_color.lstrip("#").upper()
    cached_png_path = os.path.join(RENDERED_CACHE_DIR, f"{canonical_name}_{clean_hex}_{size}.png")

    if os.path.exists(cached_png_path):
        return cached_png_path

    svg_content = fetch_material_symbol_svg(canonical_name)
    if not svg_content:
        raise ValueError(f"Failed to fetch Material Symbol for: {canonical_name}")

    # Inject target fill color
    # Google symbols have <path d="..." .../>
    if "fill=" in svg_content:
        recolored_svg = re.sub(r'fill="[^"]+"', f'fill="#{clean_hex}"', svg_content)
    else:
        recolored_svg = svg_content.replace("<path ", f'<path fill="#{clean_hex}" ')

    # Render with resvg_py at requested dimensions
    png_bytes = resvg_py.svg_to_bytes(recolored_svg, width=size, height=size)
    with open(cached_png_path, "wb") as f:
        f.write(png_bytes)

    return cached_png_path
