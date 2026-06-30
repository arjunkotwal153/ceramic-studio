import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove importmap
html = re.sub(r'<script type="importmap">.*?</script>', '', html, flags=re.DOTALL)

# Replace canvas with iframe
iframe_html = '''<div class="alloy-counter-skew" id="heroAlloy">
                            <iframe title="Rays Gramlights 57CR" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/47063c38bdaa46ebaf2d2af2079c7118/embed?autostart=1&transparent=1&ui_controls=0&ui_infos=0&ui_watermark=0&ui_stop=0&scrollwheel=0" style="width: 140%; height: 140%; pointer-events: none; position: absolute; top: -20%; left: -20%;"> </iframe>
                            <div class="alloy-glint" id="alloyGlint"></div>
                        </div>'''

html = re.sub(r'<div class="alloy-counter-skew" id="heroAlloy">.*?</div>\s*</div>', iframe_html + '\n                    </div>', html, flags=re.DOTALL)

# Remove three-wheel.js script
html = html.replace('<script type="module" src="js/three-wheel.js"></script>', '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Add back js logic for glinting
with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Instead of regex replacement, let's just make sure the block looks like it did before
js_replacement = """
            setTimeout(() => {
                const heroAlloy = document.getElementById('heroAlloy');
                if(heroAlloy) {
                    heroAlloy.classList.add('is-rotating');
                    heroAlloy.classList.add('is-glinting');
                    
                    setInterval(() => {
                        heroAlloy.classList.remove('is-glinting');
                        void heroAlloy.offsetWidth; // trigger reflow
                        heroAlloy.classList.add('is-glinting');
                    }, 6000);
                }
            }, 600); 
"""

# We'll just append a cleanup replacing the old setTimeout block in main.js
# First find the setTimeout block
js = re.sub(r'setTimeout\(\(\) => \{\n\s*alloyWrapper\.classList\.add.*?600\);\s*\}', js_replacement, js, flags=re.DOTALL)

# Wait, in the previous step I already changed alloyWrapper to document.getElementById('heroAlloy').
# Let's just rewrite the triggerHeroAnimations function
new_trigger_func = """
    function triggerHeroAnimations() {
        if (!heroFg) return;
        hasTriggeredAnimations = true;
        heroFg.classList.add('is-active');
        
        setTimeout(() => {
            const heroAlloy = document.getElementById('heroAlloy');
            if(heroAlloy) {
                heroAlloy.classList.add('is-rotating');
                heroAlloy.classList.add('is-glinting');
                
                setInterval(() => {
                    heroAlloy.classList.remove('is-glinting');
                    void heroAlloy.offsetWidth; 
                    heroAlloy.classList.add('is-glinting');
                }, 6000);
            }
        }, 600);
    }
"""
js = re.sub(r'function triggerHeroAnimations\(\) \{.*', new_trigger_func + '\n});', js, flags=re.DOTALL)

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Delete three-wheel.js if it exists
if os.path.exists('js/three-wheel.js'):
    os.remove('js/three-wheel.js')
