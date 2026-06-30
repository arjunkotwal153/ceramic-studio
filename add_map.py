import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add dependencies to <head>
if 'maplibre-gl.css' not in html:
    html = html.replace('</head>', '    <!-- MapLibre GL JS -->\n    <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet" />\n    <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>\n</head>')

# Add map container inside <section class="studio">
if '<div id="studio-map"></div>' not in html:
    html = html.replace('<section class="studio">', '<section class="studio" id="studio-section">\n        <div id="studio-map"></div>')

# Add map.js to scripts
if 'js/map.js' not in html:
    html = html.replace('<script src="js/whatsapp.js" defer></script>', '<script src="js/whatsapp.js" defer></script>\n    <script src="js/map.js" defer></script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
