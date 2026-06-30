import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Using regex to safely replace the video tag block
image_html = '<img class="hero-bg" src="thar roxx.png" alt="Mahindra Thar Roxx Background">'
html = re.sub(r'<video class="hero-video".*?</video>', image_html, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('.hero-video {', '.hero-bg {')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
