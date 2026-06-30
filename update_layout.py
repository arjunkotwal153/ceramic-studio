import re
import os

css_file = r'c:\Users\PC\Downloads\ceramic studio\css\style.css'
resp_file = r'c:\Users\PC\Downloads\ceramic studio\css\responsive.css'

with open(css_file, 'r', encoding='utf-8') as f:
    style_content = f.read()

with open(resp_file, 'r', encoding='utf-8') as f:
    resp_content = f.read()

# Replace fixed width with max-width
# E.g., width: 1120px; -> max-width: 1120px; width: 100%;
def fix_width(match):
    val = match.group(1)
    if val == '100%': return match.group(0) # safe check
    return f"max-width: {val}px; width: 100%"

style_content = re.sub(r'width:\s*(\d+)px', fix_width, style_content)

# Add object-fit cover to images if they are in .car-img or others
# Wait, we already replaced 100vw/vh for hero.
# For .thumb img or other images
style_content += "\nimg { max-width: 100%; height: auto; object-fit: cover; }\n"

# Navbar on mobile: add to responsive.css
navbar_mobile = """
@media(max-width:768px) {
    nav {
        padding: 12px 20px;
    }
    .brand {
        font-size: clamp(12px, 3vw, 15px);
    }
    .brand .mk {
        width: 24px;
        height: 24px;
        font-size: 14px;
    }
    .nav-cta {
        padding: 8px 16px;
        font-size: 11px;
    }
    .hero-fg {
        padding: 0 16px 40px;
    }
    .hero {
        justify-content: center;
    }
}
"""

resp_content += navbar_mobile

# Add a fix for max-width on body/html overflow
style_content = style_content.replace('overflow-x: hidden;', 'overflow-x: hidden; max-width: 100vw;')

with open(css_file, 'w', encoding='utf-8') as f:
    f.write(style_content)

with open(resp_file, 'w', encoding='utf-8') as f:
    f.write(resp_content)

print("Updated widths, navbar, and containers")
