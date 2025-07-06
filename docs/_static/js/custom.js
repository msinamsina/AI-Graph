// AI-Graph Custom Documentation JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy button to code blocks
    const codeBlocks = document.querySelectorAll('pre');
    codeBlocks.forEach(block => {
        // Create copy button
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = '📋 Copy';
        copyButton.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: var(--gradient-bg);
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 10;
        `;

        // Make parent relative for absolute positioning
        block.style.position = 'relative';
        block.appendChild(copyButton);

        // Show/hide copy button on hover
        block.addEventListener('mouseenter', () => {
            copyButton.style.opacity = '1';
        });

        block.addEventListener('mouseleave', () => {
            copyButton.style.opacity = '0';
        });

        // Copy functionality
        copyButton.addEventListener('click', async () => {
            const code = block.querySelector('code');
            const text = code ? code.innerText : block.innerText;

            try {
                await navigator.clipboard.writeText(text);
                copyButton.innerHTML = '✅ Copied!';
                setTimeout(() => {
                    copyButton.innerHTML = '📋 Copy';
                }, 2000);
            } catch (err) {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);

                copyButton.innerHTML = '✅ Copied!';
                setTimeout(() => {
                    copyButton.innerHTML = '📋 Copy';
                }, 2000);
            }
        });
    });

    // Add "Back to Top" button
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '⬆️';
    backToTopButton.className = 'back-to-top';
    backToTopButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: var(--gradient-bg);
        color: white;
        border: none;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        font-size: 20px;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: var(--shadow);
    `;

    document.body.appendChild(backToTopButton);

    // Show/hide back to top button
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.style.opacity = '1';
            backToTopButton.style.visibility = 'visible';
        } else {
            backToTopButton.style.opacity = '0';
            backToTopButton.style.visibility = 'hidden';
        }
    });

    // Back to top functionality
    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Add reading progress indicator
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 4px;
        background: var(--gradient-bg);
        z-index: 1000;
        transition: width 0.3s ease;
    `;

    document.body.appendChild(progressBar);

    // Update reading progress
    window.addEventListener('scroll', () => {
        const scrolled = (window.pageYOffset / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        progressBar.style.width = scrolled + '%';
    });

    // Enhanced search functionality
    const searchInput = document.querySelector('input[type="text"]');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            if (query.length > 2) {
                highlightSearchTerms(query);
            } else {
                removeHighlights();
            }
        });
    }

    function highlightSearchTerms(query) {
        const walker = document.createTreeWalker(
            document.querySelector('.document'),
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const textNodes = [];
        let node;
        while (node = walker.nextNode()) {
            textNodes.push(node);
        }

        textNodes.forEach(textNode => {
            const text = textNode.textContent;
            const regex = new RegExp(`(${query})`, 'gi');
            if (regex.test(text)) {
                const highlightedText = text.replace(regex, '<mark class="search-highlight">$1</mark>');
                const span = document.createElement('span');
                span.innerHTML = highlightedText;
                textNode.parentNode.replaceChild(span, textNode);
            }
        });
    }

    function removeHighlights() {
        const highlights = document.querySelectorAll('.search-highlight');
        highlights.forEach(highlight => {
            const parent = highlight.parentNode;
            parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
            parent.normalize();
        });
    }

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="text"]');
            if (searchInput) {
                searchInput.focus();
            }
        }

        // Escape to close search
        if (e.key === 'Escape') {
            const searchInput = document.querySelector('input[type="text"]');
            if (searchInput && document.activeElement === searchInput) {
                searchInput.blur();
                removeHighlights();
            }
        }
    });

    // Add tooltips to navigation items
    const navItems = document.querySelectorAll('.wy-menu-vertical a');
    navItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'nav-tooltip';
            tooltip.textContent = this.textContent;
            tooltip.style.cssText = `
                position: absolute;
                background: var(--dark-color);
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 1000;
                pointer-events: none;
                white-space: nowrap;
                left: 100%;
                top: 50%;
                transform: translateY(-50%);
                margin-left: 10px;
                opacity: 0;
                transition: opacity 0.3s ease;
            `;

            this.style.position = 'relative';
            this.appendChild(tooltip);

            setTimeout(() => {
                tooltip.style.opacity = '1';
            }, 100);
        });

        item.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.nav-tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });

    // Add dark mode toggle (optional)
    const darkModeToggle = document.createElement('button');
    darkModeToggle.innerHTML = '🌙';
    darkModeToggle.className = 'dark-mode-toggle';
    darkModeToggle.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--gradient-bg);
        color: white;
        border: none;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        font-size: 16px;
        cursor: pointer;
        z-index: 1000;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    `;

    document.body.appendChild(darkModeToggle);

    // Dark mode functionality
    darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        this.innerHTML = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';

        // Save preference
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
    });

    // Load dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
        darkModeToggle.innerHTML = '☀️';
    }

    // Add CSS for dark mode
    const darkModeStyles = document.createElement('style');
    darkModeStyles.textContent = `
        .dark-mode {
            --light-color: #1a1a1a;
            --dark-color: #e0e0e0;
            --code-bg: #2d2d2d;
            --code-border: #404040;
            background-color: var(--light-color) !important;
            color: var(--dark-color) !important;
        }

        .dark-mode .wy-nav-content {
            background-color: #2d2d2d !important;
            color: var(--dark-color) !important;
        }

        .dark-mode .wy-nav-side {
            background-color: #1a1a1a !important;
        }

        .dark-mode .wy-menu-vertical a {
            color: var(--dark-color) !important;
        }
    `;
    document.head.appendChild(darkModeStyles);

    // Add animation to elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out';
            }
        });
    }, observerOptions);

    // Observe all sections
    document.querySelectorAll('section, .section').forEach(section => {
        observer.observe(section);
    });

    console.log('AI-Graph Documentation Enhanced! 🚀');
});
