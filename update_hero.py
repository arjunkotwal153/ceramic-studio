import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace the cine block with video
cine_replacement = '''<div class="cine">
            <video class="hero-video" id="heroVideo" autoplay muted loop playsinline poster="data:image/placeholder">
                <source src="placeholder-defender.mp4" type="video/mp4">
            </video>
            <div class="cine-overlay"></div>
        </div>'''
# Careful non-greedy match to grab the whole cine div
html = re.sub(r'<div class="cine">.*?</div>\s*</div>', cine_replacement, html, flags=re.DOTALL)

# 2. Replace the wordmark
wordmark_replacement = '''<h1 class="wordmark" id="heroWordmark">
                <div class="l1"><span class="txt-anim c-1">CERAMIC</span></div>
                <div class="l2">
                    <span class="txt-anim c-2">STUDI</span>
                    <div class="alloy-wrapper txt-anim c-3">
                        <img class="alloy" id="heroAlloy" src="data:image/placeholder" alt="alloy wheel">
                        <div class="alloy-glint" id="alloyGlint"></div>
                    </div>
                </div>
            </h1>'''
html = re.sub(r'<h1 class="wordmark">.*?</h1>', wordmark_replacement, html, flags=re.DOTALL)

# 3. Add scroll indicator after hero-stats
# Currently it ends with:
#         <div class="hero-stats">...</div>
#     </div>
# </header>
scroll_indicator = '''        </div>
        
        <div class="scroll-indicator txt-anim c-4">
            <div class="mouse">
                <div class="scroll-wheel"></div>
            </div>
        </div>
    </div>
</header>'''

html = re.sub(r'\s*</div>\s*</header>', '\n' + scroll_indicator, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
