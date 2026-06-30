import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Change the material color to white
html = html.replace('color: 0x2a2a2a,', 'color: 0xffffff,')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
