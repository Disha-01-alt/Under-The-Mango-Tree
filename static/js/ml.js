// Machine Learning video data structure
const mlVideos = [
    {
        id: "GwIo3gDZCVQ",
        title: "Machine Learning Tutorial 01 - What is ML?",
        description: "Introduction to Machine Learning concepts and applications."
    },
    {
        id: "6x0ME2b67n4",
        title: "Machine Learning Tutorial 02 - Types of ML",
        description: "Supervised, unsupervised, and reinforcement learning explained."
    },
    {
        id: "zM4VZR0px8E",
        title: "Machine Learning Tutorial 03 - Linear Regression",
        description: "Understanding linear regression and how it works."
    },
    {
        id: "suaA0nRM0PQ",
        title: "Machine Learning Tutorial 04 - Logistic Regression",
        description: "Learn logistic regression for classification problems."
    }
    // Add more ML videos as needed
];

document.addEventListener('DOMContentLoaded', function() {
    const videoTableBody = document.getElementById('video-table-body');
    
    if (videoTableBody) {
        mlVideos.forEach((video, index) => {
            const row = document.createElement('tr');
            
            const videoCell = document.createElement('td');
            videoCell.className = 'video-cell';
            videoCell.innerHTML = `
                <div class="video-container">
                    <iframe 
                        src="https://www.youtube.com/embed/${video.id}" 
                        title="${video.title}" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                </div>
            `;
            
            const titleCell = document.createElement('td');
            titleCell.className = 'title-cell';
            titleCell.innerHTML = `<h5>${index + 1}. ${video.title}</h5>`;
            
            const descCell = document.createElement('td');
            descCell.className = 'desc-cell';
            descCell.textContent = video.description;
            
            row.appendChild(videoCell);
            row.appendChild(titleCell);
            row.appendChild(descCell);
            
            videoTableBody.appendChild(row);
        });
        
        const tableContainer = document.querySelector('.table-responsive');
        if (tableContainer && !document.getElementById('ml-blog-link')) {
            const blogLink = document.createElement('div');
            blogLink.id = 'ml-blog-link';
            blogLink.className = 'text-center mt-4';
            blogLink.innerHTML = `
                <a href="https://machinelearningmastery.com/blog/" class="btn btn-primary" target="_blank">
                    <i class="fas fa-external-link-alt me-2"></i>Visit Machine Learning Mastery Blog
                </a>
            `;
            tableContainer.parentNode.appendChild(blogLink);
        }
    }
});
