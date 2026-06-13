import io
import re

html_path = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\templates\peethas\index.html"
css_path = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\static\css\styles.css"

# 1. Update index.html
with io.open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Insert the hamburger button before <nav class="nav-links">
# Also wrap the top row for mobile
hamburger_html = """
            <div class="mobile-top-bar">
                <button class="hamburger-btn" onclick="document.querySelector('.nav-links').classList.toggle('open')">☰ Menu</button>
            </div>
            <nav class="nav-links">"""

if '<button class="hamburger-btn"' not in html_content:
    html_content = html_content.replace('            <nav class="nav-links">', hamburger_html)
    with io.open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("index.html updated with hamburger button.")


# 2. Update styles.css responsive block
with io.open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

marker = "/* =========================================\n   RESPONSIVE DESIGN (MOBILE COMPATIBILITY)\n   ========================================= */"

if marker in css_content:
    base_css = css_content.split(marker)[0]
else:
    base_css = css_content

new_responsive_css = """
/* =========================================
   RESPONSIVE DESIGN (MOBILE COMPATIBILITY)
   ========================================= */

.mobile-top-bar {
    display: none;
    width: 100%;
    justify-content: space-between;
    align-items: center;
}

.hamburger-btn {
    background: var(--gold);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: var(--radius);
    font-weight: 600;
    cursor: pointer;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Large Tablets / Laptops */
@media (max-width: 1200px) {
    .peethas-grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
    }
}

/* Tablets & Mobile */
@media (max-width: 992px) {
    /* Header / Nav */
    .site-header {
        border-radius: 20px;
        padding-bottom: 5px;
    }
    
    .header-container {
        flex-direction: column;
        gap: 15px;
        padding: 15px 10px;
        height: auto;
    }
    
    .mobile-top-bar {
        display: flex;
    }

    .lang-selector-container {
        align-self: center;
        margin-bottom: 5px;
    }
    
    .nav-links {
        display: none; /* Hide by default */
        flex-direction: column;
        width: 100%;
        gap: 10px;
        padding: 10px 0;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
    }

    .nav-links.open {
        display: flex;
    }
    
    .nav-link {
        text-align: center;
        width: 100%;
    }

    /* Detail Page */
    .detail-grid {
        grid-template-columns: 1fr;
        gap: 30px;
    }
    
    .sidebar-sticky {
        position: static;
        top: auto;
    }
}

/* Mobile Devices */
@media (max-width: 768px) {
    /* Hero Section */
    .hero {
        padding: 60px 0 80px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .hero-om {
        font-size: 2.2rem;
        margin-bottom: 10px;
        order: 2; /* Put below murals */
    }
    
    .hero h2 {
        font-size: 1.8rem;
        order: 3;
    }
    
    .hero-subtitle {
        font-size: 0.9rem;
        padding: 0 10px;
        order: 4;
    }

    /* Murals side by side */
    .hero-mural {
        position: static; /* Remove absolute positioning */
        width: 130px;
        height: 85px;
        transform: none !important;
        opacity: 0.95 !important;
        pointer-events: none;
        display: inline-block !important;
        margin: 0 10px 20px 10px;
    }

    .murals-mobile-container {
        display: flex;
        justify-content: center;
        width: 100%;
        order: 1; /* Put at the very top */
    }

    /* Peethas Grid */
    .peethas-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
    }
    
    .peetha-card {
        padding-top: 70px;
        margin-top: 60px;
    }
    
    .card-portrait-wrapper {
        top: -60px;
    }
    
    .card-portrait {
        width: 120px;
        height: 120px;
    }
    
    /* About Section */
    .about-section {
        padding: 50px 0;
    }
    
    .about-section h2 {
        font-size: 1.5rem;
    }
    
    /* Auth Containers */
    .auth-section {
        padding-top: 80px;
        padding-bottom: 40px;
    }
    
    .auth-container {
        padding: 25px;
        margin: 0 15px;
        width: calc(100% - 30px);
    }
    
    .auth-header h2 {
        font-size: 1.5rem;
    }
    
    /* Detail Page */
    .detail-hero {
        padding: 60px 0 30px;
    }
    
    .detail-hero h2 {
        font-size: 1.6rem;
    }
    
    .content-card {
        padding: 25px;
    }
    
    .section-title {
        font-size: 1.4rem;
    }

    /* Footer */
    .footer-content {
        flex-direction: column;
        text-align: center;
        gap: 10px;
    }
    
    .footer-links {
        justify-content: center;
        flex-wrap: wrap;
    }
}

/* Small Mobile Devices */
@media (max-width: 480px) {
    /* Peethas Grid - 1 Column */
    .peethas-grid {
        grid-template-columns: 1fr;
    }
    
    .card-mutt-photo {
        height: 180px;
    }
    
    .peetha-card {
        margin-left: 20px;
        margin-right: 20px;
    }

    /* Auth Forms */
    .auth-container {
        padding: 20px;
    }
}
"""

with io.open(css_path, "w", encoding="utf-8") as f:
    f.write(base_css + new_responsive_css)
    
print("styles.css updated with hamburger menu logic and side-by-side murals.")
