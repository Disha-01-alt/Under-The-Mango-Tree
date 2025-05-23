// Python video data structure
const pythonVideos = [
    {
        id: "ruGpu6BilYs",
        title: "Python Tutorial 01 - Basic Introduction",
        description: "Introduction to Python programming and its basic structure."
    },
    {
        id: "_YkSrGKNgFI",
        title: "Python Tutorial 02 - Basic Operators",
        description: "Learn arithmetic and comparison operators in Python."
    },
    {
        id: "pS7uCnnFKYs",
        title: "Python Tutorial 03 - Indentation",
        description: "Understand Python's indentation rules and block structures."
    },
    {
        id: "PRz0RmvYsE4",
        title: "Python Tutorial 04 - Decision Making using If Else",
        description: "Learn how to use if, else, and elif for decision-making."
    },
    {
        id: "wURLEjcMwmE",
        title: "Python Tutorial 05 - Function with One Input Variable",
        description: "Define and use a function with one input parameter."
    },
    {
        id: "K4Zsfgkb-nE",
        title: "Python Tutorial 06 - Function Output",
        description: "How to return results from Python functions."
    },
    {
        id: "AtnC-eHPjUE",
        title: "Python Tutorial 07 - Function with Two Input Variables",
        description: "Functions that accept and operate on two inputs."
    },
    {
        id: "jdPwiner0aI",
        title: "Python Tutorial 08 - Break, Continue and Pass",
        description: "Use break, continue, and pass in loops for control flow."
    },
    {
        id: "OoGezi_REq4",
        title: "Python Tutorial 09 - Lists",
        description: "Introduction to Python lists and how to create them."
    },
    {
        id: "NoH-MfljqH8",
        title: "Python Tutorial 10 - List Operations",
        description: "Perform common operations on Python lists like append, pop, and slicing."
    },
    {
        id: "rZBihU7Vybk",
        title: "Python Tutorial 11 - For Loops",
        description: "Iterate over data using for loops."
    },
    {
        id: "9mKG_gB9u28",
        title: "Python Tutorial 12 - Loops with Lists",
        description: "Loop through list elements and perform operations."
    },
    {
        id: "jOq5j3265Tw",
        title: "Python Tutorial 13 - While Loops",
        description: "Use while loops for conditional iteration."
    },
    {
        id: "BEvoeyLx9oM",
        title: "Python Tutorial 14 - Maximum and Minimum of List of Numbers",
        description: "Find the max and min values in a list."
    },
    {
        id: "xvuf71GLlww",
        title: "Python Tutorial 15 - Nested Loops",
        description: "Use loops inside other loops for complex iterations."
    },
    {
        id: "ST_pQyLSg78",
        title: "Python Tutorial 16 - Sorting",
        description: "Learn how to sort data using built-in methods."
    },
    {
        id: "bNEbY0HwPmw",
        title: "Python Tutorial 17 - Dictionaries",
        description: "Understand dictionaries and key-value pairs in Python."
    },
    {
        id: "sX5-xSbdEFY",
        title: "Python Tutorial 18 - Dictionary Copying and Updation",
        description: "Copy and update dictionaries."
    },
    {
        id: "dMCmxObS3g0",
        title: "Python Tutorial 19 - Loops with Dictionaries",
        description: "Loop through dictionary keys and values."
    },
    {
        id: "G6IGOZXvCHA",
        title: "Python Tutorial 20 - Dictionary Example",
        description: "Practical example of using dictionaries."
    },
    {
        id: "CT1A-Twctr4",
        title: "Python Tutorial 21 - String Introduction",
        description: "Introduction to strings in Python."
    },
    {
        id: "zufr18LtyIs",
        title: "Python Tutorial 22 - String Examples",
        description: "Examples of working with strings in Python."
    }
];

document.addEventListener('DOMContentLoaded', function() {
    const videoTableBody = document.getElementById('video-table-body');
    
    if (videoTableBody) {
        // Generate table rows for each video
        pythonVideos.forEach((video, index) => {
            const row = document.createElement('tr');
            
            // Create video cell with embedded YouTube player
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
            
            // Create title cell
            const titleCell = document.createElement('td');
            titleCell.className = 'title-cell';
            titleCell.innerHTML = `<h5>${index + 1}. ${video.title}</h5>`;
            
            // Create description cell
            const descCell = document.createElement('td');
            descCell.className = 'desc-cell';
            descCell.textContent = video.description;
            
            // Add all cells to the row
            row.appendChild(videoCell);
            row.appendChild(titleCell);
            row.appendChild(descCell);
            
            // Add the row to the table body
            videoTableBody.appendChild(row);
        });
        
        // Add the Python blog link below the table
        const tableContainer = document.querySelector('.table-responsive');
        const blogLink = document.createElement('div');
        blogLink.className = 'text-center mt-4';
        blogLink.innerHTML = `
            <a href="https://pythonpal.org/blog" class="btn btn-primary" target="_blank">
                <i class="fas fa-external-link-alt me-2"></i>Visit Python Pal Blog
            </a>
        `;
        
        if (tableContainer) {
            tableContainer.parentNode.appendChild(blogLink);
        }
    }
});
