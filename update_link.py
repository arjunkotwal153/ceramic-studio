import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the old Google Maps link with the new shortlink
old_link = 'href="https://www.google.com/maps/search/?api=1&query=Detailing+Colors+Shahid+Jasdev+Singh+Nagar+Ludhiana"'
new_link = 'href="https://maps.app.goo.gl/4vXbQ9eAiLookemB9"'

if old_link in html:
    html = html.replace(old_link, new_link)
else:
    # Fallback regex in case of slight formatting differences
    html = re.sub(r'href="https://www\.google\.com/maps/search/\?api=1[^"]+"', new_link, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
