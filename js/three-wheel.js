import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const canvas = document.getElementById('threeWheelCanvas');
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;

const updateSize = () => {
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
};

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.z = 4.5;

const pmremGenerator = new THREE.PMREMGenerator(renderer);
scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;

// Materials
const glossBlack = new THREE.MeshStandardMaterial({
    color: 0x050505,
    metalness: 1.0,
    roughness: 0.15,
});
const chrome = new THREE.MeshStandardMaterial({
    color: 0xffffff,
    metalness: 1.0,
    roughness: 0.1,
});
const matteBlack = new THREE.MeshStandardMaterial({
    color: 0x0a0a0a,
    metalness: 0.8,
    roughness: 0.8,
});

const wheelGroup = new THREE.Group();
const rimGroup = new THREE.Group(); // Inner group for rotation

// --- 1. Procedural Barrel (LatheGeometry) ---
const points = [];
// Define the cross-section profile of a deep concave rim
points.push(new THREE.Vector2(1.2, 0.8));   // Inner lip
points.push(new THREE.Vector2(1.3, 0.8));   
points.push(new THREE.Vector2(1.6, 0.75));  // Barrel flat
points.push(new THREE.Vector2(1.6, -0.4));  // Drop center
points.push(new THREE.Vector2(1.7, -0.5));
points.push(new THREE.Vector2(1.7, -0.7));  // Front face mount area
points.push(new THREE.Vector2(1.85, -0.8)); // Front outer lip
points.push(new THREE.Vector2(1.9, -0.85)); // Front edge
points.push(new THREE.Vector2(1.85, -0.9)); 
points.push(new THREE.Vector2(1.75, -0.9)); 
// Thicken it by mirroring back
points.push(new THREE.Vector2(1.65, -0.75));
points.push(new THREE.Vector2(1.5, -0.5));
points.push(new THREE.Vector2(1.5, 0.7));
points.push(new THREE.Vector2(1.15, 0.75));
points.push(new THREE.Vector2(1.15, 0.8));

const latheGeo = new THREE.LatheGeometry(points, 64);
const barrel = new THREE.Mesh(latheGeo, glossBlack);
barrel.rotation.x = Math.PI / 2; // Orient to face the camera
rimGroup.add(barrel);

// --- 2. Concave Spokes ---
const numSpokes = 7;
// We'll create a shape and extrude it
const spokeShape = new THREE.Shape();
spokeShape.moveTo(-0.12, 0); // Bottom width (hub)
spokeShape.lineTo(-0.06, 1.7); // Top width (rim)
spokeShape.absarc(0, 1.75, 0.06, Math.PI, 0, true); // rounded top
spokeShape.lineTo(0.12, 0);
spokeShape.lineTo(-0.12, 0);

const extrudeSettings = {
    steps: 2,
    depth: 0.25, // thickness of spoke
    bevelEnabled: true,
    bevelThickness: 0.03,
    bevelSize: 0.02,
    bevelSegments: 3
};

const spokeGeo = new THREE.ExtrudeGeometry(spokeShape, extrudeSettings);
// Center the extrusion on Z
spokeGeo.translate(0, 0, -0.125);

// The spoke needs to curve inward (concave)
// We can apply a position modifier or just tilt them
for (let i = 0; i < numSpokes; i++) {
    const spoke = new THREE.Mesh(spokeGeo, glossBlack);
    const angle = (Math.PI * 2 / numSpokes) * i;
    
    const spokeWrapper = new THREE.Group();
    // Tilt the spoke to create the concave dish effect
    spoke.rotation.x = -0.25; 
    spoke.position.z = 0.55; // Push out to meet the lip
    spoke.position.y = 0.2; // Move slightly out from absolute center

    spokeWrapper.rotation.z = angle;
    spokeWrapper.add(spoke);
    rimGroup.add(spokeWrapper);
}

// --- 3. Center Hub ---
const hubGeo = new THREE.CylinderGeometry(0.35, 0.45, 0.3, 32);
const hub = new THREE.Mesh(hubGeo, glossBlack);
hub.rotation.x = Math.PI / 2;
hub.position.z = 0.2; // Push back for deep concave
rimGroup.add(hub);

// Center Cap (Logo area)
const capGeo = new THREE.CylinderGeometry(0.15, 0.15, 0.32, 32);
const cap = new THREE.Mesh(capGeo, matteBlack);
cap.rotation.x = Math.PI / 2;
cap.position.z = 0.2;
rimGroup.add(cap);

// --- 4. Lug Nuts ---
const lugGeo = new THREE.CylinderGeometry(0.04, 0.04, 0.15, 6); // Hexagonal lugs
for (let i = 0; i < 5; i++) { // 5-lug pattern
    const lug = new THREE.Mesh(lugGeo, chrome);
    const angle = (Math.PI * 2 / 5) * i;
    const radius = 0.23;
    lug.position.x = Math.cos(angle) * radius;
    lug.position.y = Math.sin(angle) * radius;
    lug.position.z = 0.28; 
    lug.rotation.x = Math.PI / 2;
    lug.rotation.y = angle; // Align hexagon
    rimGroup.add(lug);
}

// Group hierarchy: 
// wheelGroup (handles Parallax Tilt) -> rimGroup (handles infinite rotation)
wheelGroup.add(rimGroup);
scene.add(wheelGroup);

// --- Lighting for Glint Sweep ---
const sweepLight = new THREE.SpotLight(0xffffff, 0); 
sweepLight.position.set(-6, 6, 6);
sweepLight.angle = 0.15;
sweepLight.penumbra = 0.8;
scene.add(sweepLight);

// Also add a subtle rim light
const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
fillLight.position.set(0, -2, 5);
scene.add(fillLight);

// --- Parallax Tilt Logic ---
let targetTiltX = 0;
let targetTiltY = 0;
let isHoverDevice = window.matchMedia("(hover: hover)").matches;

if (isHoverDevice) {
    document.addEventListener('mousemove', (e) => {
        // Map mouse position to -1 -> 1
        const mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        const mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
        
        const maxTilt = Math.PI / 36; // 5 degrees
        targetTiltX = mouseY * maxTilt;
        targetTiltY = mouseX * maxTilt;
    });
}

// --- Animation Loop ---
const clock = new THREE.Clock();
let glintTimer = 0;
const GLINT_INTERVAL = 6.0; 

function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta();
    
    // 1. Infinite Spin (1 revolution per 10s)
    const rotationSpeed = (Math.PI * 2) / 10;
    rimGroup.rotation.z -= rotationSpeed * delta; 
    
    // 2. Parallax Tilt (Lerp towards target)
    if (isHoverDevice) {
        wheelGroup.rotation.x += (targetTiltX - wheelGroup.rotation.x) * 5 * delta;
        wheelGroup.rotation.y += (targetTiltY - wheelGroup.rotation.y) * 5 * delta;
    }
    
    // 3. Glint Sweep
    const heroFg = document.querySelector('.hero-fg');
    if (!heroFg || heroFg.classList.contains('is-active')) {
        glintTimer += delta;
        if (glintTimer > GLINT_INTERVAL) {
            const sweepProgress = glintTimer - GLINT_INTERVAL;
            if (sweepProgress < 1.5) { 
                sweepLight.intensity = Math.sin((sweepProgress / 1.5) * Math.PI) * 100;
                sweepLight.position.x = -6 + (sweepProgress / 1.5) * 12; 
                sweepLight.lookAt(rimGroup.position);
            } else {
                sweepLight.intensity = 0;
                glintTimer = 0; 
            }
        }
    }

    renderer.render(scene, camera);
}

window.addEventListener('resize', updateSize);
updateSize(); 
animate();
