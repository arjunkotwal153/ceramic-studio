const WHATSAPP_NUMBER = "919876543210"; // demo WhatsApp number

        const nav = document.getElementById('nav');
        addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 40));
        const io = new IntersectionObserver((es) => { es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }) }, { threshold: .16 });
        document.querySelectorAll('.reveal').forEach(el => io.observe(el));
        const cer = document.getElementById('ceramic');
        new IntersectionObserver((es) => { es.forEach(e => { if (e.isIntersecting) cer.classList.add('in'); }) }, { threshold: .3 }).observe(cer);
        document.getElementById('submitBtn').addEventListener('click', () => {
            const v = id => document.getElementById(id).value.trim();
            const name = v('name'), brand = v('brand'), model = v('model'), service = document.getElementById('service').value, time = v('time');
            if (!name || !brand) { alert('Please add at least your name and car brand so we can confirm your slot.'); return; }
            const msg = `Hi Detailing Colors! I'd like to book a service.\n\nName: ${name}\nCar: ${brand} ${model}\nService: ${service}\nPreferred time: ${time || 'flexible'}\n\nPlease confirm my slot.`;
            window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`, '_blank');
        });
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
        
        setTimeout(() => {
            const heroAlloy = document.getElementById('heroAlloy');
            if(heroAlloy) {
                heroAlloy.classList.add('is-rotating');
                heroAlloy.classList.add('is-glinting');
                
                setInterval(() => {
                    heroAlloy.classList.remove('is-glinting');
                    void heroAlloy.offsetWidth; 
                    heroAlloy.classList.add('is-glinting');
                }, 6000);
            }
        }, 600);
    }

});