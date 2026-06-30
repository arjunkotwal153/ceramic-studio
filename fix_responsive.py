import os

resp_file = r'c:\Users\PC\Downloads\ceramic studio\css\responsive.css'

with open(resp_file, 'a', encoding='utf-8') as f:
    f.write("""
@media(max-width: 414px) {
    .eyebrow {
        font-size: 8.5px;
        letter-spacing: 0.15em;
        gap: 8px;
    }
    .eyebrow::before, .eyebrow::after {
        width: 15px;
    }
    nav {
        padding: 12px 10px;
    }
    .brand {
        font-size: 11px;
        letter-spacing: 0.1em;
        gap: 6px;
    }
    .brand .mk {
        width: 24px;
        height: 24px;
        font-size: 12px;
    }
    .nav-cta {
        padding: 8px 12px;
        font-size: 10px;
    }
    .hero-stats {
        gap: 10px;
    }
    .hs {
        font-size: 10px;
    }
}
""")
print("Updated responsive.css")
