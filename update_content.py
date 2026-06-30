import re

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('Detailing Colors', 'CERAMIC STUDIO')
html = html.replace('Detailing <span class="rd">Colors</span>', 'CERAMIC <span class="rd">STUDIO</span>')
html = html.replace('add number here', '9888641543, 8968123457')
html = html.replace('https://www.instagram.com/detailingcolors/', 'https://www.instagram.com/ceramic_studio.13')
html = html.replace('@detailingcolors', '@ceramic_studio.13')
html = html.replace(
    'https://www.google.com/maps/search/?api=1&query=CERAMIC+STUDIO+Shahid+Jasdev+Singh+Nagar+Ludhiana',
    'https://www.google.com/maps/place/CERAMIC+STUDIO/@30.86562,75.8290633,17z/data=!3m1!4b1!4m6!3m5!1s0x391a830025f7e3c7:0xdcde6cb1dc70d926!8m2!3d30.86562!4d75.8316382!16s%2Fg%2F11z6k88nhm?entry=ttu'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# Update js/whatsapp.js
with open('js/whatsapp.js', 'r', encoding='utf-8') as f:
    wa = f.read()

wa = wa.replace('919999999999', '919888641543')
wa = wa.replace('Detailing Colors', 'CERAMIC STUDIO')

with open('js/whatsapp.js', 'w', encoding='utf-8') as f:
    f.write(wa)


# Update js/map.js
with open('js/map.js', 'r', encoding='utf-8') as f:
    m = f.read()

m = m.replace('const STUDIO_COORDS = [75.8573, 30.9010];', 'const STUDIO_COORDS = [75.8316382, 30.86562];')
m = m.replace('''    const FULL_ROUTE_COORDS = [
        [75.8200, 30.8600],
        [75.8350, 30.8750],
        [75.8450, 30.8850],
        [75.8520, 30.8950],
        STUDIO_COORDS
    ];''', '''    const FULL_ROUTE_COORDS = [
        [75.8200, 30.8500],
        [75.8250, 30.8550],
        [75.8280, 30.8600],
        [75.8300, 30.8630],
        STUDIO_COORDS
    ];''')

with open('js/map.js', 'w', encoding='utf-8') as f:
    f.write(m)
