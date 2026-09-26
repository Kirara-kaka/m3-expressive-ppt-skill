"""
Unified CLI Entrypoint for M3 Expressive Presentation Generator.
Usage:
    python generate_deck.py --input outline.json --output presentation.pptx [--export-png]
    python generate_deck.py --prompt "Presentation title and details" --output presentation.pptx
"""

import os
import sys
import json
import argparse
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import build_deck_from_json, build_deck_from_dict, auto_plan_from_outline, M3DeckBuilder

def export_slides_to_png(pptx_path: str, output_dir: str):
    """Invokes export_slide.ps1 via PowerShell COM to render slides to PNG."""
    ps_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "export_slide.ps1")
    if not os.path.exists(ps_script):
        print(f"Warning: {ps_script} not found. Skipping PNG export.")
        return

    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-File", ps_script,
        "-PptxPath", os.path.abspath(pptx_path),
        "-OutputDir", os.path.abspath(output_dir)
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(res.stdout)
    except subprocess.CalledProcessError as e:
        print(f"PowerPoint COM export error: {e.stderr}")

def main():
    parser = argparse.ArgumentParser(description="Google Material 3 Expressive Deck Generator")
    parser.add_argument("-i", "--input", help="Path to JSON outline file or JSON string")
    parser.add_argument("-o", "--output", default="m3_presentation.pptx", help="Target .pptx file path")
    parser.add_argument("--export-png", action="store_true", help="Automatically export slide PNGs")
    parser.add_argument("--png-dir", default=None, help="Directory to save exported slide PNGs")
    args = parser.parse_args()

    if not args.input:
        print("Error: --input JSON outline file or string is required.")
        sys.exit(1)

    # Load input
    if os.path.exists(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        try:
            data = json.loads(args.input)
        except Exception as e:
            print(f"Error parsing JSON input: {e}")
            sys.exit(1)

    print("==================================================")
    print("   Google Material 3 Expressive Presentation Gen  ")
    print("==================================================")
    
    saved_pptx = build_deck_from_json(data, args.output)
    print(f"\n[SUCCESS] Presentation ready at: {saved_pptx}")

    if args.export_png:
        png_dir = args.png_dir or os.path.join(os.path.dirname(os.path.abspath(saved_pptx)), "slides_png")
        print(f"\nExporting high-resolution slide PNGs to: {png_dir}...")
        export_slides_to_png(saved_pptx, png_dir)

if __name__ == "__main__":
    main()
