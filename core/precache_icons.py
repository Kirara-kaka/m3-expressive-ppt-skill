"""
Pre-cache core Material Symbols Rounded icons locally for offline reliability.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.icon_manager import fetch_material_symbol_svg, SEMANTIC_ICON_MAP

def precache_all():
    unique_symbols = sorted(list(set(SEMANTIC_ICON_MAP.values())))
    print(f"Pre-caching {len(unique_symbols)} core Material Symbols...")
    success_count = 0
    for symbol in unique_symbols:
        svg = fetch_material_symbol_svg(symbol)
        if svg:
            success_count += 1
            print(f"  [OK] {symbol}")
        else:
            print(f"  [FAIL] {symbol}")
    print(f"\nSuccessfully cached {success_count}/{len(unique_symbols)} official Material Symbols!")

if __name__ == "__main__":
    precache_all()
