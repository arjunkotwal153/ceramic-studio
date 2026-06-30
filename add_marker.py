import re

# Update map.js
with open('js/map.js', 'r', encoding='utf-8') as f:
    js = f.read()

marker_code = """
    const markerEl = document.createElement('div');
    markerEl.className = 'map-marker-container';
    markerEl.innerHTML = `
        <div class="map-marker-glow"></div>
        <svg viewBox="0 0 24 36" class="map-marker-pin">
            <path d="M12 0C5.373 0 0 5.373 0 12c0 9 12 24 12 24s12-15 12-24c0-6.627-5.373-12-12-12zm0 17c-2.761 0-5-2.239-5-5s2.239-5 5-5 5 2.239 5 5-2.239 5-5 5z" fill="#F05A5D"/>
            <circle cx="12" cy="12" r="6" fill="#F0F3F4"/>
        </svg>
        <div class="map-marker-shadow"></div>
    `;
    const marker = new maplibregl.Marker({ element: markerEl, offset: [0, -18] })
"""

js = re.sub(r'const markerEl = document\.createElement.*?offset: \[0, -10\] \}\)', marker_code.strip(), js, flags=re.DOTALL)

with open('js/map.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update style.css
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

marker_css = """
/* MAP MARKER */
.map-marker-container {
    position: relative;
    width: 32px;
    height: 48px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    opacity: 0;
    transform: scale(0) translateY(20px);
    transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.map-marker-container.active {
    opacity: 1;
    transform: scale(1) translateY(0);
}
.map-marker-pin {
    width: 32px;
    height: 40px;
    position: relative;
    z-index: 2;
}
.map-marker-shadow {
    width: 32px;
    height: 12px;
    background: #3B4D5C;
    border-radius: 50%;
    position: absolute;
    bottom: -6px;
    z-index: 1;
}
.map-marker-glow {
    position: absolute;
    width: 40px;
    height: 40px;
    background: rgba(240, 90, 93, 0.5);
    border-radius: 50%;
    top: 5px;
    z-index: 0;
    animation: pulse-glow 2s infinite ease-out;
}
@keyframes pulse-glow {
    0% { transform: scale(0.8); opacity: 1; }
    100% { transform: scale(2.0); opacity: 0; }
}
"""

with open('css/style.css', 'a', encoding='utf-8') as f:
    f.write(marker_css)
