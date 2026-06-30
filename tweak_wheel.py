import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Increase wrapper size
css = css.replace('width: 0.8em;', 'width: 0.86em;')
css = css.replace('height: 0.8em;', 'height: 0.86em;')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Increase material brightness
html = html.replace('color: 0x050505,', 'color: 0x2a2a2a,') # Dark metallic grey
html = html.replace('metalness: 1.0,', 'metalness: 0.9,') # Slightly less metallic for better diffuse visibility

# Increase exposure
html = html.replace('renderer.toneMappingExposure = 1.0;', 'renderer.toneMappingExposure = 1.7;')

# Adjust lighting
old_light = '''const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
fillLight.position.set(0, -2, 5);
scene.add(fillLight);'''

new_light = '''const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
scene.add(ambientLight);
const fillLight = new THREE.DirectionalLight(0xffffff, 2.0);
fillLight.position.set(-2, 4, 5);
scene.add(fillLight);
const rimLight = new THREE.PointLight(0xffffff, 50);
rimLight.position.set(3, -3, 2);
scene.add(rimLight);
'''

html = html.replace(old_light, new_light)

# Also scale the geometry up slightly within the camera view
html = html.replace('camera.position.z = 4.5;', 'camera.position.z = 4.2;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
