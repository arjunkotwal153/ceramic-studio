import re

with open('css/responsive.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix the map-container and hero-bg on mobile
mobile_fixes = """
            .studio::before { display: none !important; }
            
            .map-container {
                position: relative !important;
                width: 100% !important;
                height: 350px !important;
            }
            
            .hero-bg {
                object-position: 70% center !important; /* shift background image right */
            }
"""

# Insert these fixes inside the max-width: 820px block
if '.map-container' not in css:
    css = css.replace('.studio::before {', mobile_fixes + '\n            /* old ::before */\n            .studio-old-before {')

with open('css/responsive.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Update font size in style.css for .l1
with open('css/style.css', 'r', encoding='utf-8') as f:
    style_css = f.read()

style_css = style_css.replace('font-size: clamp(2.7rem, 10vw, 7.4rem);', 'font-size: clamp(3.2rem, 15vw, 7.4rem);')
style_css = style_css.replace('object-position: center right !important;', '') # clean up if it was there globally

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(style_css)
