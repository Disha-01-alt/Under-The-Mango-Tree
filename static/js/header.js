// ====================================
// HEADER NAVIGATION JAVASCRIPT
// ====================================

// ====================================
// MOBILE MENU FUNCTIONALITY
// ====================================
function initializeMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const mobileSubmenuBtn = document.getElementById('mobile-submenu-btn');
    const mobileSubmenu = document.getElementById('mobile-submenu');
    const submenuIcon = document.getElementById('submenu-icon');

    if (!mobileMenuBtn || !mobileMenu) return; // Exit if mobile menu elements don't exist

    // Toggle main mobile menu
    mobileMenuBtn.addEventListener('click', function() {
        mobileMenu.classList.toggle('hidden');
        
        // Change hamburger to X icon
        if (mobileMenu.classList.contains('hidden')) {
            menuIcon.classList.remove('fa-times');
            menuIcon.classList.add('fa-bars');
        } else {
            menuIcon.classList.remove('fa-bars');
            menuIcon.classList.add('fa-times');
        }
    });

    // Toggle mobile submenu (Learning dropdown)
    if (mobileSubmenuBtn && mobileSubmenu) {
        mobileSubmenuBtn.addEventListener('click', function() {
            mobileSubmenu.classList.toggle('hidden');
            
            // Rotate arrow icon
            if (mobileSubmenu.classList.contains('hidden')) {
                submenuIcon.style.transform = 'rotate(0deg)';
            } else {
                submenuIcon.style.transform = 'rotate(180deg)';
            }
        });
    }

    // Close mobile menu when clicking on links
    const mobileMenuLinks = document.querySelectorAll('#mobile-menu a');
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', function() {
            mobileMenu.classList.add('hidden');
            menuIcon.classList.remove('fa-times');
            menuIcon.classList.add('fa-bars');
        });
    });
}

// ====================================
// DESKTOP DROPDOWN FUNCTIONALITY
// ====================================
function initializeDesktopDropdown() {
    const toggleBtn = document.getElementById('learningToggle');
    const menu = document.getElementById('learningMenu');

    if (!toggleBtn || !menu) return; // Exit if dropdown elements don't exist

    toggleBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        menu.classList.toggle('hidden');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
        if (!menu.contains(e.target) && !toggleBtn.contains(e.target)) {
            menu.classList.add('hidden');
        }
    });
}

// ====================================
// SMOOTH SCROLLING FOR NAVIGATION
// ====================================
function initializeNavigationScrolling() {
    // Smooth scrolling for anchor links in navigation
    document.querySelectorAll('nav a[href^="#"], .mobile-menu a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close mobile menu after clicking on anchor link
                const mobileMenu = document.getElementById('mobile-menu');
                const menuIcon = document.getElementById('menu-icon');
                if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                    if (menuIcon) {
                        menuIcon.classList.remove('fa-times');
                        menuIcon.classList.add('fa-bars');
                    }
                }
            }
        });
    });
}

// ====================================
// HEADER SCROLL EFFECTS (OPTIONAL)
// ====================================
function initializeHeaderScrollEffects() {
    const header = document.querySelector('header, .header, nav');
    if (!header) return;

    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add shadow when scrolling
        if (scrollTop > 10) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        // Optional: Hide header on scroll down, show on scroll up
        // Uncomment the following if you want this behavior
        /*
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            header.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            header.style.transform = 'translateY(0)';
        }
        */
        
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
}

// ====================================
// ACTIVE NAVIGATION HIGHLIGHTING
// ====================================
function initializeActiveNavigation() {
    const navLinks = document.querySelectorAll('nav a[href^="#"], .mobile-menu a[href^="#"]');
    const sections = document.querySelectorAll('section[id], div[id]');
    
    if (navLinks.length === 0 || sections.length === 0) return;

    const observerOptions = {
        threshold: 0.3,
        rootMargin: '-100px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const sectionId = entry.target.getAttribute('id');
                
                // Remove active class from all nav links
                navLinks.forEach(link => {
                    link.classList.remove('active', 'current');
                });
                
                // Add active class to current section's nav link
                const activeLink = document.querySelector(`nav a[href="#${sectionId}"], .mobile-menu a[href="#${sectionId}"]`);
                if (activeLink) {
                    activeLink.classList.add('active');
                }
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        observer.observe(section);
    });
}

// ====================================
// HEADER NAVIGATION INITIALIZATION
// ====================================
function initializeHeaderNavigation() {
    initializeMobileMenu();
    initializeDesktopDropdown();
    initializeNavigationScrolling();
    initializeHeaderScrollEffects();
    initializeActiveNavigation();
}

// ====================================
// AUTO-INITIALIZE ON DOM READY
// ====================================
document.addEventListener('DOMContentLoaded', function() {
    initializeHeaderNavigation();
});

// ====================================
// UTILITY FUNCTIONS FOR EXTERNAL USE
// ====================================

// Function to manually close mobile menu (can be called from other scripts)
function closeMobileMenu() {
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    
    if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
        mobileMenu.classList.add('hidden');
        if (menuIcon) {
            menuIcon.classList.remove('fa-times');
            menuIcon.classList.add('fa-bars');
        }
    }
}

// Function to manually close desktop dropdown (can be called from other scripts)
function closeDesktopDropdown() {
    const menu = document.getElementById('learningMenu');
    if (menu) {
        menu.classList.add('hidden');
    }
}

// Function to highlight specific navigation item
function setActiveNavItem(sectionId) {
    const navLinks = document.querySelectorAll('nav a, .mobile-menu a');
    
    navLinks.forEach(link => {
        link.classList.remove('active', 'current');
        if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
        }
    });
}

