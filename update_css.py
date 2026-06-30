import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Update .studio background to remove the graffiti image since the map is there
css = re.sub(r'background:\s*#[0-9a-fA-F]+\s*var\(--graffiti\)[^;}]*', 'background: #101010', css)

# Add #studio-map and marker CSS
map_css = """
#studio-map {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: auto;
}

/* Customize maplibre elements to hide them if desired, or keep them minimal */
.maplibregl-control-container {
    display: none;
}
"""

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css + '\n' + map_css)

anim_css = """
.map-marker {
    width: 20px;
    height: 20px;
    background-color: var(--red);
    border-radius: 50%;
    position: relative;
    box-shadow: 0 0 10px rgba(232, 70, 42, 0.8);
    opacity: 0; /* Hidden before flight ends */
    transition: opacity 1s ease;
}

.map-marker.active {
    opacity: 1;
}

.map-marker.active::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 100%;
    background-color: var(--red);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: markerPulse 2s infinite;
}

@keyframes markerPulse {
    0% {
        width: 100%;
        height: 100%;
        opacity: 0.8;
    }
    100% {
        width: 300%;
        height: 300%;
        opacity: 0;
    }
}
"""
with open('css/animations.css', 'a', encoding='utf-8') as f:
    f.write('\n' + anim_css)
