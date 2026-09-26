import urllib.request
import resvg_py

url = 'https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsrounded/auto_awesome/default/24px.svg'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=5) as resp:
    svg_data = resp.read().decode('utf-8')

colored_svg = svg_data.replace('<path ', '<path fill="#005AC1" ')
png_bytes = resvg_py.svg_to_bytes(colored_svg, width=512, height=512)
with open('test_resvg_icon.png', 'wb') as f:
    f.write(png_bytes)
print(f'Rendered icon to test_resvg_icon.png ({len(png_bytes)} bytes)!')
