const videos = [
    {
        embed: `<iframe width="300" height="170" src="https://www.youtube.com/embed/aircAruvnKk" title="Deep Learning in 5 Minutes" frameborder="0" allowfullscreen></iframe>`,
        title: "Deep Learning in 5 Minutes",
        description: "A quick overview of what deep learning is and how it works."
    },
    {
        embed: `<iframe width="300" height="170" src="https://www.youtube.com/embed/ILsA4nyG7I0" title="Neural Networks from Scratch" frameborder="0" allowfullscreen></iframe>`,
        title: "Neural Networks from Scratch",
        description: "Learn how to build and train neural networks from the ground up."
    },
    {
        embed: `<iframe width="300" height="170" src="https://www.youtube.com/embed/bNmRXvT7hHw" title="CNN Explained" frameborder="0" allowfullscreen></iframe>`,
        title: "Convolutional Neural Networks Explained",
        description: "A visual explanation of CNNs and their role in image processing."
    },
    {
        embed: `<iframe width="300" height="170" src="https://www.youtube.com/embed/6g4O5UOH304" title="RNNs and LSTMs" frameborder="0" allowfullscreen></iframe>`,
        title: "Recurrent Neural Networks (RNNs) and LSTMs",
        description: "Understand how RNNs and LSTMs work for sequential data."
    },
    {
        embed: `<iframe width="300" height="170" src="https://www.youtube.com/embed/U0s0f995w14" title="Transformers in NLP" frameborder="0" allowfullscreen></iframe>`,
        title: "Transformers in NLP",
        description: "Introduction to the Transformer architecture used in models like BERT and GPT."
    }
];

const videoTable = document.getElementById("video-table-body");

videos.forEach(video => {
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${video.embed}</td>
        <td>${video.title}</td>
        <td>${video.description}</td>
    `;
    videoTable.appendChild(row);
});
