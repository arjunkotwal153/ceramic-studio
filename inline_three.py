import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('js/three-wheel.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the external script tag with an inline module
inline_script = f'<script type="module">\n{js}\n</script>'
html = html.replace('<script type="module" src="js/three-wheel.js"></script>', inline_script)

# Also fix the size observer in JS just in case
if 'ResizeObserver' not in html:
    # We will inject a robust size observer into the inline script
    old_update = '''const updateSize = () => {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
};'''
    new_update = '''const updateSize = () => {
    const width = canvas.parentElement.clientWidth || 100;
    const height = canvas.parentElement.clientHeight || 100;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
};
const resizeObs = new ResizeObserver(() => updateSize());
resizeObs.observe(canvas.parentElement);
'''
    html = html.replace(old_update, new_update)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
