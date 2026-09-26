"""
Unit tests for Material Symbols Icon Manager.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_manager import (
    resolve_icon_name,
    fetch_material_symbol_svg,
    get_recolored_icon_png
)

def test_semantic_resolution():
    assert resolve_icon_name("ai") == "auto_awesome"
    assert resolve_icon_name("chart") == "insights"
    assert resolve_icon_name("growth") == "trending_up"
    assert resolve_icon_name("bento") == "grid_view"
    print("[PASS] Semantic resolution passed!")

def test_fetch_and_render():
    test_cases = [
        ("ai", "#005AC1"),
        ("bento", "#191C20"),
        ("growth", "#984061"),
        ("check", "#006C4A"),
        ("rocket", "#BA1A1A"),
    ]
    for kw, hex_clr in test_cases:
        png_path = get_recolored_icon_png(kw, hex_clr, size=256)
        assert os.path.exists(png_path), f"File {png_path} does not exist"
        size_bytes = os.path.getsize(png_path)
        assert size_bytes > 500, f"Rendered icon file too small: {size_bytes} bytes"
        print(f"[PASS] Rendered '{kw}' ({resolve_icon_name(kw)}) in {hex_clr} -> {os.path.basename(png_path)} ({size_bytes} bytes)")

if __name__ == "__main__":
    test_semantic_resolution()
    test_fetch_and_render()
    print("\nALL ICON TESTS PASSED!")
