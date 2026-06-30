css_addition = """
/* ---------- CINEMATIC HERO ADDITIONS ---------- */
.hero-video {
    width: 100vw;
    height: 100vh;
    object-fit: cover;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
}
.cine-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: linear-gradient(to bottom, rgba(5,5,5,0.4) 0%, rgba(5,5,5,0.9) 100%);
    z-index: 2;
    pointer-events: none;
}
.hero-fg {
    z-index: 3;
}
.wordmark {
    animation: none !important; /* Override old static animation */
    opacity: 1 !important;
}
.txt-anim {
    display: inline-block;
    opacity: 0;
    transform: translateY(20px);
}
.txt-anim.c-1 { transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1); }
.txt-anim.c-2 { transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.15s; }
.txt-anim.c-3 { transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.3s; }
.txt-anim.c-4 { transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.45s; }

.hero-fg.is-active .txt-anim {
    opacity: 1;
    transform: translateY(0);
}

.alloy-wrapper {
    display: inline-block;
    position: relative;
    width: 0.85em; 
    height: 0.85em;
    vertical-align: middle;
    margin-left: 0.03em;
    overflow: hidden; /* Contains the glint */
    border-radius: 50%;
}
.alloy-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
}
.alloy-wrapper.is-rotating img {
    animation: alloyRotate 10s linear infinite;
}

.alloy-glint {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(105deg, transparent 30%, rgba(255,255,255,0.9) 50%, transparent 70%);
    opacity: 0;
    pointer-events: none;
    transform: translateX(-150%) skewX(-20deg);
}
.alloy-wrapper.is-glinting .alloy-glint {
    animation: alloyGlintSweep 2s cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
}

.scroll-indicator {
    position: absolute;
    bottom: clamp(20px, 4vh, 40px);
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
    opacity: 0; /* Handled by txt-anim logic */
}
.mouse {
    width: 22px;
    height: 38px;
    border: 2px solid rgba(255,255,255,0.3);
    border-radius: 14px;
    position: relative;
}
.scroll-wheel {
    width: 4px;
    height: 8px;
    background: rgba(255,255,255,0.6);
    border-radius: 2px;
    position: absolute;
    top: 6px;
    left: 50%;
    transform: translateX(-50%);
    animation: scrollWheel 2s infinite ease-in-out;
}
"""

with open('css/style.css', 'a', encoding='utf-8') as f:
    f.write(css_addition)

anim_addition = """
@keyframes alloyRotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
@keyframes alloyGlintSweep {
    0% { transform: translateX(-150%) skewX(-20deg); opacity: 0; }
    30% { opacity: 1; }
    100% { transform: translateX(150%) skewX(-20deg); opacity: 0; }
}
@keyframes scrollWheel {
    0% { transform: translate(-50%, 0); opacity: 1; }
    100% { transform: translate(-50%, 12px); opacity: 0; }
}
"""

with open('css/animations.css', 'a', encoding='utf-8') as f:
    f.write(anim_addition)

js_logic = """
// Cinematic Hero Orchestration
document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById('heroVideo');
    const heroFg = document.querySelector('.hero-fg');
    const alloyWrapper = document.querySelector('.alloy-wrapper');
    
    let hasTriggeredAnimations = false;

    if (video) {
        // Ensure video is playing
        video.play().catch(e => {
            console.log("Autoplay prevented:", e);
            // If autoplay fails, trigger animations anyway
            triggerHeroAnimations();
        });

        video.addEventListener('error', triggerHeroAnimations);
        
        video.addEventListener('timeupdate', () => {
            // Orchestrate the synchronization at exactly 2.5 seconds (simulated headlights fully on)
            if (video.currentTime >= 2.5 && !hasTriggeredAnimations) {
                triggerHeroAnimations();
            }
        });
        
        // Safety fallback just in case the video event never fires
        setTimeout(() => {
            if (!hasTriggeredAnimations) triggerHeroAnimations();
        }, 4000);
    } else {
        triggerHeroAnimations();
    }

    function triggerHeroAnimations() {
        if (!heroFg) return;
        hasTriggeredAnimations = true;
        heroFg.classList.add('is-active');
        
        // Start wheel rotation and the synchronized glint sweep slightly after the text fades in
        if (alloyWrapper) {
            setTimeout(() => {
                alloyWrapper.classList.add('is-rotating');
                alloyWrapper.classList.add('is-glinting');
                
                // Keep the glinting loop going every few seconds as requested
                setInterval(() => {
                    alloyWrapper.classList.remove('is-glinting');
                    void alloyWrapper.offsetWidth; // trigger reflow
                    alloyWrapper.classList.add('is-glinting');
                }, 6000);
            }, 600); 
        }
    }
});
"""

with open('js/main.js', 'a', encoding='utf-8') as f:
    f.write(js_logic)
