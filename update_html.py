with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '<div id="studio-map"></div>'
replacement = '''<div class="map-container">
            <div id="studio-map"></div>
            <div class="map-fog-overlay"></div>
        </div>'''

html = html.replace(target, replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
