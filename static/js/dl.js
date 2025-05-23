// static/js/dl_data.js

const courseData = {
    instructor: "Dr. Kushal Shah",
    prerequisite: "Machine Learning",
    weeks: [
        {
            weekNumber: 1,
            topic: "Artificial Neural Networks",
            primaryMaterial: [
                {
                    title: "ANN basics",
                    videos: [
                        { url: "https://youtu.be/6nkylSKqaAc", description: "ANN basics 1" },
                        { url: "https://youtu.be/ntnwjWEpnkk", description: "ANN basics 2" },
                        { url: "https://youtu.be/qctUEQn9Hj8", description: "ANN basics 3" },
                        { url: "https://www.youtube.com/watch?v=llg3gGewQ5U", description: "ANN basics 4" }
                    ]
                },
                {
                    title: "Advanced ANN",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=nUUqwaxLnWs", description: "Advanced ANN 1" },
                        { url: "https://www.youtube.com/watch?v=dXB-KQYkzNU", description: "Advanced ANN 2" },
                        { url: "https://www.youtube.com/watch?v=NE88eqLnaka", description: "Advanced ANN 3" },
                        { url: "https://www.youtube.com/watch?v=k8fTYJPd3_I", description: "Advanced ANN 4" }, // Corrected ID, was k8fTYJPd3 |
                        { url: "https://www.youtube.com/watch?v=1waHlpKiNyY&list=PLkDaE6sCZn6Hn0vK8co82zjQtt3T2Nkqc", description: "Advanced ANN 5 (Playlist item)" },
                        { url: "https://www.youtube.com/watch?v=Gey9CG6R6w8", description: "Advanced ANN 6" },
                        { url: "https://www.youtube.com/watch?v=Q1JCrG1bJ-A", description: "Advanced ANN 7" }
                    ]
                },
                {
                    title: "Deep Learning Intro",
                    videos: [
                        { url: "https://youtu.be/MTbBOu4M7_M", description: "Deep Learning Intro Video" } // Corrected ID, was MTbBOu4M7 M
                    ]
                }
            ],
            otherReferences: [
                { title: "Universal Approximation Theorem", url: "http://neuralnetworksanddeeplearning.com/chap4.html" },
                { title: "Activation functions Comparison", url: "https://towardsdatascience.com/comparison-of-activation-functions-for-deep-neural-networks-706ac4284c8a" },
                { title: "Optimization Algorithms", url: "https://arxiv.org/pdf/1609.04747" },
                { title: "Loss Functions", url: "https://towardsdatascience.com/understanding-different-loss-functions-for-neural-networks-dd1ed0274718" },
                { title: "Vanishing Gradient Problem", url: "https://towardsdatascience.com/the-vanishing-gradient-problem-69bf08b15484" },
                { title: "Regularization for ANN", url: "https://towardsdatascience.com/how-to-improve-a-neural-network-with-regularization-8a18ecda9fe3" },
                { title: "Dropout in Neural Networks", url: "https://towardsdatascience.com/dropout-in-neural-networks-47a162d621d9" },
                { title: "Dropout (YouTube)", url: "https://www.youtube.com/watch?v=qfsacble9Al" },
                { title: "Embedding layer vs Dense layer", url: "https://medium.com/logivan/neural-network-embedding-and-dense-layers-whats-the-difference-fa177c6d0304" },
                { title: "Difference between Brain and ANN (Towards Data Science)", url: "https://towardsdatascience.com/the-differences-between-artificial-and-biological-neural-networks-a8b46db828b7" },
                { title: "Are artificial neural networks like the human brain? (Medium)", url: "https://medium.com/digital-catapult/are-artificial-neural-networks-like-the-human-brain-and-does-it-matter-3add0f029273" },
                { title: "PyTorch (YouTube)", url: "https://www.youtube.com/watch?v=Uv0AIRr3ptg" },
                { title: "TensorFlow Colab", url: "https://colab.research.google.com/drive/1Pz8b_h-W9zlBk1p2e6v-YFYThG1NkYeS?usp=sharing"},
                { title: "TensorFlow (YouTube Playlist)", url: "https://www.youtube.com/watch?v=OHZqmJwi7n4&list=PL9ooVrP1hQOFJ8UZI86fYfmB1_P5yGzBT"},
                { title: "TensorFlow Tutorialspoint", url: "https://www.tutorialspoint.com/tensorflow/index.htm"},
                { title: "House Price Prediction (Medium)", url: "https://medium.com/@robertjohn_15390/simple-housing-price-prediction-using-neural-networks-with-tensorflow-8b486d3db3ca"},
                { title: "Image recognition using ANN (Nextjournal)", url: "https://nextjournal.com/gkoehler/digit-recognition-with-keras"},
                { title: "Backpropagation from scratch (Machine Learning Mastery)", url: "https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/"}
            ]
        },
        {
            weekNumber: 2,
            topic: "Boosting Algorithms",
            primaryMaterial: [
                {
                    title: "Boosting Algorithms",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=kho60ANGU_A", description: "Boosting 1" }, // Corrected ID
                        { url: "https://www.youtube.com/watch?v=LsK-xG1cLYA", description: "Boosting 2" },
                        { url: "https://www.youtube.com/watch?v=OtD8wVaFm6E", description: "Boosting 3" }
                    ]
                }
            ],
            otherReferences: [
                { title: "Boltzmann Machines (GeeksForGeeks)", url: "https://www.geeksforgeeks.org/grownet-gradient-boosting-neural-networks/"} // Note: Link text says grownet, PDF says Boltzmann
            ]
        },
        {
            weekNumber: 3,
            topic: "Computer Vision - Basic CNN Model",
            primaryMaterial: [
                {
                    title: "Basic CNN Model",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=UHBmv7qCey4", description: "CNN Basics 1" },
                        { url: "https://www.youtube.com/watch?v=NmLK_WQBXB4", description: "CNN Basics 2" },
                        { url: "https://www.youtube.com/watch?v=QzY57FaENXq", description: "CNN Basics 3" },
                        { url: "https://www.youtube.com/watch?v=HGwBXDKFk9I", description: "CNN Basics 4" }, // Corrected ID
                        { url: "https://www.youtube.com/watch?v=2-OI7ZB0MmU", description: "CNN Basics 5" }
                    ]
                },
                {
                    title: "Backprop in CNN",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=pUCCd2-17vI", description: "Backprop in CNN" } // Corrected ID
                    ]
                },
                {
                    title: "Image Segmentation",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=FNHZ64k83e8", description: "Image Segmentation" }
                    ]
                },
                {
                    title: "Object Detection using YOLO",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=MhftoBaoZpq", description: "YOLO Object Detection" }
                    ]
                }
            ],
            otherReferences: [
                { title: "NPTEL course on DL for CV by IITM", url: "https://dl4cv-nptel.github.io/DL4CVBK/intro.html" },
                { title: "Comprehensive Guide to CNNs (Towards Data Science)", url: "https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53" },
                { title: "From AlexNet to NASNet (Towards Data Science)", url: "https://towardsdatascience.com/from-alexnet-to-nasnet-a-brief-history-and-introduction-of-convolutional-neural-networks-cf63bf3320e1" },
                { title: "CNN Architectures (YouTube)", url: "https://www.youtube.com/watch?v=KuXjwB4LzSA" },
                { title: "CNN Layers (YouTube)", url: "https://www.youtube.com/watch?v=umGJ30-15_A" }, // Corrected ID
                { title: "CNN Code references", url: "#" } // Placeholder if specific link intended or link to a repo
            ]
        },
        {
            weekNumber: 4,
            topic: "Computer Vision - CNN Architectures",
            primaryMaterial: [
                 {
                    title: "CNN Architectures",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=DAOcjicFr1Y", description: "CNN Architectures Overview" }
                    ]
                }
            ],
            otherReferences: [
                { title: "CNN Architectures (GeeksForGeeks)", url: "https://www.geeksforgeeks.org/convolutional-neural-network-cnn-architectures/" },
                { title: "CNNs Architectures: LeNet, AlexNet, VGG, GoogLeNet, ResNet and more (Medium)", url: "https://medium.com/analytics-vidhya/cnns-architectures-lenet-alexnet-vgg-googlenet-resnet-and-more-666091488df5" }
            ]
        },
        {
            weekNumber: 5,
            topic: "Computer Vision - Autoencoders & GANs",
            primaryMaterial: [
                {
                    title: "Autoencoders & GANs",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=5WoltGTWV54", description: "Autoencoders" },
                        { url: "https://www.youtube.com/watch?v=9zKuYvjFFS8", description: "GANs" }
                    ]
                }
            ],
            otherReferences: [
                { title: "GANs for MNIST digits (Machine Learning Mastery)", url: "https://machinelearningmastery.com/how-to-develop-a-generative-adversarial-network-for-an-mnist-handwritten-digits-from-scratch-in-keras/" },
                { title: "Generative Adversarial Network (Pathmind Wiki)", url: "https://wiki.pathmind.com/generative-adversarial-network-gan" }
            ]
        },
        {
            weekNumber: 6,
            topic: "Computer Vision - Practical Considerations",
            primaryMaterial: [ /* No primary YouTube links listed in PDF for this week */ ],
            otherReferences: [
                { title: "CNNs: A Practical Perspective (Towards Data Science)", url: "https://towardsdatascience.com/convolutional-neural-networks-cnns-a-practical-perspective-c7b3b2091aa8" }
            ]
        },
        {
            weekNumber: 7,
            topic: "Sequence Modeling - RNNs and LSTMs I",
            primaryMaterial: [
                {
                    title: "RNN & LSTM Theory",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=6nigTuYFZLQ", description: "RNN & LSTM Theory" }
                    ]
                }
            ],
            otherReferences: [
                { title: "Understanding LSTMs (Colah's Blog)", url: "http://colah.github.io/posts/2015-08-Understanding-LSTMs/" },
                { title: "The Unreasonable Effectiveness of RNNs (Karpathy's Blog)", url: "http://karpathy.github.io/2015/05/21/rnn-effectiveness/" },
                { title: "RNN, LSTM & GRU (YouTube)", url: "https://www.youtube.com/watch?v=WCUNPb-5EYI" },
                { title: "Exploring LSTMs (Edwin Chen's Blog)", url: "http://blog.echen.me/2017/05/30/exploring-lstms/" },
                { title: "Dropout in RNNs (Medium)", url: "https://adriangcoder.medium.com/a-review-of-dropout-as-applied-to-rnns-72e79ecd5b2b" }, // Corrected URL ending
                { title: "RNN Regularization (arXiv)", url: "https://arxiv.org/abs/1409.2329" },
                { title: "RNN Regularization - Which component to regularize? (Stack Overflow)", url: "https://stackoverflow.com/questions/48714407/rnn-regularization-which-component-to-regularize" },
                { title: "Word Embeddings Survey (Medium)", url: "https://medium.com/@phylypo/a-survey-of-the-state-of-the-art-language-models-up-to-early-2020-aba824302c6" }
            ]
        },
        {
            weekNumber: 8,
            topic: "Sequence Modeling - RNNs and LSTMs II",
            primaryMaterial: [
                {
                    title: "RNN & LSTM Practical",
                    videos: [ /* No specific video for this, implies using Karpathy's blog from Week 7 */ ]
                }
            ],
            otherReferences: [
                { title: "RNN & LSTM Code (Karpathy's Blog - same as week 7)", url: "https://karpathy.github.io/2015/05/21/rnn-effectiveness/" },
                { title: "Stacked LSTMs (Machine Learning Mastery)", url: "https://machinelearningmastery.com/stacked-long-short-term-memory-networks/" },
                { title: "Return Sequences and Return States for LSTMs in Keras (Machine Learning Mastery)", url: "https://machinelearningmastery.com/return-sequences-and-return-states-for-lstms-in-keras/" },
                { title: "LSTM Regularization (Machine Learning Mastery)", url: "https://machinelearningmastery.com/use-weight-regularization-lstm-networks-time-series-forecasting/" }
            ]
        },
        {
            weekNumber: 9,
            topic: "NLP - Transformer Architecture and LLMs",
            primaryMaterial: [
                {
                    title: "Transformer Architecture",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=SZorAJ4I-sA", description: "Transformer Introduction" }, // Corrected ID
                        { url: "https://www.youtube.com/watch?v=TQQIZhbC5ps", description: "Transformers Explained 1" },
                        { url: "https://www.youtube.com/watch?v=wjZofJX0v4M", description: "Transformers Explained 2" },
                        { url: "https://www.youtube.com/watch?v=eMIx5fFNoYc", description: "Transformers Explained 3" },
                        { url: "https://www.youtube.com/watch?v=OyFJWRnt_AY", description: "Transformers Explained 4" }, // Corrected ID
                        { url: "https://www.youtube.com/watch?v=UPtG_38Oq80", description: "Transformers Explained 5" } // Corrected ID
                    ]
                }
            ],
            otherReferences: [
                { title: "The Illustrated Transformer (Jay Alammar)", url: "https://jalammar.github.io/illustrated-transformer/" },
                { title: "Is Attention explanation?", url: "#" }, // Placeholder
                { title: "Code for LLM Inference", url: "#" }, // Placeholder
                { title: "Tokenization using BPE, Unigram and WordPiece (FloydHub)", url: "https://blog.floydhub.com/tokenization-nlp/" },
                { title: "WordPiece Tokenization by HuggingFace", url: "#" }, // Placeholder - specific link needed
                { title: "Dissecting BERT (Medium)", url: "https://medium.com/@mromerocalvo/dissecting-bert-part1-6dcf5360b07f" },
                { title: "Chris McCormick AI Videos (BERT Explained)", url: "https://www.youtube.com/c/ChrisMcCormickAl/videos" },
                { title: "The Illustrated BERT (Jay Alammar)", url: "http://jalammar.github.io/illustrated-bert/" },
                { title: "GPT-3: A Complete Overview (Towards Data Science)", url: "https://towardsdatascience.com/gpt-3-a-complete-overview-190232eb259f" }, // Corrected ID
                { title: "The Annotated Transformer (Harvard NLP)", url: "http://nlp.seas.harvard.edu/2018/04/03/attention.html" },
                { title: "Attention & Transformers (YouTube Playlist)", url: "https://www.youtube.com/watch?v=Osj0Z6rwJB4&list=PLEJK-H61XlwxpfpVzt30DLQ8vr1XiEhev&index=2" },
                { title: "Positional Encoding in Transformer (Kazemnejad Blog)", url: "https://kazemnejad.com/blog/transformer_architecture_positional_encoding/" },
                { title: "Master Positional Encoding (Towards Data Science)", url: "https://towardsdatascience.com/master-positional-encoding-part-i-63c05d90a0c3" },
                { title: "Understanding Positional Embeddings (Towards Data Science)", url: "https://towardsdatascience.com/understanding-positional-embeddings-in-transformers-from-absolute-to-rotary-31c082e16b26" }
            ]
        },
        {
            weekNumber: 10,
            topic: "NLP - LLM Pre-Training",
            primaryMaterial: [
                {
                    title: "LLM Pre-Training",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=knTc-NQSİKA", description: "LLM Pre-Training" } // Note: ID has a special char 'İ'
                    ]
                }
            ],
            otherReferences: [
                { title: "LLM Notebooks by Anish (GitHub)", url: "https://github.com/anishiisc/Build_LLM_from_Scratch/tree/main" },
                { title: "Pre-Training and Fine-Tuning", url: "#" }, // Placeholder
                { title: "BERT MLM Task Details", url: "#" }, // Placeholder
                { title: "In-Context Learning", url: "#" }, // Placeholder
                { title: "Gen AI Hyperparameters", url: "#" }, // Placeholder
                { title: "LLM Model Details", url: "#" } // Placeholder
            ]
        },
        {
            weekNumber: 11,
            topic: "NLP - Fine Tuning LLMs",
            primaryMaterial: [
                {
                    title: "Fine Tuning LLMs",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=kCc8FmEb1nY", description: "Fine Tuning LLMs 1" },
                        { url: "https://www.youtube.com/watch?v=mw7ay38--ak", description: "Fine Tuning LLMs 2" },
                        { url: "https://www.youtube.com/watch?v=dzyDHMусх_с", description: "Fine Tuning LLMs 3" } // Note: Special chars in ID
                    ]
                }
            ],
            otherReferences: [
                { title: "Code for Fine-tuning BERT & LLaMA", url: "#" }, // Placeholder
                { title: "WeightWatcher.ai", url: "https://weightwatcher.ai" }
            ]
        },
        {
            weekNumber: 12,
            topic: "NLP - Retrieval Augmented Generation",
            primaryMaterial: [
                {
                    title: "Retrieval Augmented Generation (RAG)",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=wd7TZ4w1mSw&list=PLfaDEFXuae2LXbO1_PKyVJiQ23ZztA0x", description: "RAG Overview (Playlist item)" },
                        { url: "https://www.youtube.com/watch?v=ahnGLM-RC1Y", description: "RAG Details" }
                    ]
                }
            ],
            otherReferences: [
                { title: "Text Classification: Finetuning BERT (The Python Code)", url: "https://www.thepythoncode.com/article/finetuning-bert-using-huggingface-transformers-python" },
                { title: "Sentiment Analysis with BERT (Curiousily)", url: "https://curiousily.com/posts/sentiment-analysis-with-bert-and-hugging-face-using-pytorch-and-python/" },
                { title: "Text Classification with Transformer Models (Towards Data Science)", url: "https://towardsdatascience.com/https-medium-com-chaturangarajapakshe-text-classification-with-transformer-models-d370944b50ca" },
                { title: "NER: Named Entity Recognition with BERT (Depends On The Definition)", url: "https://www.depends-on-the-definition.com/named-entity-recognition-with-bert/" },
                { title: "Named Entity Recognition with BERT in PyTorch (Towards Data Science)", url: "https://towardsdatascience.com/named-entity-recognition-with-bert-in-pytorch-a454405e0b6a" },
                { title: "Sentence Similarity using BERT and SBERT", url: "#" }, // Placeholder
                { title: "Limitation of IR using LLMs", url: "#" }, // Placeholder
                { title: "RAG using LangChain", url: "#" } // Placeholder
            ]
        },
        {
            weekNumber: 13,
            topic: "Image Captioning, Text to Image",
            primaryMaterial: [
                {
                    title: "Image Captioning & Text to Image",
                    videos: [
                        { url: "https://www.youtube.com/watch?v=JmATtG0yA5E", description: "Image Captioning" },
                        { url: "https://www.youtube.com/watch?v=pea3sH6orMc", description: "Text to Image" },
                        { url: "https://www.youtube.com/watch?v=fUSTbGrL1tc", description: "Text to Image Models 1" },
                        { url: "https://www.youtube.com/watch?v=LWIZi_RJYIM", description: "Text to Image Models 2" }, // Corrected ID
                        { url: "https://www.youtube.com/watch?v=aaP7JJZuvGs", description: "Text to Image Models 3" } // Corrected ID
                    ]
                }
            ],
            otherReferences: [
                { title: "The Illustrated Stable Diffusion (Jay Alammar)", url: "https://jalammar.github.io/illustrated-stable-diffusion/" },
                { title: "Diffusion Models Details (YouTube)", url: "https://www.youtube.com/watch?v=hCmka_vC70A" },
                { title: "Diffusion Models Explained (YouTube)", url: "https://www.youtube.com/watch?v=9BHQvQIsVdE" }
            ]
        },
        {
            weekNumber: 14,
            topic: "Deployment",
            primaryMaterial: [ /* No primary YouTube links listed */ ],
            otherReferences: [
                { title: "Full Stack Deep Learning Course (2022)", url: "https://fullstackdeeplearning.com/course/2022/" }
            ]
        }
    ],
    textbooks: [
        { title: "Understanding Deep Learning by Simon Prince", url: null },
        { title: "Deep Learning by Ian Goodfellow, Yoshua Bengio & Aaron Courville", url: "https://www.deeplearningbook.org/" }, // Added official link
        { title: "Deep Learning by Christopher Bishop and Hugh Bishop", url: null } // Note: This might be "Deep Learning: Foundations and Concepts" by Bishop
    ],
    referencesForNLP: [ // Assuming this is a general NLP ref section
        // If there are specific NLP reference links, add them here as { title: "...", url: "..." }
        // The PDF only lists "References for NLP" as a heading.
    ]
};
