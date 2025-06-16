document.addEventListener('DOMContentLoaded', function() {
    // --- Sidebar Toggle Logic ---
    const sidebar = document.getElementById('course-sidebar');
    const mainContent = document.getElementById('main-content');
    // In static/js/course_page.js

// Change this line
const toggleButton = document.getElementById('floating-sidebar-toggle'); 
// The rest of the script remains exactly the same.
    const toggleIcon = document.getElementById('sidebar-toggle-icon');

    if (sidebar && mainContent && toggleButton && toggleIcon) {
        toggleButton.addEventListener('click', function() {
            sidebar.classList.toggle('hidden');
            const isSidebarHidden = sidebar.classList.contains('hidden');

            if (isSidebarHidden) {
                // EXPAND MAIN CONTENT
                mainContent.classList.remove('lg:col-span-8', 'xl:col-span-9');
                mainContent.classList.add('lg:col-span-12', 'xl:col-span-12');
                toggleIcon.classList.remove('fa-angles-left');
                toggleIcon.classList.add('fa-angles-right');
            } else {
                // SHRINK MAIN CONTENT
                mainContent.classList.remove('lg:col-span-12', 'xl:col-span-12');
                mainContent.classList.add('lg:col-span-8', 'xl:col-span-9');
                toggleIcon.classList.remove('fa-angles-right');
                toggleIcon.classList.add('fa-angles-left');
            }
        });
    }
});
