import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the wordmark hero section using regex to be safe about spaces/newlines
html = re.sub(
    r'<div class="l1">Detailing</div>\s*<div class="l2">C<img class="alloy" src="data:image/placeholder" alt="alloy wheel">Lors</div>',
    '<div class="l1">CERAMIC</div>\n                <div class="l2">STUDI<img class="alloy" src="data:image/placeholder" alt="alloy wheel"></div>',
    html
)

# Replace 'Premium Detailing Studio' with 'Premium Ceramic Studio'
html = html.replace('Premium Car Detailing Studio', 'Premium Ceramic Studio')
html = html.replace('Premium Detailing Studio', 'Premium Ceramic Studio')

# Ensure the footer is fully updated
html = html.replace('Detailing <span class="rd">Colors</span>', 'CERAMIC <span class="rd">STUDIO</span>')
html = html.replace('Detailing Colors', 'CERAMIC STUDIO')

# Let's replace any lingering 'detailing colors' (case insensitive) just in case, but carefully.
# Actually, the copyright might still say "Detailing Colors" if it wasn't exact case, so let's do regex case insensitive
html = re.sub(r'detailing colors', 'Ceramic Studio', html, flags=re.IGNORECASE)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
