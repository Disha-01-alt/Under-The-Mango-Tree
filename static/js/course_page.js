// static/js/course_page.js

document.addEventListener('DOMContentLoaded', function() {

    // --- Feature 1: Sidebar Toggle and Content Expansion ---
    const sidebar = document.getElementById('course-sidebar');
    const mainContent = document.getElementById('main-content');
    const toggleButton = document.getElementById('sidebar-toggle');
    const toggleIcon = document.getElementById('sidebar-toggle-icon');

    if (sidebar && mainContent && toggleButton && toggleIcon) {
        toggleButton.addEventListener('click', function() {
            sidebar.classList.toggle('hidden');
            const isSidebarHidden = sidebar.classList.contains('hidden');

            if (isSidebarHidden) {
                mainContent.classList.remove('lg:col-span-8', 'xl:col-span-9');
                mainContent.classList.add('lg:col-span-12');
                toggleIcon.classList.remove('fa-angles-left');
                toggleIcon.classList.add('fa-angles-right');
            } else {
                mainContent.classList.remove('lg:col-span-12');
                mainContent.classList.add('lg:col-span-8', 'xl:col-span-9');
                toggleIcon.classList.remove('fa-angles-right');
                toggleIcon.classList.add('fa-angles-left');
            }
        });
    }

    // --- Feature 2: Auto-scroll on Mobile after Page Load ---
    // Check if the URL contains a video_id (which happens on every video page except the first)
    // and if the screen is mobile-sized.
    const hasVideoId = window.location.pathname.split('/').pop() !== '' && !isNaN(window.location.pathname.split('/').pop());
    const isMobile = window.innerWidth < 1024; // lg breakpoint in Tailwind

    if (hasVideoId && isMobile) {
        const videoSection = document.getElementById('video-section');
        if (videoSection) {
            // This will now run only after the new page is fully loaded.
            videoSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
    
    // --- Feature 3: Auto-expand active topic in accordion ---
    const activeLink = document.querySelector('.sidebar-accordion .video-link.active');
    if (activeLink) {
        const accordionContent = activeLink.closest('.accordion-content');
        if (accordionContent && !accordionContent.classList.contains('show')) {
            accordionContent.classList.add('show');
            const button = accordionContent.previousElementSibling;
            if(button) {
                button.classList.remove('collapsed');
            }
        }
    }
});

// --- Accordion Toggle Function (remains global for onclick) ---
function toggleAccordion(button) {
    const content = button.nextElementSibling;
    if (content) {
        const isCurrentlyShown = content.classList.contains('show');
        // First, close all other accordions
        document.querySelectorAll('.sidebar-accordion .accordion-content.show').forEach(item => {
            item.classList.remove('show');
            item.previousElementSibling.classList.add('collapsed');
        });
        // Then, if the clicked one was closed, open it
        if (!isCurrentlyShown) {
            content.classList.add('show');
            button.classList.remove('collapsed');
        }
    }
}
