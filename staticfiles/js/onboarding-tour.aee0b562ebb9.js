(function() {
    // Dynamic CSS Injection
    const css = `
        .tour-overlay {
            position: fixed;
            background-color: rgba(15, 23, 42, 0.75);
            z-index: 100000;
            pointer-events: auto;
            transition: all 0.3s ease;
            backdrop-filter: blur(1px);
        }
        .tour-popover {
            position: absolute;
            width: 350px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(15, 23, 42, 0.3);
            z-index: 100001;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            border: 2px solid #ea580c;
            font-family: 'Inter', sans-serif;
            opacity: 0;
            transform: scale(0.95);
            transition: opacity 0.25s ease, transform 0.25s ease;
            pointer-events: auto;
        }
        .tour-popover.visible {
            opacity: 1;
            transform: scale(1);
        }
        .tour-popover-header {
            font-family: 'Outfit', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: #ea580c;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1.5px solid #ffedd5;
            padding-bottom: 8px;
        }
        .tour-popover-body {
            font-size: 0.92rem;
            color: #334155;
            line-height: 1.6;
        }
        .tour-popover-body p {
            margin-bottom: 6px;
        }
        .tour-popover-body .lang-section {
            padding: 4px 0;
        }
        .tour-popover-body .kn-text {
            font-weight: 500;
            color: #475569;
            border-top: 1px dashed #e2e8f0;
            margin-top: 8px;
            padding-top: 8px;
        }
        .tour-popover-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 4px;
        }
        .tour-progress {
            font-size: 0.78rem;
            font-weight: 600;
            color: #64748b;
        }
        .tour-btn-group {
            display: flex;
            gap: 8px;
            align-items: center;
        }
        .tour-btn {
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 700;
            cursor: pointer;
            border: none;
            transition: all 0.2s ease;
        }
        .tour-btn-primary {
            background: linear-gradient(135deg, #ea580c, #f97316);
            color: white;
            box-shadow: 0 4px 10px rgba(234, 88, 12, 0.2);
        }
        .tour-btn-primary:hover {
            box-shadow: 0 6px 15px rgba(234, 88, 12, 0.3);
            transform: translateY(-1px);
        }
        .tour-btn-secondary {
            background-color: #cbd5e1;
            color: #334155;
        }
        .tour-btn-secondary:hover {
            background-color: #94a3b8;
        }
        .tour-btn-skip {
            background: transparent;
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 500;
            text-decoration: underline;
        }
        .tour-btn-skip:hover {
            color: #ea580c;
        }
        .tour-highlight {
            position: relative;
            z-index: 100002 !important;
            box-shadow: 0 0 0 16px rgba(234, 88, 12, 0.3) !important;
            pointer-events: none !important;
            transition: box-shadow 0.25s ease;
        }
    `;

    // Inject CSS styles into head
    const styleElement = document.createElement('style');
    styleElement.innerHTML = css;
    document.head.appendChild(styleElement);

    // Overlay Elements
    let overlayTop, overlayBottom, overlayLeft, overlayRight;
    let popover;
    let currentStep = 0;

    // Onboarding Steps Definition
    const steps = [
        {
            target: null, // Center screen
            title: {
                en: "Welcome to Panchapeetas! 🧭",
                kn: "ಪಂಚಪೀಠಗಳ ಜಾಲತಾಣಕ್ಕೆ ಸುಸ್ವಾಗತ! 🧭"
            },
            body: {
                en: "Let's take a quick 1-minute guided tour of the main actions, devotional features, and bookings on our platform.",
                kn: "ವೆಬ್‌ಸೈಟ್‌ನಲ್ಲಿ ಪೂಜೆ ಸೇವೆಗಳು, ವಸತಿ ಕೋಣೆಗಳು ಹಾಗೂ ಧಾರ್ಮಿಕ ವೈಶಿಷ್ಟ್ಯಗಳನ್ನು ಬಳಸುವ ವಿಧಾನದ ಬಗ್ಗೆ ಒಂದು ಸಣ್ಣ ಪ್ರವಾಸ ಆರಂಭಿಸೋಣ."
            }
        },
        {
            target: ".lang-selector-container",
            title: {
                en: "Language Selector / ಭಾಷೆ ಆಯ್ಕೆ",
                kn: "ಪ್ರಾದೇಶಿಕ ಭಾಷೆಗಳ ಬದಲಾವಣೆ"
            },
            body: {
                en: "You can instantly switch the entire platform into 7 different languages, including English, Kannada, Hindi, and others here.",
                kn: "ನಿಮ್ಮ ಆಯ್ಕೆಯ ಭಾಷೆಯಲ್ಲಿ ವೆಬ್‌ಸೈಟ್ ಓದಲು ಇಲ್ಲಿ ಕ್ಲಿಕ್ ಮಾಡಿ ಕನ್ನಡ ಸೇರಿದಂತೆ 7 ಪ್ರಾದೇಶಿಕ ಭಾಷೆಗಳನ್ನು ಆರಿಸಿಕೊಳ್ಳಬಹುದು."
            }
        },
        {
            target: ".nav-links",
            title: {
                en: "Platform Navigation",
                kn: "ಪುಟಗಳ ತ್ವರಿತ ಸಂಚಾರ"
            },
            body: {
                en: "Use these navigation links to quickly jump to the Divine Heritage info, Veerashaivism scriptures, and other about sections.",
                kn: "ಮಠಗಳ ಇತಿಹಾಸ, ವೀರಶೈವ ಸಿದ್ಧಾಂತ ಹಾಗೂ ಸಂಸ್ಕೃತಿ ವಿವರಗಳ ಪುಟಕ್ಕೆ ತಕ್ಷಣ ಹೋಗಲು ಇಲ್ಲಿ ಕ್ಲಿಕ್ ಮಾಡಿ."
            }
        },
        {
            target: ".nav-btn-dashboard, .nav-profile-dropdown",
            title: {
                en: "Devotee Login & Portal",
                kn: "ಭಕ್ತರ ಪ್ರೊಫೈಲ್ ಮತ್ತು ಲಾಗಿನ್"
            },
            body: {
                en: "Sign in using your Google account or email to configure your Nakshatra/Gotra profile, track bookings, and download PDF receipts.",
                kn: "ಗೂಗಲ್ ಅಥವಾ ಇಮೇಲ್ ಬಳಸಿ ಲಾಗಿನ್ ಆಗಿ ನಿಮ್ಮ ನಕ್ಷತ್ರ-ಗೋತ್ರದ ವಿವರ ಉಳಿಸಿಕೊಳ್ಳಬಹುದು, ಮತ್ತು ಬುಕ್ ಮಾಡಿದ ರಶೀದಿಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಬಹುದು."
            }
        },
        {
            target: ".peethas-grid",
            title: {
                en: "Monastery Profiles (Peethas)",
                kn: "ಧರ್ಮ ಪೀಠಗಳ ವಿವರಗಳು"
            },
            body: {
                en: "Click on any Peetha card to view its biography, details of the Current Swamiji, and watch live darshan YouTube streams.",
                kn: "ಯಾವುದೇ ಪೀಠದ ಚಿತ್ರದ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಿದರೆ ಆ ಮಠದ ಇತಿಹಾಸ, ಪೂಜ್ಯ ಶ್ರೀಗಳ ಪರಿಚಯ ಮತ್ತು ಲೈವ್ ದರ್ಶನ ವೀಕ್ಷಿಸುವ ಪುಟ ತೆರೆದುಕೊಳ್ಳುತ್ತದೆ."
            }
        },
        {
            target: "#devotional-player",
            title: {
                en: "Devotional stotra Player",
                kn: "ಆಧ್ಯಾತ್ಮಿಕ ಸಂಗೀತ ವಾಹಕ"
            },
            body: {
                en: "Control stotras and mantra chantings. It continues playing in the background even if you refresh or switch pages!",
                kn: "ಮಧುರ ಜಪ ಹಾಗೂ ಶ್ಲೋಕಗಳನ್ನು ಕೇಳಲು ಈ ಪ್ಲೇಯರ್ ಬಳಸಿ. ವೆಬ್ ಪುಟ ಬದಲಾಯಿಸಿದರೂ ಇದು ಹಿನ್ನೆಲೆಯಲ್ಲಿ ಪ್ಲೇ ಆಗುತ್ತಿರುತ್ತದೆ."
            }
        },
        {
            target: null, // Center screen
            title: {
                en: "Onboarding Complete! 🎉",
                kn: "ಪ್ರವಾಸ ಮುಕ್ತಾಯಗೊಂಡಿದೆ! 🎉"
            },
            body: {
                en: "You are all set to explore the Panchapeetas platform. Enjoy your experience!",
                kn: "ಪಂಚಪೀಠ ಜಾಲತಾಣದ ಸಂಪೂರ್ಣ ಪರಿಚಯ ಮುಗಿದಿದೆ. ಪುಟಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಪ್ರಾರಂಭಿಸಿ!"
            }
        }
    ];

    // Create Overlay backdrops
    function createOverlay() {
        if (overlayTop) return; // Already exists
        
        overlayTop = document.createElement('div');
        overlayBottom = document.createElement('div');
        overlayLeft = document.createElement('div');
        overlayRight = document.createElement('div');

        overlayTop.className = 'tour-overlay';
        overlayBottom.className = 'tour-overlay';
        overlayLeft.className = 'tour-overlay';
        overlayRight.className = 'tour-overlay';

        document.body.appendChild(overlayTop);
        document.body.appendChild(overlayBottom);
        document.body.appendChild(overlayLeft);
        document.body.appendChild(overlayRight);

        // Create Popover
        popover = document.createElement('div');
        popover.className = 'tour-popover';
        document.body.appendChild(popover);
        
        // Listen to resize and scroll
        window.addEventListener('resize', repositionCurrentStep);
        window.addEventListener('scroll', repositionCurrentStep);
    }

    // Destroy Overlay backdrops
    function destroyOverlay() {
        if (overlayTop) overlayTop.remove();
        if (overlayBottom) overlayBottom.remove();
        if (overlayLeft) overlayLeft.remove();
        if (overlayRight) overlayRight.remove();
        if (popover) popover.remove();

        overlayTop = overlayBottom = overlayLeft = overlayRight = popover = null;
        
        // Remove highlighters
        document.querySelectorAll('.tour-highlight').forEach(el => {
            el.classList.remove('tour-highlight');
        });
        
        window.removeEventListener('resize', repositionCurrentStep);
        window.removeEventListener('scroll', repositionCurrentStep);
    }

    // Spotlight layout calculation
    function updateSpotlight(element) {
        if (!overlayTop) return;
        
        if (!element) {
            // Full Screen Cover
            overlayTop.style.top = '0px';
            overlayTop.style.left = '0px';
            overlayTop.style.width = '100%';
            overlayTop.style.height = '100%';
            
            overlayBottom.style.height = '0px';
            overlayLeft.style.width = '0px';
            overlayRight.style.width = '0px';
            return;
        }

        const rect = element.getBoundingClientRect();
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        const offset = 8; // Margin around spotlight element

        // Top band
        overlayTop.style.top = '0px';
        overlayTop.style.left = '0px';
        overlayTop.style.width = '100%';
        overlayTop.style.height = Math.max(0, rect.top - offset) + 'px';

        // Bottom band
        overlayBottom.style.top = Math.min(viewportHeight, rect.bottom + offset) + 'px';
        overlayBottom.style.left = '0px';
        overlayBottom.style.width = '100%';
        overlayBottom.style.height = Math.max(0, viewportHeight - (rect.bottom + offset)) + 'px';

        // Left band (flanking element)
        overlayLeft.style.top = Math.max(0, rect.top - offset) + 'px';
        overlayLeft.style.left = '0px';
        overlayLeft.style.width = Math.max(0, rect.left - offset) + 'px';
        overlayLeft.style.height = (rect.height + offset * 2) + 'px';

        // Right band (flanking element)
        overlayRight.style.top = Math.max(0, rect.top - offset) + 'px';
        overlayRight.style.left = Math.min(viewportWidth, rect.right + offset) + 'px';
        overlayRight.style.width = Math.max(0, viewportWidth - (rect.right + offset)) + 'px';
        overlayRight.style.height = (rect.height + offset * 2) + 'px';
    }

    // Position popover relative to spotlight
    function updatePopoverPosition(element) {
        if (!popover) return;

        if (!element) {
            // Center in screen
            popover.style.position = 'fixed';
            popover.style.top = '50%';
            popover.style.left = '50%';
            popover.style.transform = 'translate(-50%, -50%)';
            return;
        }

        popover.style.position = 'absolute';
        popover.style.transform = 'none';

        const rect = element.getBoundingClientRect();
        const popoverWidth = 350;
        const offset = 16;
        
        let top = rect.bottom + window.scrollY + offset;
        let left = rect.left + window.scrollX + (rect.width - popoverWidth) / 2;

        // Boundary safety checks
        if (left < 10) left = 10;
        if (left + popoverWidth > window.innerWidth - 10) {
            left = window.innerWidth - popoverWidth - 10;
        }

        // If it overlaps screen bottom, show above instead
        if (rect.bottom + popover.offsetHeight + offset > window.innerHeight) {
            top = rect.top + window.scrollY - popover.offsetHeight - offset;
        }

        popover.style.top = top + 'px';
        popover.style.left = left + 'px';
    }

    // Reposition loop for window changes
    function repositionCurrentStep() {
        const step = steps[currentStep];
        let targetEl = null;
        if (step.target) {
            targetEl = document.querySelector(step.target);
        }
        updateSpotlight(targetEl);
        updatePopoverPosition(targetEl);
    }

    // Main Tour Runner logic
    function showStep(index) {
        currentStep = index;
        const step = steps[index];
        
        // Remove highlighters on all previous items
        document.querySelectorAll('.tour-highlight').forEach(el => {
            el.classList.remove('tour-highlight');
        });

        // Hide popover temporarily for clean transition
        popover.classList.remove('visible');

        let targetEl = null;
        if (step.target) {
            targetEl = document.querySelector(step.target);
        }

        if (targetEl) {
            targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Wait brief moment for smooth scrolling
            setTimeout(() => {
                targetEl.classList.add('tour-highlight');
                updateSpotlight(targetEl);
                renderPopoverContent(step);
                updatePopoverPosition(targetEl);
                popover.classList.add('visible');
            }, 300);
        } else {
            // Screen centered welcome/done step
            updateSpotlight(null);
            renderPopoverContent(step);
            updatePopoverPosition(null);
            popover.classList.add('visible');
        }
    }

    // Render HTML content of popover card
    function renderPopoverContent(step) {
        if (!popover) return;

        const isFirst = currentStep === 0;
        const isLast = currentStep === steps.length - 1;

        popover.innerHTML = `
            <div class="tour-popover-header">
                <span class="tour-icon">ॐ</span>
                <div>${step.title.en}</div>
            </div>
            <div class="tour-popover-body">
                <div class="lang-section en-text">
                    ${step.body.en}
                </div>
                <div class="lang-section kn-text">
                    ${step.body.kn}
                </div>
            </div>
            <div class="tour-popover-footer">
                <div class="tour-progress">
                    ${isFirst || isLast ? '' : `Step ${currentStep} of ${steps.length - 2} / ಹಂತ ${currentStep}`}
                </div>
                <div class="tour-btn-group">
                    ${isFirst ? '' : `<button class="tour-btn tour-btn-secondary" onclick="window.onboardingTour.prevStep()">Back</button>`}
                    
                    <button class="tour-btn tour-btn-primary" onclick="window.onboardingTour.nextStep()">
                        ${isFirst ? 'Start / ಪ್ರಾರಂಭಿಸಿ' : (isLast ? 'Finish / ಮುಕ್ತಾಯ' : 'Next / ಮುಂದೆ')}
                    </button>
                </div>
            </div>
            <div style="text-align: right; margin-top: 4px;">
                ${isLast ? '' : `<button class="tour-btn-skip" onclick="window.onboardingTour.endTour()">Skip Tour / ಪ್ರವಾಸ ಬೇಡ</button>`}
            </div>
        `;
    }

    // API triggers
    function startTour() {
        if (window.location.pathname !== '/' && window.location.pathname !== '') {
            const langParam = new URLSearchParams(window.location.search).get('lang');
            let redirectUrl = '/?start_tour=true';
            if (langParam) redirectUrl += '&lang=' + langParam;
            window.location.href = redirectUrl;
            return;
        }
        createOverlay();
        showStep(0);
    }

    function nextStep() {
        if (currentStep < steps.length - 1) {
            showStep(currentStep + 1);
        } else {
            endTour();
        }
    }

    function prevStep() {
        if (currentStep > 0) {
            showStep(currentStep - 1);
        }
    }

    function endTour() {
        destroyOverlay();
        localStorage.setItem('panchapeethas_tour_completed', 'true');
    }

    // Expose APIs globally
    window.onboardingTour = {
        startTour: startTour,
        nextStep: nextStep,
        prevStep: prevStep,
        endTour: endTour
    };

    // Auto-start for first-time visitors
    document.addEventListener('DOMContentLoaded', () => {
        // Trigger if URL parameter ?start_tour=true is present
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('start_tour') === 'true') {
            // Clean URL parameter for clean aesthetic
            const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
            window.history.replaceState({path: newUrl}, '', newUrl);
            setTimeout(startTour, 1000);
            return;
        }

        // Auto-run if tour not completed yet
        const tourCompleted = localStorage.getItem('panchapeethas_tour_completed');
        if (!tourCompleted) {
            // Give layout 2 seconds to render, image loadings, stotra autoplay configs etc
            setTimeout(startTour, 2000);
        }

        // Bind clicks to startTourBtn
        const tourBtn = document.getElementById('startTourBtn');
        if (tourBtn) {
            tourBtn.addEventListener('click', (e) => {
                e.preventDefault();
                startTour();
            });
        }
    });

})();
