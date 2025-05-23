// Deep Learning video data structure
const dlVideos = [
    {
        id: "O5xeyoRL95U",
        title: "Deep Learning Introduction",
        description: "Overview of deep learning concepts and applications."
    },
    {
        id: "aircAruvnKk",
        title: "Neural Networks Basics",
        description: "Understanding the fundamentals of neural networks."
    },
    {
        id: "CS4cs9xVecg",
        title: "Activation Functions",
        description: "Learn about different activation functions used in deep learning."
    },
    {
        id: "V3d2FzH1GGc",
        title: "Backpropagation Explained",
        description: "How backpropagation works in training neural networks."
    },
    {
        id: "tPYj3fFJGjk",
        title: "Convolutional Neural Networks",
        description: "Introduction to CNNs and their applications in image processing."
    },
    {
        id: "y3f8GOTjXz0",
        title: "Recurrent Neural Networks",
        description: "Explore RNNs for sequential data and time series."
    },
    {
        id: "iX5V1K46FTM",
        title: "Autoencoders",
        description: "Understanding autoencoders and their uses in unsupervised learning."
    },
    {
        id: "Zjvu64T7FuA",
        title: "Generative Adversarial Networks (GANs)",
        description: "Learn the basics of GANs and how they generate data."
    },
    {
        id: "u1lo2CO2OM4",
        title: "Transfer Learning",
        description: "Using pre-trained models to improve training efficiency."
    },
    {
        id: "sCgtH1hl2pQ",
        title: "Deep Learning Frameworks",
        description: "Overview of popular frameworks like TensorFlow and PyTorch."
    }
];

document.addEventListener('DOMContentLoaded', function() {
    const videoTableBody = document.getElementById('video-table-body');
    
    if (videoTableBody) {
        dlVideos.forEach((video, index) => {
            const row = document.createElement('tr');
            
            // Video iframe cell
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
            
            // Title cell
            const titleCell = document.createElement('td');
            titleCell.className = 'title-cell';
            titleCell.innerHTML = `<h5>${index + 1}. ${video.title}</h5>`;
            
            // Description cell
            const descCell = document.createElement('td');
            descCell.className = 'desc-cell';
            descCell.textContent = video.description;
            
            row.appendChild(videoCell);
            row.appendChild(titleCell);
            row.appendChild(descCell);
            videoTableBody.appendChild(row);
        });

        // Add a link below the table for more DL resources
        const tableContainer = document.querySelector('.table-responsive');
        const blogLink = document.createElement('div');
        blogLink.className = 'text-center mt-4';
        blogLink.innerHTML = `
            <a href="https://deeplearning.ai/blog" class="btn btn-primary" target="_blank">
                <i class="fas fa-external-link-alt me-2"></i>Visit DeepLearning.AI Blog
            </a>
        `;

        if (tableContainer) {
            tableContainer.parentNode.appendChild(blogLink);
        }
    }
});
