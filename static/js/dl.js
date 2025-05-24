// js/dl_course_data.js

const deepLearningSyllabus = [
    {
        week: 1, // This property will be ignored in rendering
        topic: "Artificial Neural Networks",
        primaryYouTubeLinks: [
            {
                subTopic: "ANN basics",
                links: [
                    { title: "ANN Basic 1", url: "https://youtu.be/6nkylSKqaAc" },
                    { title: "ANN Basic 2", url: "https://youtu.be/ntnwjWEpnkk" },
                    { title: "ANN Basic 3", url: "https://youtu.be/qctUEQn9Hj8" },
                    { title: "ANN Basic 4", url: "https://www.youtube.com/watch?v=llg3gGewQ5U" }
                ]
            },
            {
                subTopic: "Advanced ANN",
                links: [
                    { title: "Advanced ANN 1", url: "https://www.youtube.com/watch?v=nUUqwaxLnWs" },
                    { title: "Advanced ANN 2", url: "https://www.youtube.com/watch?v=dXB-KQYkzNU" },
                    { title: "Advanced ANN 3", url: "https://www.youtube.com/watch?v=NE88eqLnaka" },
                    { title: "Advanced ANN 4", url: "https://www.youtube.com/watch?v=k8fTYJPd3_I" },
                    { title: "Advanced ANN 5 (Playlist)", url: "https://www.youtube.com/watch?v=1waHlpKiNyY&list=PLkDaE6sCZn6Hn0vK8co82zjQtt3T2Nkqc" },
                    { title: "Advanced ANN 6", url: "https://www.youtube.com/watch?v=Gey9CG6R6w8" },
                    { title: "Advanced ANN 7", url: "https://www.youtube.com/watch?v=Q1JCrG1bJ-A" }
                ]
            },
            {
                subTopic: "Deep Learning Intro",
                links: [
                    { title: "DL Intro", url: "https://youtu.be/MTbBOu4M7_M" }
                ]
            }
        ],
        otherReferences: [
            { category: "Universal Approximation Theorem", url: "http://neuralnetworksanddeeplearning.com/chap4.html" },
            { category: "Activation functions", url: "https://towardsdatascience.com/comparison-of-activation-functions-for-deep-neural-networks-706ac4284c8a" },
            { category: "Optimization Algorithms", url: "https://arxiv.org/pdf/1609.04747" },
            { category: "Loss Functions", url: "https://towardsdatascience.com/understanding-different-loss-functions-for-neural-networks-dd1ed0274718" },
            { category: "Vanishing Gradient Problem", url: "https://towardsdatascience.com/the-vanishing-gradient-problem-69bf08b15484" },
            { category: "Regularization for ANN", url: "https://towardsdatascience.com/how-to-improve-a-neural-network-with-regularization-8a18ecda9fe3" },
            { category: "Dropout", url: "https://towardsdatascience.com/dropout-in-neural-networks-47a162d621d9" },
            { category: "Dropout Video", url: "https://www.youtube.com/watch?v=qfsacble9Al" },
            { category: "Embedding layer vs Dense layer", url: "https://medium.com/logivan/neural-network-embedding-and-dense-layers-whats-the-difference-fa177c6d0304" },
            { category: "Difference between Brain and ANN", url: "https://towardsdatascience.com/the-differences-between-artificial-and-biological-neural-networks-a8b46db828b7" },
            { category: "Are ANNs like Human Brain?", url: "https://medium.com/digital-catapult/are-artificial-neural-networks-like-the-human-brain-and-does-it-matter-3add0f029273" },
            { category: "PyTorch Intro Video", url: "https://www.youtube.com/watch?v=Uv0AIRr3ptg" },
            { category: "PyTorch Colab", url: "https://colab.research.google.com/drive/1Pz8b_h-W9zlBk1p2e6v-YFYThG1NkYeS?usp=sharing" },
            { category: "TensorFlow Video Playlist", url: "https://www.youtube.com/watch?v=OHZqmJwi7n4&list=PL9ooVrP1hQOFJ8UZI86fYfmB1_P5yGzBT" },
            { category: "TensorFlow Tutorial", url: "https://www.tutorialspoint.com/tensorflow/index.htm" },
            { category: "House Price Prediction (TF)", url: "https://medium.com/@robertjohn_15390/simple-housing-price-prediction-using-neural-networks-with-tensorflow-8b486d3db3ca" },
            { category: "Image recognition using ANN (Keras)", url: "https://nextjournal.com/gkoehler/digit-recognition-with-keras" },
            { category: "Backpropagation from scratch", url: "https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/" },
            { category: "Boltzmann Machines", url: "https://www.geeksforgeeks.org/grownet-gradient-boosting-neural-networks/" }
        ]
    },
    {
        week: 2, // Ignored
        topic: "Boosting Algorithms",
        primaryYouTubeLinks: [
            {
                subTopic: "Boosting Concepts",
                links: [
                    { title: "Boosting 1", url: "https://www.youtube.com/watch?v=kho60ANGU_A" },
                    { title: "Boosting 2", url: "https://www.youtube.com/watch?v=LsK-xG1cLYA" },
                    { title: "Boosting 3", url: "https://www.youtube.com/watch?v=OtD8wVaFm6E" }
                ]
            }
        ],
        otherReferences: [ /* ... */ ]
    },
    {
        week: 3, // Ignored
        topic: "Computer Vision - Basic CNN Model",
        primaryYouTubeLinks: [
            {
                subTopic: "CNN Basics",
                links: [
                    { title: "CNN Basic 1", url: "https://www.youtube.com/watch?v=UHBmv7qCey4" },
                    { title: "CNN Basic 2", url: "https://www.youtube.com/watch?v=NmLK_WQBXB4" },
                    { title: "CNN Basic 3", url: "https://www.youtube.com/watch?v=QzY57FaENXq" },
                    { title: "CNN Basic 4", url: "https://www.youtube.com/watch?v=HGwBXDKFk9l" },
                    { title: "CNN Basic 5", url: "https://www.youtube.com/watch?v=2-OI7ZB0MmU" }
                ]
            },
            {
                subTopic: "Backprop in CNN",
                links: [
                    { title: "CNN Backprop", url: "https://www.youtube.com/watch?v=pUCCd2-17vl" }
                ]
            },
            {
                subTopic: "Image Segmentation",
                links: [
                    { title: "Image Segmentation", url: "https://www.youtube.com/watch?v=FNHZ64k83e8" }
                ]
            },
            {
                subTopic: "Object Detection using YOLO",
                links: [
                    { title: "YOLO Object Detection", url: "https://www.youtube.com/watch?v=MhftoBaoZpq" }
                ]
            }
        ],
        otherReferences: [
            { category: "NPTEL course on DL for CV by IITM", url: "https://dl4cv-nptel.github.io/DL4CVBK/intro.html" },
            { category: "Comprehensive Guide to CNNs", url: "https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53" },
            { category: "History of CNNs (AlexNet to NASNet)", url: "https://towardsdatascience.com/from-alexnet-to-nasnet-a-brief-history-and-introduction-of-convolutional-neural-networks-cf63bf3320e1" },
            { category: "CNN Video Explainer 1", url: "https://www.youtube.com/watch?v=KuXjwB4LzSA" },
            { category: "CNN Video Explainer 2", url: "https://www.youtube.com/watch?v=umGJ30-15_A" },
            { category: "CNN Code references", url: "" }
        ]
    },
    {
        week: 4, // Ignored
        topic: "Computer Vision - CNN Architectures",
        primaryYouTubeLinks: [
            {
                subTopic: "CNN Architectures Overview",
                links: [
                    { title: "CNN Architectures", url: "https://www.youtube.com/watch?v=DAOcjicFr1Y" }
                ]
            }
        ],
        otherReferences: [
            { category: "CNN Architectures (GeeksForGeeks)", url: "https://www.geeksforgeeks.org/convolutional-neural-network-cnn-architectures/" },
            { category: "CNNs Architectures (Analytics Vidhya)", url: "https://medium.com/analytics-vidhya/cnns-architectures-lenet-alexnet-vgg-googlenet-resnet-and-more-666091488df5" }
        ]
    },
    {
        week: 5, // Ignored
        topic: "Computer Vision - Autoencoders & GANs",
        primaryYouTubeLinks: [
            {
                subTopic: "Autoencoders & GANs",
                links: [
                    { title: "Autoencoders & GANs 1", url: "https://www.youtube.com/watch?v=5WoltGTWV54" },
                    { title: "Autoencoders & GANs 2", url: "https://www.youtube.com/watch?v=9zKuYvjFFS8" }
                ]
            }
        ],
        otherReferences: [
            { category: "GANs for MNIST digits (Keras)", url: "https://machinelearningmastery.com/how-to-develop-a-generative-adversarial-network-for-an-mnist-handwritten-digits-from-scratch-in-keras/" },
            { category: "Generative Adversarial Network GAN (Pathmind)", url: "https://wiki.pathmind.com/generative-adversarial-network-gan" }
        ]
    },
    {
        week: 6, // Ignored
        topic: "Computer Vision - Practical Considerations",
        primaryYouTubeLinks: [ /* No primary links listed for week 6 in OCR */ ],
        otherReferences: [
            { category: "CNNs Practical Perspective", url: "https://towardsdatascience.com/convolutional-neural-networks-cnns-a-practical-perspective-c7b3b2091aa8" }
        ]
    },
    {
        week: 7, // Ignored
        topic: "Sequence Modeling - RNNs and LSTMs I",
        primaryYouTubeLinks: [
            {
                subTopic: "RNN & LSTM Theory",
                links: [
                    { title: "RNN & LSTM Theory", url: "https://www.youtube.com/watch?v=6nigTuYFZLQ" }
                ]
            }
        ],
        otherReferences: [
            { category: "Understanding LSTMs (Colah's Blog)", url: "http://colah.github.io/posts/2015-08-Understanding-LSTMS/" },
            { category: "The Unreasonable Effectiveness of RNNs (Karpathy)", url: "http://karpathy.github.io/2015/05/21/rnn-effectiveness/" },
            { category: "RNN & LSTM Video (StatQuest)", url: "https://www.youtube.com/watch?v=WCUNPb-5EYI" },
            { category: "Exploring LSTMs (Edwin Chen)", url: "http://blog.echen.me/2017/05/30/exploring-lstms/" },
            { category: "Dropout in RNNs", url: "https://adriangcoder.medium.com/a-review-of-dropout-as-applied-to-rnns-72e79ecd5b2b" },
            { category: "RNN Regularization (arXiv)", url: "https://arxiv.org/abs/1409.2329" },
            { category: "RNN Regularization (StackOverflow)", url: "https://stackoverflow.com/questions/48714407/rnn-regularization-which-component-to-regularize" },
            { category: "Word Embeddings Survey", url: "https://medium.com/@phylypo/a-survey-of-the-state-of-the-art-language-models-up-to-early-2020-aba824302c6" }
        ]
    },
    {
        week: 8, // Ignored
        topic: "Sequence Modeling - RNNs and LSTMs II",
        primaryYouTubeLinks: [
            {
                subTopic: "RNN & LSTM Practical",
                links: [
                    // No specific YouTube link given for "RNN & LSTM Practical" in the OCR, Karpathy link is repeated
                ]
            }
        ],
        otherReferences: [
            { category: "RNN & LSTM Code (Karpathy)", url: "https://karpathy.github.io/2015/05/21/rnn-effectiveness/" },
            { category: "Stacked LSTMs", url: "https://machinelearningmastery.com/stacked-long-short-term-memory-networks/" },
            { category: "Return Sequences and States for LSTMs (Keras)", url: "https://machinelearningmastery.com/return-sequences-and-return-states-for-lstms-in-keras/" },
            { category: "LSTM Regularization", url: "https://machinelearningmastery.com/use-weight-regularization-lstm-networks-time-series-forecasting/" }
        ]
    },
    {
        week: 9, // Ignored
        topic: "NLP - Transformer Architecture and LLMs",
        primaryYouTubeLinks: [
            {
                subTopic: "Transformer & LLMs",
                links: [
                    { title: "Transformer & LLMs", url: "https://www.youtube.com/watch?v=SZorAJ4I-sA" },
                    { title: "Transformer & LLMs 2", url: "https://www.youtube.com/watch?v=TQQIZhbC5ps" },
                    { title: "Transformer & LLMs 3", url: "https://www.youtube.com/watch?v=wjZofJX0v4M" },
                    { title: "Transformer & LLMs 4", url: "https://www.youtube.com/watch?v=eMIx5fFNoYc" },
                    { title: "Transformer & LLMs 5", url: "https://www.youtube.com/watch?v=OyFJWRnt_AY" },
                    { title: "Transformer & LLMs 6", url: "https://www.youtube.com/watch?v=UPtG_38Oq80" }
                ]
            }
        ],
        otherReferences: [
            { category: "The Illustrated Transformer (Jay Alammar)", url: "https://jalammar.github.io/illustrated-transformer/" },
            { category: "Is Attention explanation?", url: "" },
            { category: "Code for LLM Inference", url: "" },
            { category: "Tokenization using BPE, Unigram and WordPiece", url: "https://blog.floydhub.com/tokenization-nlp/" },
            { category: "WordPiece Tokenization by HuggingFace", url: "" },
            { category: "BERT: Dissecting BERT Part 1", url: "https://medium.com/@mromerocalvo/dissecting-bert-part1-6dcf5360b07f" },
            { category: "ChrisMcCormickAI Videos (BERT)", url: "https://www.youtube.com/c/ChrisMcCormickAl/videos" },
            { category: "The Illustrated BERT (Jay Alammar)", url: "http://jalammar.github.io/illustrated-bert/" },
            { category: "GPT-3: A Complete Overview", url: "https://towardsdatascience.com/gpt-3-a-complete-overview-190232eb2559" },
            { category: "Annotated Transformer (Harvard NLP)", url: "http://nlp.seas.harvard.edu/2018/04/03/attention.html" },
            { category: "Attention Video Series", url: "https://www.youtube.com/watch?v=Osj0Z6rwJB4&list=PLEJK-H61XlwxpfpVzt30DLQ8vr1XiEhev&index=2" },
            { category: "Positional Encoding Blog", url: "https://kazemnejad.com/blog/transformer_architecture_positional_encoding/" },
            { category: "Master Positional Encoding Part I", url: "https://towardsdatascience.com/master-positional-encoding-part-i-63c05d90a0c3" },
            { category: "Understanding Positional Embeddings (Absolute to Rotary)", url: "https://towardsdatascience.com/understanding-positional-embeddings-in-transformers-from-absolute-to-rotary-31c082e16b26" }
        ]
    },
    {
        week: 10, // Ignored
        topic: "NLP - LLM Pre-Training",
        primaryYouTubeLinks: [
            {
                subTopic: "LLM Pre-Training",
                links: [
                    { title: "LLM Pre-Training", url: "https://www.youtube.com/watch?v=knTc-NQSİKA" }
                ]
            }
        ],
        otherReferences: [
            { category: "LLM Notebooks by Anish", url: "https://github.com/anishiisc/Build_LLM_from_Scratch/tree/main" },
            { category: "Pre-Training and Fine-Tuning", url: "" },
            { category: "BERT MLM Task Details", url: "" },
            { category: "In-Context Learning", url: "" },
            { category: "Gen AI Hyperparameters", url: "" },
            { category: "LLM Model Details", url: "" }
        ]
    },
    {
        week: 11, // Ignored
        topic: "NLP - Fine Tuning LLMs",
        primaryYouTubeLinks: [
            {
                subTopic: "Fine Tuning LLMs",
                links: [
                    { title: "Fine Tuning LLMs 1", url: "https://www.youtube.com/watch?v=kCc8FmEb1nY" },
                    { title: "Fine Tuning LLMs 2", url: "https://www.youtube.com/watch?v=mw7ay38--ak" },
                    { title: "Fine Tuning LLMs 3", url: "https://www.youtube.com/watch?v=dzyDHMусх_c" }
                ]
            }
        ],
        otherReferences: [
            { category: "Code for Fine-tuning BERT & LLaMA", url: "" },
            { category: "WeightWatcher.ai", url: "https://weightwatcher.ai" },
            { category: "Text Classification (Fine-tuning BERT)", url: "https://www.thepythoncode.com/article/finetuning-bert-using-huggingface-transformers-python" },
            { category: "Sentiment Analysis with BERT (PyTorch)", url: "https://curiousily.com/posts/sentiment-analysis-with-bert-and-hugging-face-using-pytorch-and-python/" },
            { category: "Text Classification with Transformers (Chaturanga)", url: "https://towardsdatascience.com/https-medium-com-chaturangarajapakshe-text-classification-with-transformer-models-d370944b50ca" },
            { category: "NER: Named Entity Recognition with BERT", url: "https://www.depends-on-the-definition.com/named-entity-recognition-with-bert/" },
            { category: "NER with BERT in PyTorch", url: "https://towardsdatascience.com/named-entity-recognition-with-bert-in-pytorch-a454405e0b6a" }
        ]
    },
    {
        week: 12, // Ignored
        topic: "NLP - Retrieval Augmented Generation",
        primaryYouTubeLinks: [
            {
                subTopic: "RAG",
                links: [
                    { title: "RAG (Playlist)", url: "https://www.youtube.com/watch?v=wd7TZ4w1mSw&list=PLfaDFEXuae2LXbO1_PKyVJiQ23ZztA0x" },
                    { title: "RAG 2", url: "https://www.youtube.com/watch?v=ahnGLM-RC1Y" }
                ]
            }
        ],
        otherReferences: [
            { category: "Sentence Similarity using BERT and SBERT", url: "" },
            { category: "Limitation of IR using LLMs", url: "" },
            { category: "RAG using LangChain", url: "" }
        ]
    },
    {
        week: 13, // Ignored
        topic: "Image Captioning, Text to Image",
        primaryYouTubeLinks: [
            {
                subTopic: "Image/Text Generation",
                links: [
                    { title: "Image Captioning/Text to Image 1", url: "https://www.youtube.com/watch?v=JmATtG0yA5E" },
                    { title: "Image Captioning/Text to Image 2", url: "https://www.youtube.com/watch?v=pea3sH6orMc" },
                    { title: "Image Captioning/Text to Image 3", url: "https://www.youtube.com/watch?v=fUSTbGrL1tc" },
                    { title: "Image Captioning/Text to Image 4", url: "https://www.youtube.com/watch?v=LWIZİ_RJYİM" },
                    { title: "Image Captioning/Text to Image 5", url: "https://www.youtube.com/watch?v=aaP7JJZuvGs" }
                ]
            }
        ],
        otherReferences: [
            { category: "The Illustrated Stable Diffusion", url: "https://jalammar.github.io/illustrated-stable-diffusion/" },
            { category: "Stable Diffusion Video", url: "https://www.youtube.com/watch?v=hCmka_vC70A" },
            { category: "Diffusion Models Video", url: "https://www.youtube.com/watch?v=9BHQvQIsVdE" }
        ]
    },
    {
        week: 14, // Ignored
        topic: "Deployment",
        primaryYouTubeLinks: [ /* No primary links listed for week 14 in OCR */ ],
        otherReferences: [
            { category: "Full Stack Deep Learning Course (2022)", url: "https://fullstackdeeplearning.com/course/2022/" }
        ]
    }
];

const courseInfo = {
    instructor: "Dr. Kushal Shah",
    prerequisite: "Before starting to learn Deep Learning, make sure to first learn basics of Machine Learning."
};

const textbooks = [
    "Understanding Deep Learning by Simon Prince",
    "Deep Learning by Ian Goodfellow, Yoshua Bengio & Aaron Courville",
    "Deep Learning by Christopher Bishop and Hugh Bishop"
];

// nlpReferences can be removed if not used, or kept for future general NLP links.
// const nlpReferences = [];


document.addEventListener('DOMContentLoaded', function() {
    const dlTableBody = document.getElementById('dl-table-body');
    const coursePreamble = document.getElementById('course-preamble');
    const courseTextbooks = document.getElementById('course-textbooks');

    if (coursePreamble) {
        coursePreamble.innerHTML = `
            <p><strong>Instructor:</strong> ${courseInfo.instructor}</p>
            <p class="alert alert-warning"><strong>Prerequisite:</strong> ${courseInfo.prerequisite}</p>
        `;
    }
    
    if (dlTableBody) {
        deepLearningSyllabus.forEach(item => {
            const row = document.createElement('tr');
            
            // REMOVED Week Cell
            // const weekCell = document.createElement('td');
            // weekCell.textContent = item.week;
            // row.appendChild(weekCell);

            // Topic Cell
            const topicCell = document.createElement('td');
            topicCell.innerHTML = `<strong>${item.topic}</strong>`;
            row.appendChild(topicCell);

            // Primary YouTube Links Cell
            const primaryLinksCell = document.createElement('td');
            if (item.primaryYouTubeLinks && item.primaryYouTubeLinks.length > 0) {
                item.primaryYouTubeLinks.forEach(group => {
                    const groupDiv = document.createElement('div');
                    groupDiv.classList.add('mb-2');
                    if (group.subTopic) {
                         groupDiv.innerHTML += `<h6>${group.subTopic}</h6>`;
                    }
                    const ul = document.createElement('ul');
                    ul.classList.add('list-unstyled', 'ps-2');
                    group.links.forEach(link => {
                        const li = document.createElement('li');
                        if (item.primaryYouTubeLinks.indexOf(group) === 0 && group.links.indexOf(link) === 0 && link.url.includes("youtu")) {
                             li.innerHTML = `
                                <p><a href="${link.url}" target="_blank">${link.title || 'Watch Video'} <i class="fas fa-external-link-alt fa-xs"></i></a></p>
                                <div class="video-container mb-2">
                                    <iframe 
                                        src="https://www.youtube.com/embed/${getYoutubeId(link.url)}" 
                                        title="${link.title || 'YouTube Video'}" 
                                        frameborder="0" 
                                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                        allowfullscreen>
                                    </iframe>
                                </div>
                            `;
                        } else {
                            li.innerHTML = `<a href="${link.url}" target="_blank">${link.title || 'Link'} <i class="fas fa-external-link-alt fa-xs"></i></a>`;
                        }
                        ul.appendChild(li);
                    });
                    groupDiv.appendChild(ul);
                    primaryLinksCell.appendChild(groupDiv);
                });
            } else {
                primaryLinksCell.textContent = 'N/A';
            }
            row.appendChild(primaryLinksCell);

            // Other References Cell
            const otherReferencesCell = document.createElement('td');
            if (item.otherReferences && item.otherReferences.length > 0) {
                const ul = document.createElement('ul');
                ul.classList.add('list-unstyled');
                item.otherReferences.forEach(ref => {
                    const li = document.createElement('li');
                    if (ref.url) {
                        li.innerHTML = `<strong>${ref.category || 'Reference'}:</strong> <a href="${ref.url}" target="_blank">${ref.url.substring(0,50)}... <i class="fas fa-external-link-alt fa-xs"></i></a>`;
                    } else {
                        li.innerHTML = `<strong>${ref.category || 'Reference'}:</strong> N/A`;
                    }
                    ul.appendChild(li);
                });
                otherReferencesCell.appendChild(ul);
            } else {
                otherReferencesCell.textContent = 'N/A';
            }
            row.appendChild(otherReferencesCell);
            
            dlTableBody.appendChild(row);
        });
    }

    if (courseTextbooks && textbooks.length > 0) {
        let html = '<h4>Recommended Textbooks</h4><ul class="list-group">';
        textbooks.forEach(book => {
            html += `<li class="list-group-item">${book}</li>`;
        });
        html += '</ul>';
        courseTextbooks.innerHTML = html;
    }

});

function getYoutubeId(url) {
    if (!url) return '';
    let videoId = '';
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    if (match && match[2].length === 11) {
        videoId = match[2];
    } else {
        const parts = url.split('/');
        videoId = parts[parts.length -1];
        if(videoId.includes("?")) videoId = videoId.substring(0, videoId.indexOf("?"));
    }
    return videoId;
}
