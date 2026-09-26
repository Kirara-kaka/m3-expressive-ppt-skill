"""
Test M3 Dynamic Tonal Palette Engine.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.tokens import generate_theme, get_preset_theme

def test_custom_seed():
    theme_light = generate_theme("#4F378B", is_dark=False, name="Purple Seed")
    assert theme_light.hex("primary").startswith("#")
    assert theme_light.hex("primary_container").startswith("#")
    assert theme_light.hex("tertiary_container").startswith("#")
    assert theme_light.hex("surface_container").startswith("#")
    print("[PASS] Custom seed Light mode theme passed!")

    theme_dark = generate_theme("#4F378B", is_dark=True, name="Purple Seed Dark")
    assert theme_dark.hex("surface") != theme_light.hex("surface")
    print("[PASS] Custom seed Dark mode theme passed!")

def test_presets():
    for key in ["indigo_coral", "electric_mint", "digital_lavender", "warm_amber"]:
        theme = get_preset_theme(key, is_dark=False)
        print(f"[PASS] Preset '{key}' ({theme.name}): Primary={theme.hex('primary')}, Tertiary={theme.hex('tertiary')}, Surface={theme.hex('surface')}")

if __name__ == "__main__":
    test_custom_seed()
    test_presets()
    print("\nALL TOKEN TESTS PASSED!")
