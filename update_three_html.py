import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add importmap
import_map = '''
    <script type="importmap">
        {
            "imports": {
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
                "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
            }
        }
    </script>
'''
if "importmap" not in html:
    html = html.replace('</title>', '</title>' + import_map)

# Replace the SVG with a canvas
canvas_html = '''<div class="alloy-counter-skew" id="heroAlloy">
                            <canvas id="threeWheelCanvas"></canvas>
                        </div>'''

html = re.sub(r'<div class="alloy-counter-skew" id="heroAlloy">.*?</div>\s*</div>', canvas_html + '\n                    </div>', html, flags=re.DOTALL)

# Add script module
if "three-wheel.js" not in html:
    html = html.replace('</body>', '    <script type="module" src="js/three-wheel.js"></script>\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Update CSS for canvas
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css += '''
#threeWheelCanvas {
    width: 100%;
    height: 100%;
    display: block;
    outline: none;
    background: transparent;
}
'''
with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Update js/main.js to remove glinting logic since we removed the div
with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = re.sub(r"document\.getElementById\('heroAlloy'\)\.classList\.add\('is-glinting'\);.*?", "", js, flags=re.DOTALL)
js = re.sub(r"document\.getElementById\('heroAlloy'\)\.classList\.remove\('is-glinting'\);.*?", "", js, flags=re.DOTALL)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)
