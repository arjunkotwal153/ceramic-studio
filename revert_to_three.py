import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add importmap if missing
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

# Replace iframe with canvas
canvas_html = '''<div class="alloy-counter-skew" id="heroAlloy">
                            <canvas id="threeWheelCanvas"></canvas>
                        </div>'''
html = re.sub(r'<div class="alloy-counter-skew" id="heroAlloy">.*?</div>\s*</div>', canvas_html + '\n                    </div>', html, flags=re.DOTALL)

# Add script module
if "three-wheel.js" not in html:
    html = html.replace('</body>', '    <script type="module" src="js/three-wheel.js"></script>\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
