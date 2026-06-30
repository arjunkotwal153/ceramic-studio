import re

css_file = r'c:\Users\PC\Downloads\ceramic studio\css\style.css'
resp_file = r'c:\Users\PC\Downloads\ceramic studio\css\responsive.css'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update font-size with clamp
    def convert_to_clamp(match):
        original = match.group(0)
        value = float(match.group(1))
        unit = match.group(2)
        if value == 0: return original
        if unit == 'px':
            if value < 13: return original # keep small fonts as is to avoid issues
            min_val = max(12, value * 0.8)
            vw_val = value / 10
            return f"font-size: clamp({min_val:.1f}px, {vw_val:.2f}vw + 0.5rem, {value}px)"
        elif unit == 'rem':
            min_val = max(0.8, value * 0.7)
            vw_val = value * 2
            return f"font-size: clamp({min_val:.2f}rem, {vw_val:.2f}vw + 0.5rem, {value}rem)"
        return original
    
    content = re.sub(r'font-size:\s*([\d.]+)(px|rem)(?!\s*\()', convert_to_clamp, content)

    # 2. Update 100vh to 100svh
    content = content.replace('height: 100vh;', 'height: 100svh;')
    content = content.replace('min-height: 100vh;', 'min-height: 100svh;')
    content = content.replace('width: 100vw;', 'width: 100%;')

    # 3. Prevent horizontal scrolling
    if 'overflow-x: hidden' in content:
        content = content.replace('overflow-x: hidden;', 'overflow-x: hidden; max-width: 100vw;')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

process_file(css_file)
process_file(resp_file)

# Specific fixes for style.css
with open(css_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix .alloy
alloy_old = """.alloy {
            width: .96em;
            height: .96em;
            display: inline-block;
            vertical-align: middle;
            margin: 0 .03em;
            animation: wheelSpin 14s linear infinite;
            filter: drop-shadow(0 6px 16px rgba(0, 0, 0, .6));
            transform-origin: center
        }"""
alloy_new = """.alloy {
            width: .96em;
            height: .96em;
            display: inline-block;
            vertical-align: middle;
            margin: 0 .03em;
            animation: wheelSpin 14s linear infinite;
            filter: drop-shadow(0 6px 16px rgba(0, 0, 0, .6));
            transform-origin: center;
            flex-shrink: 0;
            max-width: 100%;
        }
        .alloy canvas {
            width: 100% !important;
            height: 100% !important;
            object-fit: contain;
            display: block;
        }"""
content = content.replace(alloy_old, alloy_new)

# Make images responsive
content += "\nimg { max-width: 100%; height: auto; }\n.car-img, .hero-bg { object-fit: cover; }\n"

with open(css_file, 'w', encoding='utf-8') as f:
    f.write(content)

# Specific fixes for responsive.css
with open(resp_file, 'a', encoding='utf-8') as f:
    f.write("""
@media(max-width:768px) {
    nav { padding: 12px 20px; }
    .hero-fg { padding: 0 16px 40px; }
    .hero { justify-content: center; }
    .hero-stats { gap: 20px; }
    .cta-row { gap: 10px; }
}
""")
print("Done")
