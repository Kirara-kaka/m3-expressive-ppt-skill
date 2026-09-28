"""
Google Material 3 Dynamic Color & Tonal Palette Engine.
Powered by Google Material Color Utilities (MCU) SchemeExpressive algorithm.
"""

from dataclasses import dataclass
from typing import Dict, Optional
from pptx.dml.color import RGBColor

from materialyoucolor.hct import Hct
from materialyoucolor.scheme.scheme_expressive import SchemeExpressive
from materialyoucolor.utils.color_utils import argb_from_rgb

def hex_to_rgb_tuple(hex_str: str) -> tuple:
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_tuple_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02X}{g:02X}{b:02X}"

def argb_to_hex(argb: int) -> str:
    r = (argb >> 16) & 0xFF
    g = (argb >> 8) & 0xFF
    b = argb & 0xFF
    return f"#{r:02X}{g:02X}{b:02X}"

@dataclass
class M3Theme:
    name: str
    is_dark: bool
    seed_hex: str
    tokens: Dict[str, str]

    def hex(self, role: str) -> str:
        """Get hex string e.g. '#385EA4'"""
        return self.tokens.get(role, "#000000")

    def rgb(self, role: str) -> RGBColor:
        """Get python-pptx RGBColor object"""
        r, g, b = hex_to_rgb_tuple(self.hex(role))
        return RGBColor(r, g, b)

    def rgb_tuple(self, role: str) -> tuple:
        """Get (r, g, b) tuple"""
        return hex_to_rgb_tuple(self.hex(role))

def generate_theme(seed_hex: str, is_dark: bool = False, name: str = "Custom Expressive") -> M3Theme:
    """
    Generate an authentic Google Material 3 Expressive theme using MCU.
    """
    r, g, b = hex_to_rgb_tuple(seed_hex)
    seed_argb = argb_from_rgb(r, g, b)
    hct_seed = Hct.from_int(seed_argb)
    scheme = SchemeExpressive(hct_seed, is_dark, 0.0)

    # Google M3 Tonal Mapping for Light and Dark Modes
    if not is_dark:
        tokens = {
            "primary": argb_to_hex(scheme.primary_palette.tone(40)),
            "on_primary": argb_to_hex(scheme.primary_palette.tone(100)),
            "primary_container": argb_to_hex(scheme.primary_palette.tone(90)),
            "on_primary_container": argb_to_hex(scheme.primary_palette.tone(10)),

            "secondary": argb_to_hex(scheme.secondary_palette.tone(40)),
            "on_secondary": argb_to_hex(scheme.secondary_palette.tone(100)),
            "secondary_container": argb_to_hex(scheme.secondary_palette.tone(90)),
            "on_secondary_container": argb_to_hex(scheme.secondary_palette.tone(10)),

            # Expressive Tertiary is Google's high-contrast complement
            "tertiary": argb_to_hex(scheme.tertiary_palette.tone(40)),
            "on_tertiary": argb_to_hex(scheme.tertiary_palette.tone(100)),
            "tertiary_container": argb_to_hex(scheme.tertiary_palette.tone(90)),
            "on_tertiary_container": argb_to_hex(scheme.tertiary_palette.tone(10)),

            # Surface elevation tiers
            "surface": argb_to_hex(scheme.neutral_palette.tone(98)),
            "surface_dim": argb_to_hex(scheme.neutral_palette.tone(87)),
            "surface_bright": argb_to_hex(scheme.neutral_palette.tone(98)),
            "surface_container_lowest": argb_to_hex(scheme.neutral_palette.tone(100)),
            "surface_container_low": argb_to_hex(scheme.neutral_palette.tone(96)),
            "surface_container": argb_to_hex(scheme.neutral_palette.tone(94)),
            "surface_container_high": argb_to_hex(scheme.neutral_palette.tone(92)),
            "surface_container_highest": argb_to_hex(scheme.neutral_palette.tone(90)),

            "on_surface": argb_to_hex(scheme.neutral_palette.tone(10)),
            "on_surface_variant": argb_to_hex(scheme.neutral_variant_palette.tone(30)),
            "outline": argb_to_hex(scheme.neutral_variant_palette.tone(50)),
            "outline_variant": argb_to_hex(scheme.neutral_variant_palette.tone(80)),

            # Inverse (for snackbars, tooltips, special overlays)
            "inverse_surface": argb_to_hex(scheme.neutral_palette.tone(20)),
            "inverse_on_surface": argb_to_hex(scheme.neutral_palette.tone(95)),
            "inverse_primary": argb_to_hex(scheme.primary_palette.tone(80)),

            # Error
            "error": argb_to_hex(scheme.error_palette.tone(40)),
            "on_error": argb_to_hex(scheme.error_palette.tone(100)),
            "error_container": argb_to_hex(scheme.error_palette.tone(90)),
            "on_error_container": argb_to_hex(scheme.error_palette.tone(10)),
        }
    else:
        tokens = {
            "primary": argb_to_hex(scheme.primary_palette.tone(80)),
            "on_primary": argb_to_hex(scheme.primary_palette.tone(20)),
            "primary_container": argb_to_hex(scheme.primary_palette.tone(30)),
            "on_primary_container": argb_to_hex(scheme.primary_palette.tone(90)),

            "secondary": argb_to_hex(scheme.secondary_palette.tone(80)),
            "on_secondary": argb_to_hex(scheme.secondary_palette.tone(20)),
            "secondary_container": argb_to_hex(scheme.secondary_palette.tone(30)),
            "on_secondary_container": argb_to_hex(scheme.secondary_palette.tone(90)),

            "tertiary": argb_to_hex(scheme.tertiary_palette.tone(80)),
            "on_tertiary": argb_to_hex(scheme.tertiary_palette.tone(20)),
            "tertiary_container": argb_to_hex(scheme.tertiary_palette.tone(30)),
            "on_tertiary_container": argb_to_hex(scheme.tertiary_palette.tone(90)),

            "surface": argb_to_hex(scheme.neutral_palette.tone(6)),
            "surface_dim": argb_to_hex(scheme.neutral_palette.tone(6)),
            "surface_bright": argb_to_hex(scheme.neutral_palette.tone(24)),
            "surface_container_lowest": argb_to_hex(scheme.neutral_palette.tone(4)),
            "surface_container_low": argb_to_hex(scheme.neutral_palette.tone(10)),
            "surface_container": argb_to_hex(scheme.neutral_palette.tone(12)),
            "surface_container_high": argb_to_hex(scheme.neutral_palette.tone(17)),
            "surface_container_highest": argb_to_hex(scheme.neutral_palette.tone(22)),

            "on_surface": argb_to_hex(scheme.neutral_palette.tone(90)),
            "on_surface_variant": argb_to_hex(scheme.neutral_variant_palette.tone(80)),
            "outline": argb_to_hex(scheme.neutral_variant_palette.tone(60)),
            "outline_variant": argb_to_hex(scheme.neutral_variant_palette.tone(30)),

            # Inverse (for snackbars, tooltips, special overlays)
            "inverse_surface": argb_to_hex(scheme.neutral_palette.tone(90)),
            "inverse_on_surface": argb_to_hex(scheme.neutral_palette.tone(20)),
            "inverse_primary": argb_to_hex(scheme.primary_palette.tone(40)),

            # Error
            "error": argb_to_hex(scheme.error_palette.tone(80)),
            "on_error": argb_to_hex(scheme.error_palette.tone(20)),
            "error_container": argb_to_hex(scheme.error_palette.tone(30)),
            "on_error_container": argb_to_hex(scheme.error_palette.tone(90)),
        }

    return M3Theme(name=name, is_dark=is_dark, seed_hex=seed_hex, tokens=tokens)

# Curated Expressive Presets
PRESET_THEMES = {
    "indigo_coral": lambda is_dark=False: generate_theme("#005AC1", is_dark, "Indigo & Coral Glow"),
    "electric_mint": lambda is_dark=False: generate_theme("#006C4A", is_dark, "Electric Mint & Charcoal"),
    "digital_lavender": lambda is_dark=False: generate_theme("#6E5676", is_dark, "Digital Lavender & Berry"),
    "warm_amber": lambda is_dark=False: generate_theme("#8C5000", is_dark, "Warm Amber & Forest"),
    "electric_violet": lambda is_dark=False: generate_theme("#5B4DFF", is_dark, "Electric Blue-Violet & Lime Glow"),
}

def get_preset_theme(preset_key: str = "indigo_coral", is_dark: bool = False) -> M3Theme:
    factory = PRESET_THEMES.get(preset_key, PRESET_THEMES["indigo_coral"])
    return factory(is_dark=is_dark)
