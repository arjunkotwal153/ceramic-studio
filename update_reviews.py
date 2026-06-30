import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define the new marquee HTML
marquee_html = """
    <!-- ============ TESTIMONIALS (LOOPING) ============ -->
    <section class="sec-white testi-marquee-sec" id="reviews">
        <div class="testi-header">
            <div class="gbadge">Rated <b>5.0</b> ★ on Google · Ludhiana</div>
        </div>
        <div class="testi-marquee">
            <div class="testi-track">
                <!-- Group 1 -->
                <div class="testi-track-inner">
                    <div class="testi-card">
                        <div class="stars">★★★★★</div>
                        <p>“Picked up my car looking like it just left the showroom. The shine genuinely turned heads — worth every rupee.”</p>
                        <div class="who">Chirag Naini<small>Verified Google review</small></div>
                    </div>
                    <div class="testi-card">
                        <div class="stars">★★★★★</div>
                        <p>“Incredible attention to detail. My 5 series looks better than the day I bought it. The ceramic coating is flawless.”</p>
                        <div class="who">Gurpreet Singh<small>Verified Google review</small></div>
                    </div>
                    <div class="testi-card">
                        <div class="stars">★★★★★</div>
                        <p>“Professional team and premium setup. The paint correction removed all swirl marks completely.”</p>
                        <div class="who">Rohan Kapoor<small>Verified Google review</small></div>
                    </div>
                    <div class="testi-card">
                        <div class="stars">★★★★★</div>
                        <p>“Loved the interior detailing. My Defender smells fresh and the leather feels brand new. Highly recommended.”</p>
                        <div class="who">Jasmeet Kaur<small>Verified Google review</small></div>
                    </div>
                    <div class="testi-card">
                        <div class="stars">★★★★★</div>
                        <p>“The best detailing studio in Punjab, hands down. Customer service is top-notch and the results speak for themselves.”</p>
                        <div class="who">Amit Sharma<small>Verified Google review</small></div>
                    </div>
                </div>
                <!-- Group 2 (Duplicate for seamless loop) -->
                <div class="testi-track-inner">
                    <div class="testi-card">
                        <div class="stars">★★★★★</div>
                        <p>“Picked up my car looking like it just left the showroom. The shine genuinely turned heads — worth every rupee.”</p>
                        <div class="who">Chirag Naini<small>Verified Google review</small></div>
                    </div>
                    <div class="testi-card">
                        <div class="stars">★★★★★</div>
                        <p>“Incredible attention to detail. My 5 series looks better than the day I bought it. The ceramic coating is flawless.”</p>
                        <div class="who">Gurpreet Singh<small>Verified Google review</small></div>
                    </div>
                    <div class="testi-card">
                        <div class="stars">★★★★★</div>
                        <p>“Professional team and premium setup. The paint correction removed all swirl marks completely.”</p>
                        <div class="who">Rohan Kapoor<small>Verified Google review</small></div>
                    </div>
                    <div class="testi-card">
                        <div class="stars">★★★★★</div>
                        <p>“Loved the interior detailing. My Defender smells fresh and the leather feels brand new. Highly recommended.”</p>
                        <div class="who">Jasmeet Kaur<small>Verified Google review</small></div>
                    </div>
                    <div class="testi-card">
                        <div class="stars">★★★★★</div>
                        <p>“The best detailing studio in Punjab, hands down. Customer service is top-notch and the results speak for themselves.”</p>
                        <div class="who">Amit Sharma<small>Verified Google review</small></div>
                    </div>
                </div>
            </div>
        </div>
    </section>
"""

# Replace the old testimonial block
# Finding the block from <!-- ============ TESTIMONIAL ============ --> to the end of its </section>
html = re.sub(
    r'<!-- ============ TESTIMONIAL ============ -->\s*<section class="sec-white testi">.*?</section>',
    marquee_html,
    html,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Now, add the CSS to css/style.css
css_addition = """
/* ---------- TESTIMONIAL MARQUEE ---------- */
.testi-marquee-sec {
    padding: clamp(60px, 10vh, 100px) 0;
    overflow: hidden;
}
.testi-header {
    text-align: center;
    margin-bottom: 48px;
}
.testi-header .gbadge {
    margin-top: 0;
}
.testi-marquee {
    overflow: hidden;
    width: 100%;
    position: relative;
}
/* Add fade effect on edges */
.testi-marquee::before, .testi-marquee::after {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    width: 100px;
    z-index: 2;
    pointer-events: none;
}
.testi-marquee::before {
    left: 0;
    background: linear-gradient(to right, var(--white), transparent);
}
.testi-marquee::after {
    right: 0;
    background: linear-gradient(to left, var(--white), transparent);
}

.testi-track {
    display: flex;
    width: fit-content;
    animation: scroll-reviews 35s linear infinite;
}
.testi-track:hover {
    animation-play-state: paused;
}
.testi-track-inner {
    display: flex;
    gap: 24px;
    padding-right: 24px;
}
.testi-card {
    background: var(--cream-2);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 34px 30px;
    width: 360px;
    flex-shrink: 0;
    box-shadow: 0 8px 26px rgba(80, 55, 30, .05);
    text-align: left;
    white-space: normal;
    transition: transform 0.3s, border-color 0.3s;
}
.testi-card:hover {
    transform: translateY(-4px);
    border-color: rgba(232, 70, 42, 0.4);
}
.testi-card .stars {
    color: var(--red);
    font-size: 1.2rem;
    letter-spacing: .1em;
    margin-bottom: 16px;
}
.testi-card p {
    font-family: var(--display);
    font-weight: 600;
    font-size: 1.05rem;
    line-height: 1.5;
    color: var(--ink);
    margin-bottom: 24px;
}
.testi-card .who {
    font-family: var(--display);
    font-weight: 800;
    font-size: 0.95rem;
    color: var(--ink);
}
.testi-card .who small {
    display: block;
    color: var(--muted);
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    font-size: 10px;
    margin-top: 6px;
}
"""

with open('css/style.css', 'a', encoding='utf-8') as f:
    f.write(css_addition)

anim_addition = """
@keyframes scroll-reviews {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
"""

with open('css/animations.css', 'a', encoding='utf-8') as f:
    f.write(anim_addition)
