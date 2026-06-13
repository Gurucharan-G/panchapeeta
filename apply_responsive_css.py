import io

css_path = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\static\css\styles.css"

responsive_css = """

/* =========================================
   RESPONSIVE DESIGN (MOBILE COMPATIBILITY)
   ========================================= */

/* Large Tablets / Laptops */
@media (max-width: 1200px) {
    .peethas-grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
    }
}

/* Tablets (Portrait) */
@media (max-width: 992px) {
    /* Header / Nav */
    .header-container {
        flex-direction: column;
        gap: 15px;
        padding: 10px 0;
    }
    
    .nav-links {
        width: 100%;
        overflow-x: auto;
        white-space: nowrap;
        padding-bottom: 5px;
        justify-content: flex-start;
        /* Scrollbar styling for nav */
        -webkit-overflow-scrolling: touch;
    }
    
    .nav-links::-webkit-scrollbar {
        height: 4px;
    }
    
    .language-selector {
        margin-left: 0;
        align-self: flex-start;
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
    }
    
    .hero-om {
        font-size: 2.2rem;
        margin-bottom: 10px;
    }
    
    .hero h2 {
        font-size: 1.8rem;
    }
    
    .hero-subtitle {
        font-size: 0.9rem;
        padding: 0 10px;
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
    
    .form-group label {
        font-size: 0.9rem;
    }
    
    /* Headers */
    .nav-links {
        gap: 15px;
    }
    
    .nav-link {
        font-size: 0.85rem;
        padding: 6px 12px;
    }
}
"""

with io.open(css_path, "a", encoding="utf-8") as f:
    f.write(responsive_css)

print("Responsive CSS appended successfully.")
