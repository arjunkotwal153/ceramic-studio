import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the wordmark l2 block
svg_wheel = '''<div class="l2">
                    <span class="txt-anim c-2">STUDI</span>
                    <div class="alloy-wrapper txt-anim c-3">
                        <div class="alloy-counter-skew" id="heroAlloy">
                            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" class="alloy-svg">
                              <defs>
                                <radialGradient id="rimGrad" cx="50%" cy="50%" r="50%">
                                  <stop offset="75%" stop-color="#111"/>
                                  <stop offset="90%" stop-color="#555"/>
                                  <stop offset="100%" stop-color="#0a0a0a"/>
                                </radialGradient>
                                <linearGradient id="spokeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                  <stop offset="0%" stop-color="#e0e0e0"/>
                                  <stop offset="50%" stop-color="#888"/>
                                  <stop offset="100%" stop-color="#333"/>
                                </linearGradient>
                              </defs>
                              
                              <circle cx="50" cy="50" r="48" fill="url(#rimGrad)" stroke="#333" stroke-width="2"/>
                              
                              <g fill="url(#spokeGrad)">
                                <path d="M48 50 L46 12 L54 12 L52 50 Z" />
                                <path d="M48 50 L46 12 L54 12 L52 50 Z" transform="rotate(36 50 50)" />
                                <path d="M48 50 L46 12 L54 12 L52 50 Z" transform="rotate(72 50 50)" />
                                <path d="M48 50 L46 12 L54 12 L52 50 Z" transform="rotate(108 50 50)" />
                                <path d="M48 50 L46 12 L54 12 L52 50 Z" transform="rotate(144 50 50)" />
                                <path d="M48 50 L46 12 L54 12 L52 50 Z" transform="rotate(180 50 50)" />
                                <path d="M48 50 L46 12 L54 12 L52 50 Z" transform="rotate(216 50 50)" />
                                <path d="M48 50 L46 12 L54 12 L52 50 Z" transform="rotate(252 50 50)" />
                                <path d="M48 50 L46 12 L54 12 L52 50 Z" transform="rotate(288 50 50)" />
                                <path d="M48 50 L46 12 L54 12 L52 50 Z" transform="rotate(324 50 50)" />
                              </g>
                              
                              <circle cx="50" cy="50" r="10" fill="#000" stroke="#444" stroke-width="1"/>
                              <!-- Lug Nuts -->
                              <circle cx="50" cy="44" r="1.5" fill="#aaa"/>
                              <circle cx="50" cy="56" r="1.5" fill="#aaa"/>
                              <circle cx="44.8" cy="47" r="1.5" fill="#aaa"/>
                              <circle cx="55.2" cy="47" r="1.5" fill="#aaa"/>
                              <circle cx="46.5" cy="54" r="1.5" fill="#aaa"/>
                              <circle cx="53.5" cy="54" r="1.5" fill="#aaa"/>
                            </svg>
                            <div class="alloy-glint" id="alloyGlint"></div>
                        </div>
                    </div>
                </div>'''

html = re.sub(r'<div class="l2">.*?</div>\s*</h1>', svg_wheel + '\n            </h1>', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Update CSS for the new structure
css_overrides = """
/* ALLOY WHEEL FIXES */
.l2 {
    display: flex;
    align-items: baseline;
    justify-content: flex-start;
}
.alloy-wrapper {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 0.8em; 
    height: 0.8em;
    margin-left: 0.02em;
    vertical-align: baseline;
    position: relative;
    top: 0.05em; /* Minor optical adjustment for baseline */
}
.alloy-counter-skew {
    width: 100%;
    height: 100%;
    transform: skewX(4deg); /* Counteract the -4deg of .wordmark */
    position: relative;
    border-radius: 50%;
    overflow: hidden; /* Constrain the glint */
}
.alloy-svg {
    width: 100%;
    height: 100%;
    display: block;
}
.alloy-counter-skew.is-rotating .alloy-svg {
    animation: alloyRotate 10s linear infinite;
}
.alloy-counter-skew.is-glinting .alloy-glint {
    animation: alloyGlintSweep 2s cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
}
"""
css += css_overrides

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Update js logic to target alloy-counter-skew instead of alloy-wrapper for rotation
with open('js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("alloyWrapper.classList.add('is-rotating')", "document.getElementById('heroAlloy').classList.add('is-rotating')")
js = js.replace("alloyWrapper.classList.add('is-glinting')", "document.getElementById('heroAlloy').classList.add('is-glinting')")
js = js.replace("alloyWrapper.classList.remove('is-glinting')", "document.getElementById('heroAlloy').classList.remove('is-glinting')")
js = js.replace("void alloyWrapper.offsetWidth;", "void document.getElementById('heroAlloy').offsetWidth;")

with open('js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)
