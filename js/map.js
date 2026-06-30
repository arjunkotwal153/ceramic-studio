document.addEventListener("DOMContentLoaded", () => {
    const STUDIO_COORDS = [75.8316382, 30.86562];
    
    // Smooth bezier-like curve points leading to the studio for the glowing route
    const FULL_ROUTE_COORDS = [
        [75.8200, 30.8500],
        [75.8250, 30.8550],
        [75.8280, 30.8600],
        [75.8300, 30.8630],
        STUDIO_COORDS
    ];

    const map = new maplibregl.Map({
        container: 'studio-map',
        style: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
        center: [0, 20], 
        zoom: 2,
        pitch: 0,
        bearing: 0,
        interactive: false,
        attributionControl: false
    });

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
        .setLngLat(STUDIO_COORDS);

    let animationHasPlayed = false;
    let floatAnimationId = null;
    let routeAnimationId = null;

    map.on('style.load', () => {
        // Set Map Lighting for 3D depth
        map.setLight({
            anchor: 'viewport',
            color: '#ffffff',
            intensity: 0.35,
            position: [1.15, 210, 30] // Soft directional lighting
        });

        // Tweak existing layers to match the #0F0F0F luxury palette
        const layers = map.getStyle().layers;
        layers.forEach(layer => {
            if (layer.id.includes('background') || layer.id.includes('water')) {
                if (layer.type === 'background') map.setPaintProperty(layer.id, 'background-color', '#0F0F0F');
                if (layer.type === 'fill') map.setPaintProperty(layer.id, 'fill-color', '#0F0F0F');
            }
            if (layer.id.includes('road')) {
                // Dimmer roads, brighter highways
                const isHighway = layer.id.includes('highway') || layer.id.includes('primary');
                if (layer.type === 'line') map.setPaintProperty(layer.id, 'line-color', isHighway ? '#8A8A8A' : '#666666');
            }
            // Hide the default flat building layer from Carto Dark Matter
            if (layer.id.includes('building')) {
                map.setLayoutProperty(layer.id, 'visibility', 'none');
            }
        });

        // Add 3D Extruded Buildings
        if (map.getSource('carto')) {
            map.addLayer({
                'id': '3d-buildings',
                'source': 'carto',
                'source-layer': 'building',
                'type': 'fill-extrusion',
                'minzoom': 14,
                'paint': {
                    'fill-extrusion-color': '#2B2B2B',
                    // Use coalesce to fallback if height is missing (assign random-ish height based on polygon for visual effect if needed, but 20 is a safe fallback)
                    'fill-extrusion-height': ['coalesce', ['get', 'render_height'], ['get', 'height'], 20],
                    'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], ['get', 'min_height'], 0],
                    'fill-extrusion-opacity': 1.0
                }
            });
        }

        // Setup Route Source
        map.addSource('route', {
            type: 'geojson',
            data: {
                type: 'Feature',
                properties: {},
                geometry: {
                    type: 'LineString',
                    coordinates: [FULL_ROUTE_COORDS[0]] // Starts empty
                }
            }
        });

        // Route Glow Layer
        map.addLayer({
            id: 'route-glow',
            type: 'line',
            source: 'route',
            layout: {
                'line-join': 'round',
                'line-cap': 'round'
            },
            paint: {
                'line-color': '#E8462A',
                'line-width': 14,
                'line-opacity': 0.3,
                'line-blur': 10
            }
        });

        // Route Core Layer
        map.addLayer({
            id: 'route-core',
            type: 'line',
            source: 'route',
            layout: {
                'line-join': 'round',
                'line-cap': 'round'
            },
            paint: {
                'line-color': '#E8462A',
                'line-width': 4
            }
        });
    });

    // Animate the route drawing (GEOlayers style)
    const animateRoute = () => {
        let startTime = null;
        const duration = 4000; // 4 seconds to draw

        const step = (timestamp) => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            
            // Calculate current coordinates array based on progress
            const maxIndex = (FULL_ROUTE_COORDS.length - 1) * progress;
            const currentCoords = [];
            
            for (let i = 0; i <= Math.floor(maxIndex); i++) {
                currentCoords.push(FULL_ROUTE_COORDS[i]);
            }
            
            // Interpolate the last segment for smooth drawing
            if (Math.floor(maxIndex) < FULL_ROUTE_COORDS.length - 1) {
                const nextIndex = Math.floor(maxIndex) + 1;
                const p1 = FULL_ROUTE_COORDS[Math.floor(maxIndex)];
                const p2 = FULL_ROUTE_COORDS[nextIndex];
                const segmentProgress = maxIndex - Math.floor(maxIndex);
                
                const interpX = p1[0] + (p2[0] - p1[0]) * segmentProgress;
                const interpY = p1[1] + (p2[1] - p1[1]) * segmentProgress;
                currentCoords.push([interpX, interpY]);
            }
            
            map.getSource('route').setData({
                type: 'Feature',
                properties: {},
                geometry: {
                    type: 'LineString',
                    coordinates: currentCoords
                }
            });

            if (progress < 1) {
                routeAnimationId = requestAnimationFrame(step);
            }
        };
        routeAnimationId = requestAnimationFrame(step);
    };

    // Cinematic Flight Sequence
    const playCinematicFlight = () => {
        if (animationHasPlayed) return;
        animationHasPlayed = true;

        // Long, smooth 8-second cinematic fly-in
        map.flyTo({
            center: STUDIO_COORDS,
            zoom: 17.5,
            pitch: 75,
            bearing: -35,
            speed: 0.35, // Slows down the flight significantly
            curve: 1.1,
            essential: true,
            duration: 8000 // Force 8 seconds
        });
        
        // Start drawing the route halfway through the flight
        setTimeout(() => {
            animateRoute();
        }, 4000);

        map.once('moveend', () => {
            marker.addTo(map);
            // Delay marker glow slightly for dramatic effect
            setTimeout(() => {
                markerEl.classList.add('active');
            }, 300);
            
            // Enable user interactivity
            map.dragPan.enable();
            map.scrollZoom.enable();
            map.boxZoom.enable();
            map.dragRotate.enable();
            map.keyboard.enable();
            map.doubleClickZoom.enable();
            map.touchZoomRotate.enable();

            startFloatingAnimation();
        });
    };

    // Continuous subtle floating motion
    const startFloatingAnimation = () => {
        let startTime = performance.now();
        let initialBearing = map.getBearing();
        let initialPitch = map.getPitch();

        const animate = (timestamp) => {
            const elapsed = timestamp - startTime;
            
            if (!map.isZooming() && !map.isMoving() && !map.isRotating()) {
                const newBearing = initialBearing + Math.sin(elapsed / 8000) * 4;
                const newPitch = initialPitch + Math.sin(elapsed / 10000) * 3;
                
                map.setBearing(newBearing);
                map.setPitch(newPitch);
            } else {
                startTime = timestamp;
                initialBearing = map.getBearing();
                initialPitch = map.getPitch();
            }
            
            floatAnimationId = requestAnimationFrame(animate);
        };
        floatAnimationId = requestAnimationFrame(animate);
    };

    const studioSection = document.getElementById('studio-section');
    if (studioSection) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !animationHasPlayed) {
                    playCinematicFlight();
                }
            });
        }, { threshold: 0.4 });
        
        observer.observe(studioSection);
    }
});
