import re

# Read the file
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# I want to take the background and text-fill-color properties from .l1 and apply them to .l1 .txt-anim
# Let's find the main .l1 block
match = re.search(r'\.l1\s*\{([^}]+)\}', css)
if match:
    props = match.group(1)
    # We want to extract font-size to keep it on .l1, but move the background stuff to .txt-anim
    # Actually, simpler: just remove text-fill-color transparent from .l1, or make .txt-anim inherit it.
    
    # If I just append a rule at the bottom of the CSS file:
    # .l1 .txt-anim { background: inherit; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
    
    # But wait, if .l1 has the gradient, then .l1 .txt-anim inheriting background might not work perfectly because inline-blocks have their own box.
    # The safest fix:
    # Add a specific rule to the bottom of the CSS
    fix_css = """
/* Fix text gradient clipping for span */
.l1 .txt-anim {
    background: linear-gradient(180deg, #fff, #e2e2e4 45%, #9a9aa0 56%, #f2f2f4);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.l1 {
    -webkit-text-fill-color: initial; /* Remove from parent so it doesn't turn invisible if child fails */
}
"""
    with open('css/style.css', 'a', encoding='utf-8') as f:
        f.write(fix_css)

