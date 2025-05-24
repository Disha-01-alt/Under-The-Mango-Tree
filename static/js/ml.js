// static/js/ml.js

const courseData = {
    // instructor: "Dr. Kushal Shah", // Instructor REMOVED as per request
    prerequisite: "Python Programming and Data Handling using Python", // From PDF header
    // Additional info from PDF header that can be displayed if desired:
    // youTubeChannel: "Some URL", // Replace with actual if available
    // mlBlog: "Some URL",
    // selfShiksha: "Some URL",
    syllabus: [
        {
            // week: 1, // Internal reference
            topic: "Data Science & Machine Learning Overview",
            youTubeLinks: [
                { title: "Overview Video 1", url: "https://youtu.be/DwqbxP5BDFo" },
                { title: "Overview Video 2", url: "https://youtu.be/UnjyNYco7uQ" }
            ],
            references: [
                // No specific "Reference" column entries for this topic in PDF
            ],
            codesAndDatasets: [
                { title: "NLTK Code [Jupyter Notebook]", url: null }, // Assuming this is a concept/file, not a direct link
                { title: "Fictometer Paper @ ACL 2019", url: null }, // Assuming this is a paper reference
                { title: "Machine Learning Projects: Detecting Fake News", url: "https://data-flair.training/blogs/advanced-python-project-detecting-fake-news/" },
                { title: "ML Datasets (Curated for College Students)", url: "https://bekushal.medium.com/curated-machine-learning-datasets-for-college-students-ba8cfbc98b6b" },
                { title: "UCI Machine Learning Repository", url: "http://archive.ics.uci.edu/ml/index.php" }
            ]
        },
        {
            // week: 1, (continued)
            topic: "Random Variables and Probability Distributions",
            youTubeLinks: [
                { title: "Random Variables & Probability", url: "https://youtu.be/rGYqfhmdEmo" }
            ],
            references: [
                // No specific "Reference" column entries for this topic in PDF
            ],
            codesAndDatasets: [] // No specific "Codes and Datasets" for this sub-topic in PDF
        },
        {
            // week: 1, (continued)
            topic: "Expectation, Moments and CLT",
            youTubeLinks: [
                { title: "Expectation, Moments, CLT", url: "https://youtu.be/3-A2siEN8w8" }
            ],
            references: [
                { title: "YouTube: Expectation, Moments, CLT", url: "https://www.youtube.com/watch?v=JNm3M9cqWyc" },
                { title: "Krokhmal Paper (UChicago)", url: "http://www.math.uchicago.edu/~may/VIGRE/VIGRE2011/REUPapers/Krokhmal.pdf" }
            ],
            codesAndDatasets: []
        },
        {
            // week: 2,
            topic: "Bayes' Theorem",
            youTubeLinks: [
                { title: "Bayes' Theorem Explained", url: "https://youtu.be/q0p6VWj8N41" }
            ],
            references: [
                { title: "Conditional probability (MathIsFun)", url: "https://www.mathsisfun.com/data/probability-events-conditional.html" },
                { title: "Bayes' Theorem Practice Problems", url: "https://www.statisticshowto.com/bayes-theorem-problems/" }
            ],
            codesAndDatasets: []
        },
        {
            // week: 2, (continued)
            topic: "Naïve Bayes, Gaussian Naive Bayes, Bayes' Optimal Classifier",
            youTubeLinks: [
                { title: "Naive Bayes Introduction", url: "https://youtu.be/DV3F7AZOAE0" }
            ],
            references: [
                { title: "Naive Bayes (YouTube)", url: "https://www.youtube.com/watch?v=O2L2Uv9pdDA" },
                { title: "Gaussian Naive Bayes (YouTube)", url: "https://www.youtube.com/watch?v=H3EjCKtlVog" },
                { title: "Bayesian Networks Introduction", url: "https://towardsdatascience.com/introduction-to-bayesian-networks-81031eeed94e" }
            ],
            codesAndDatasets: [
                { title: "Spam filter using Naive Bayes (KDnuggets)", url: "https://www.kdnuggets.com/2020/07/spam-filter-python-naive-bayes-scratch.html" },
                { title: "Naive Bayes Classifier from Scratch (ML Mastery)", url: "https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/" },
                { title: "Sentiment Analysis of Tweets using Multinomial Naive Bayes", url: "https://towardsdatascience.com/sentiment-analysis-of-tweets-using-multinomial-naive-bayes-1009ed24276b" }
            ]
        },
        {
            // week: 2, (continued)
            topic: "Supervised Learning: Regression vs Classification, Curse of Dimensionality",
            youTubeLinks: [
                { title: "Regression vs Classification", url: "https://youtu.be/NYJZDRRUO84" }
            ],
            references: [
                { title: "Regression vs Classification (Springboard)", url: "https://in.springboard.com/blog/regression-vs-classification-in-machine-learning/" }
            ],
            codesAndDatasets: [
                { title: "K-Nearest Neighbour (KNN) Algorithm (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/neighbors.html" },
                { title: "KNN from scratch (ML Mastery)", url: "https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/" }
            ]
        },
        {
            // week: 3,
            topic: "Bayesian Parameter Estimation",
            youTubeLinks: [
                { title: "Bayesian Parameter Estimation", url: "https://youtu.be/8P7tdwFF0is" }
            ],
            references: [],
            codesAndDatasets: []
        },
        {
            // week: 3, (continued)
            topic: "Maximum Likelihood Estimation",
            youTubeLinks: [
                { title: "Maximum Likelihood Estimation", url: "https://youtu.be/WIPUh9yWM4c" }
            ],
            references: [
                { title: "Deriving ML Cost Functions Part 1", url: "https://allenkunle.me/deriving-ml-cost-functions-part1" },
                { title: "Deriving ML Cost Functions Part 2", url: "https://allenkunle.me/deriving-ml-cost-functions-part2" }
            ],
            codesAndDatasets: []
        },
        {
            // week: 3, (continued)
            topic: "Maximum A Posteriori Estimation",
            youTubeLinks: [
                { title: "Maximum A Posteriori Estimation", url: "https://youtu.be/XKkfIU8ugjM" }
            ],
            references: [
                { title: "MLE vs MAP", url: "https://towardsdatascience.com/mle-vs-map-a989f423ae5c" }
            ],
            codesAndDatasets: []
        },
        {
            // week: 4,
            topic: "Supervised Learning: Gradient Descent & Regularisation",
            youTubeLinks: [
                { title: "Gradient Descent & Regularisation", url: "https://youtu.be/lUmFzIU-Cp4" }
            ],
            references: [
                { title: "Gradient Descent, Learning Rate, Feature Scaling", url: "https://towardsdatascience.com/gradient-descent-the-learning-rate-and-the-importance-of-feature-scaling-6c0b416596e1" },
                { title: "Bias vs Variance (YouTube)", url: "https://www.youtube.com/watch?v=EuBBz3bl-aA" },
                { title: "Convex function (Wikipedia)", url: "https://en.wikipedia.org/wiki/Convex_function" },
                { title: "Visualization of Gradient Descent and SGD (YouTube)", url: "https://www.youtube.com/watch?v=k3AiUhwHQ28" },
                { title: "Visualization of GD/SGD (FA Bianp)", url: "https://fa.bianp.net/teaching/2018/COMP-652/index.html" }
            ],
            codesAndDatasets: [
                { title: "Handling Class Imbalance", url: "https://medium.com/data-science-in-your-pocket/handling-class-imbalance-in-classification-algorithms-explained-2b0b7377aa34" }
            ]
        },
        {
            // week: 4, (continued)
            topic: "Linear Regression: Normal Equation & Regularisation",
            youTubeLinks: [
                { title: "Linear Regression Part 1", url: "https://youtu.be/BGiAcoU4yWk" },
                { title: "Linear Regression Part 2", url: "https://www.youtube.com/watch?v=VqKq78PVO9g" }
            ],
            references: [
                { title: "Linear Regression for ML (ML Mastery)", url: "https://machinelearningmastery.com/linear-regression-for-machine-learning/" },
                { title: "Normal Equation and Matrix Calculation", url: "https://eli.thegreenplace.net/2015/the-normal-equation-and-matrix-calculus/" },
                { title: "Overfitting vs Underfitting", url: "https://towardsdatascience.com/overfitting-vs-underfitting-a-complete-example-d05dd7e19765" },
                { title: "Plot Underfitting vs Overfitting (Scikit-learn)", url: "https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html" },
                { title: "Soft Thresholding (StackExchange)", url: "https://stats.stackexchange.com/questions/123672/coordinate-descent-soft-thresholding-update-operator-for-lasso" },
                { title: "Coordinate Descent (CMU)", url: "https://www.cs.cmu.edu/~ggordon/10725-F12/slides/25-coord-desc.pdf" }
            ],
            codesAndDatasets: [
                { title: "Linear Regression using Python (TowardsDataScience)", url: "https://towardsdatascience.com/linear-regression-using-python-b136c91bf0a2" },
                { title: "Multiple Linear Regression with Python (StackAbuse)", url: "https://stackabuse.com/multiple-linear-regression-with-python/" },
                { title: "Regularization with Scikit-learn", url: "https://scikit-learn.org/stable/modules/linear_model.html" },
                { title: "Guide for Linear, Ridge and Lasso Regression (AnalyticsVidhya)", url: "https://www.analyticsvidhya.com/blog/2017/06/a-comprehensive-guide-for-linear-ridge-and-lasso-regression/" },
                { title: "Ridge Regularization (Scikit-learn MOOC)", url: "https://inria.github.io/scikit-learn-mooc/python_scripts/linear_models_regularization.html" }
            ]
        },
        {
            // week: 5,
            topic: "Logistic Regression: Loss Function, Convexity, Gradient Descent",
            youTubeLinks: [
                { title: "Logistic Regression Intro", url: "https://youtu.be/sxaYUg6zc7I" }
            ],
            references: [
                { title: "Applications of Logistic Regression", url: "https://activewizards.com/blog/5-real-world-examples-of-logistic-regression-application" },
                { title: "Why not MSE for Logistic Regression?", url: "https://towardsdatascience.com/why-not-mse-as-a-loss-function-for-logistic-regression-589816b5e03c" },
                { title: "Decision boundaries (YouTube)", url: "https://www.youtube.com/watch?v=F_VG4LNjZZw" }
            ],
            codesAndDatasets: [
                { title: "Logistic Regression in Python using Scikit-learn (Heartbeat Fritz)", url: "https://heartbeat.fritz.ai/logistic-regression-in-python-using-scikit-learn-d34e882eebb1" },
                { title: "Logistic Regression: Detailed Overview (TowardsDataScience)", url: "https://towardsdatascience.com/logistic-regression-detailed-overview-46c4da4303bc" },
                { title: "Logistic Regression (CMU Stat)", url: "https://www.stat.cmu.edu/~cshalizi/uADA/12/lectures/ch12.pdf" }
            ]
        },
        {
            // week: 5, (continued)
            topic: "Logistic Regression: Multiclass Classification",
            youTubeLinks: [
                { title: "Multiclass Logistic Regression", url: "https://youtu.be/E6MNiNsESI4" }
            ],
            references: [
                { title: "Stanford SLP3 Ch5 (Classification)", url: "https://web.stanford.edu/~jurafsky/slp3/5.pdf" },
                { title: "Classification Metrics (Precision, Recall, F1 - YouTube)", url: "https://www.youtube.com/watch?v=2osIZ-dSPGE" },
                { title: "AUC-ROC (YouTube)", url: "https://www.youtube.com/watch?v=4jRBRDbJemM" },
                { title: "Naive Bayes vs. Logistic Regression (CMU)", url: "http://www.cs.cmu.edu/~tom/mlbook/NBayesLogReg.pdf" }
            ],
            codesAndDatasets: [
                { title: "Logistic Regression (Handwritten Digit Recognition - RealPython)", url: "https://realpython.com/logistic-regression-python/#logistic-regression-in-python-handwriting-recognition" },
                { title: "Logistic Regression (University admission - TowardsDataScience)", url: "https://towardsdatascience.com/building-a-logistic-regression-in-python-301d27367c24" },
                { title: "Logistic Regression (Consumer Purchase - GeeksForGeeks)", url: "https://www.geeksforgeeks.org/ml-logistic-regression-using-python/" },
                { title: "One-Hot Encoding for Logistic Regression (AnalyticsVidhya)", url: "https://www.analyticsvidhya.com/blog/2020/03/one-hot-encoding-vs-label-encoding-using-scikit-learn/" },
                { title: "Multiclass Classification Algorithm from Scratch (TowardsDataScience)", url: "https://towardsdatascience.com/multiclass-classification-algorithm-from-scratch-with-a-project-in-python-step-by-step-guide-485a83c79992" },
                { title: "Logistic Regression MNIST (TowardsDataScience)", url: "https://towardsdatascience.com/logistic-regression-using-python-sklearn-numpy-mnist-handwriting-recognition-matplotlib-a6b31e2b166a" },
                { title: "One-vs-Rest and One-vs-One (ML Mastery)", url: "https://machinelearningmastery.com/one-vs-rest-and-one-vs-one-for-multi-class-classification/" }
            ]
        },
        {
            // week: 6,
            topic: "Support Vector Machines with Linear Kernel",
            youTubeLinks: [
                { title: "SVM with Linear Kernel", url: "https://youtu.be/Kvldyz0KdCU" }
            ],
            references: [
                { title: "SVM Applications (Medium)", url: "https://medium.com/@rinu.gour123/8-unique-real-life-applications-of-svm-8a96ca43313" },
                { title: "SVM vs. Logistic Regression (Medium)", url: "https://medium.com/axum-labs/logistic-regression-vs-support-vector-machines-svm-c335610a3d16" },
                { title: "SVM vs. Linear Discriminant Analysis (StackExchange)", url: "https://stats.stackexchange.com/questions/243932/what-is-the-difference-between-svm-and-lda" },
                { title: "SVM YouTube Explainer", url: "https://www.youtube.com/watch?v=_PwhiWxHK8o" }, // Corrected space in URL
                { title: "Understanding SVM Part 1: Lagrange Multipliers", url: "https://towardsdatascience.com/understanding-support-vector-machine-part-1-lagrange-multipliers-5c24a52ffc5e" },
                { title: "Hinge Loss Formulation of SVM (YouTube)", url: "https://www.youtube.com/watch?v=9dPjKuTYkx4" },
                { title: "Lagrange Multiplier Intuition (Medium)", url: "https://medium.com/@andrew.chamberlain/a-simple-explanation-of-why-lagrange-multipliers-works-253e2cdcbf74" },
                { title: "Lagrange Multiplier Practice Problems", url: "https://tutorial.math.lamar.edu/problems/calciii/lagrangemultipliers.aspx" }
            ],
            codesAndDatasets: [
                { title: "SVM (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/svm.html" },
                { title: "One-vs-Rest and One-vs-One for SVM (ML Mastery)", url: "https://machinelearningmastery.com/one-vs-rest-and-one-vs-one-for-multi-class-classification/" }, // Repeated link
                { title: "Classifying Data using SVMs in Python (GeeksForGeeks)", url: "https://www.geeksforgeeks.org/classifying-data-using-support-vector-machinessvms-in-python/" }
            ]
        },
        {
            // week: 6, (continued)
            topic: "Support Vector Machines: Slack Variables and Nonlinear Kernels",
            youTubeLinks: [
                { title: "SVM Slack & Nonlinear Kernels", url: "https://youtu.be/kPuHAK4RCfM" }
            ],
            references: [
                { title: "Intuitive understanding of RBF Kernel for SVM (Stanford)", url: "http://openclassroom.stanford.edu/MainFolder/DocumentPage.php?course=MachineLearning&doc=exercises/ex8/ex8.html" } // URL seems to point to an exercise page
            ],
            codesAndDatasets: []
        },
        {
            // week: 7,
            topic: "Decision Trees",
            youTubeLinks: [
                { title: "Decision Trees Intro", url: "https://youtu.be/OlreMWwTJ_8" }
            ],
            references: [
                { title: "Decision Tree Algorithm (Gini Index - YouTube)", url: "https://www.youtube.com/watch?v=7VeUPuFGJHk" },
                { title: "Pruning of Decision Trees (CMU)", url: "https://www.cs.cmu.edu/~bhiksha/courses/10-601/decisiontrees/" },
                { title: "Decision Tree for Regression (YouTube)", url: "https://www.youtube.com/watch?v=g9c66TUyIZ4" },
                { title: "Understanding Decision Trees for Classification (Python)", url: "https://towardsdatascience.com/understanding-decision-trees-for-classification-python-9663d683c952" }
            ],
            codesAndDatasets: [
                { title: "Decision Tree Implementation (Python - GeeksForGeeks)", url: "https://www.geeksforgeeks.org/decision-tree-implementation-python/" },
                { title: "Decision Trees (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/tree.html" },
                { title: "Decision Tree Classification Python (DataCamp)", url: "https://www.datacamp.com/community/tutorials/decision-tree-classification-python" }
            ]
        },
        {
            // week: 7, (continued)
            topic: "Random Forest + Comparison of Trees, SVM & LogisticRegression",
            youTubeLinks: [
                { title: "Random Forest & Comparisons", url: "https://youtu.be/pEFBH_371sU" }
            ],
            references: [
                { title: "Bagging and Boosting (YouTube 1)", url: "https://www.youtube.com/watch?v=4EOCQJgqAOY" },
                { title: "Bagging and Boosting (YouTube 2)", url: "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ" },
                { title: "Comparison of various ML algorithms", url: "https://towardsdatascience.com/comparative-study-on-classic-machine-learning-algorithms-24f9ff6ab222" }
            ],
            codesAndDatasets: [
                { title: "Random Forest in Python (TowardsDataScience)", url: "https://towardsdatascience.com/an-implementation-and-explanation-of-the-random-forest-in-python-77bf308a9b76" },
                { title: "Random Forest from Scratch (ML Mastery)", url: "https://machinelearningmastery.com/implement-random-forest-scratch-python/" }
            ]
        },
        {
            // week: 8,
            topic: "Artificial Neural Networks: Introduction",
            youTubeLinks: [
                { title: "ANN Introduction", url: "https://youtu.be/6nkylSKqaAc" } // Repeated link from DL course
            ],
            references: [
                { title: "Universal Approximation Theorem", url: "http://neuralnetworksanddeeplearning.com/chap4.html" },
                { title: "How many layers are needed in ANN?", url: "https://towardsdatascience.com/beginners-ask-how-many-hidden-layers-neurons-to-use-in-artificial-neural-networks-51466afa0d3e" },
                { title: "Difference between Brain and ANN", url: "https://towardsdatascience.com/the-differences-between-artificial-and-biological-neural-networks-a8b46db828b7" },
                { title: "Are ANNs like Human Brain? (Digital Catapult)", url: "https://medium.com/digital-catapult/are-artificial-neural-networks-like-the-human-brain-and-does-it-matter-3add0f029273" },
                { title: "Perceptron Learning Algorithm", url: "https://towardsdatascience.com/perceptron-learning-algorithm-d5db0deab975" },
                { title: "Weight initialisation in ANN (GeeksForGeeks)", url: "https://www.geeksforgeeks.org/weight-initialization-techniques-for-deep-neural-networks/" },
                { title: "Improving DeepNeural Networks-Initialization", url: "https://datascience-enthusiast.com/DL/Improving-DeepNeural-Networks-Initialization.html" },
                { title: "Regularization for ANN (TowardsDataScience)", url: "https://towardsdatascience.com/how-to-improve-a-neural-network-with-regularization-8a18ecda9fe3" }, // This is more a DL topic, but listed under ANN intro here
                { title: "Dropout (TowardsDataScience)", url: "https://towardsdatascience.com/dropout-in-neural-networks-47a162d621d9" },
                { title: "Dropout Video (YouTube)", url: "https://www.youtube.com/watch?v=qfsacble9Al" },
                { title: "Embedding layer vs Dense layer", url: "https://medium.com/logivan/neural-network-embedding-and-dense-layers-whats-the-difference-fa177c6d0304" }
            ],
            codesAndDatasets: [
                { title: "House Price Prediction using ANN (Medium)", url: "https://medium.com/@robertjohn_15390/simple-housing-price-prediction-using-neural-networks-with-tensorflow-8b486d3db3ca" },
                { title: "Image recognition using ANN (NextJournal)", url: "https://nextjournal.com/gkoehler/digit-recognition-with-keras" },
                { title: "Multi-Class classification (Keras Deep Learning)", url: "https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/" },
                { title: "Dropout Regularization in Keras", url: "https://machinelearningmastery.com/how-to-reduce-overfitting-with-dropout-regularization-in-keras/" }
            ]
        },
        {
            // week: 8, (continued)
            topic: "Artificial Neural Networks: Backpropagation",
            youTubeLinks: [
                { title: "ANN Backpropagation", url: "https://youtu.be/ntnwjWEpnkk" } // Repeated link from DL course
            ],
            references: [
                { title: "Neural Networks and Deep Learning Ch2", url: "http://neuralnetworksanddeeplearning.com/chap2.html" },
                { title: "Visual Intuitive Understanding of Backprop (3Blue1Brown)", url: "https://www.youtube.com/watch?v=IHZwWFHWa-w&ab_channel=3Blue1Brown" },
                { title: "Stochastic Gradient Descent (Paperspace)", url: "https://blog.paperspace.com/intro-to-optimization-in-deep-learning-gradient-descent/" },
                { title: "SGD Video (YouTube)", url: "https://www.youtube.com/watch?v=k3AiUhwHQ28" },
                { title: "Stochastic vs Batch Gradient Descent", url: "https://medium.com/@divakar_239/stochastic-vs-batch-gradient-descent-8820568eada1" },
                { title: "Weight initialisation (DeepLearning.ai)", url: "https://www.deeplearning.ai/ai-notes/initialization/" }
            ],
            codesAndDatasets: [
                { title: "Backpropagation Algorithm from Scratch (ML Mastery)", url: "https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/" }
            ]
        },
        {
            // week: 9,
            topic: "Artificial Neural Networks: Activation Functions, Loss functions & Optimization Algorithms",
            youTubeLinks: [
                { title: "ANN Activation, Loss, Optimization", url: "https://youtu.be/qctUEQn9Hj8" } // Repeated link from DL course
            ],
            references: [
                { title: "Activation functions Comparison", url: "https://towardsdatascience.com/comparison-of-activation-functions-for-deep-neural-networks-706ac4284c8a" },
                { title: "Optimization Algorithms (arXiv)", url: "https://arxiv.org/pdf/1609.04747" },
                { title: "Loss Functions Understanding", url: "https://towardsdatascience.com/understanding-different-loss-functions-for-neural-networks-dd1ed0274718" },
                { title: "Vanishing Gradient Problem", url: "https://towardsdatascience.com/the-vanishing-gradient-problem-69bf08b15484" },
                { title: "SVM vs ANN analysis and datasets (Archive)", url: "https://web.archive.org/web/20120304030602/http://indiji.com/svm-vs-nn.html" }
            ],
            codesAndDatasets: []
        },
        {
            // week: 9, (continued)
            topic: "Solving ODEs using ANN",
            youTubeLinks: [
                { title: "ANN for ODEs", url: "https://youtu.be/-pMLqoMarEk" }
            ],
            references: [
                { title: "Sciencedirect Article on ANN for ODEs", url: "https://www.sciencedirect.com/science/article/pii/S0021999118307125" }
            ],
            codesAndDatasets: [
                 { title: "How to solve an ODE with a Neural Network", url: "https://towardsdatascience.com/how-to-solve-an-ode-with-a-neural-network-917d11918932" }
            ]
        },
        {
            // week: 9, (continued)
            topic: "Deep Learning (Introduction)", // Assuming this is a bridge or intro for those not taking full DL
            youTubeLinks: [
                { title: "Deep Learning Intro Video", url: "https://youtu.be/MTbBOu4M7_M" } // Repeated link from DL course
            ],
            references: [
                { title: "MNIST Dataset Analysis (Yann LeCun)", url: "http://yann.lecun.com/exdb/mnist/" }
            ],
            codesAndDatasets: []
        },
        {
            // week: 10,
            topic: "Generative Vs. Discriminative Models",
            youTubeLinks: [
                { title: "Generative vs Discriminative", url: "https://youtu.be/WSxUOIGuGi8" }
            ],
            references: [],
            codesAndDatasets: [
                { title: "GAN for MNIST (ML Mastery)", url: "https://machinelearningmastery.com/how-to-develop-a-generative-adversarial-network-for-an-mnist-handwritten-digits-from-scratch-in-keras/" }
            ]
        },
        {
            // week: 10, (continued)
            topic: "Probabilistic Graphical Models: Bayesian Network and Markov Network",
            youTubeLinks: [
                { title: "PGM Intro Video 1", url: "https://youtu.be/xJtyVQMV1A8" },
                { title: "PGM Intro Video 2 (Expectation Maximization related)", url: "https://youtu.be/PNrghbfK5r0" } // This link is under ExpMax in PDF, but placed here for PGM section
            ],
            references: [
                { title: "Bayesian Network Introduction (UBC)", url: "https://www.cs.ubc.ca/~murphyk/Bayes/bnintro.html" }
            ],
            codesAndDatasets: [
                { title: "YouTube PGM Example", url: "https://www.youtube.com/watch?v=SkC8S3wulfg" }
            ]
        },
        {
            // week: 10, (continued)
            topic: "Expectation Maximization",
            youTubeLinks: [
                 // youtu.be/PNrghbfK5r0 is listed under PGM topic in this JS structure now
            ],
            references: [
                { title: "Expectation Maximization (Nature)", url: "https://www.nature.com/articles/nbt1406" }
            ],
            codesAndDatasets: [
                { title: "EM Algorithm (Duke)", url: "https://people.duke.edu/~ccc14/sta-663/EMAlgorithm.html" }
            ]
        },
        {
            // week: 11,
            topic: "K-Means clustering",
            youTubeLinks: [
                { title: "K-Means Clustering", url: "https://youtu.be/92-h3_1Yfz8" }
            ],
            references: [
                { title: "K-Means vs KNN", url: "https://becominghuman.ai/comprehending-k-means-and-knn-algorithms-c791be90883d" },
                { title: "K-Means Explanation and code (AnalyticsVidhya)", url: "https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-k-means-clustering/" },
                { title: "Visualising K-Means", url: "https://www.naftaliharris.com/blog/visualizing-k-means-clustering/" },
                { title: "How to choose optimal K value", url: "https://towardsdatascience.com/are-you-solving-ml-clustering-problems-using-k-means-68fb4efa5469" }
            ],
            codesAndDatasets: [
                { title: "K-Means Example in Python (TowardsDataScience)", url: "https://towardsdatascience.com/machine-learning-algorithms-part-9-k-means-example-in-python-f2ad05ed5203" },
                { title: "KMeans (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html" },
                { title: "Image compression using K-Means", url: "https://towardsdatascience.com/image-compression-using-k-means-clustering-aa0c91bb0eeb" },
                { title: "MNIST image classification using K-Means", url: "https://medium.com/@joel_34096/k-means-clustering-for-image-classification-a648f28bdc47" }
            ]
        },
        {
            // week: 11, (continued)
            topic: "Gaussian Mixture Models",
            youTubeLinks: [
                { title: "Gaussian Mixture Models", url: "https://youtu.be/he4ll0w1G-g" }
            ],
            references: [
                { title: "Gaussian Mixture Model (Brilliant.org)", url: "https://brilliant.org/wiki/gaussian-mixture-model/" },
                { title: "Gaussian Mixture Models (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/mixture.html" }
            ],
            codesAndDatasets: [
                { title: "Gaussian Mixture Models Clustering (AnalyticsVidhya)", url: "https://www.analyticsvidhya.com/blog/2019/10/gaussian-mixture-models-clustering/" }
            ]
        },
        {
            // week: 12,
            topic: "Principal Component Analysis (PCA) - I",
            youTubeLinks: [
                { title: "PCA Part 1", url: "https://youtu.be/cERNIfg9TLM" }
            ],
            references: [
                { title: "Step-by-Step Explanation of PCA (BuiltIn)", url: "https://builtin.com/data-science/step-step-explanation-principal-component-analysis" },
                { title: "One-Stop Shop for PCA (TowardsDataScience)", url: "https://towardsdatascience.com/a-one-stop-shop-for-principal-component-analysis-5582fb7e0a9c" }
            ],
            codesAndDatasets: [
                 { title: "PCA (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html" } // Corrected URL from OCR
            ]
        },
        {
            // week: 12, (continued)
            topic: "Principal Component Analysis (PCA) - II",
            youTubeLinks: [
                { title: "PCA Part 2", url: "https://youtu.be/ml1d1zC0jsg" }
            ],
            references: [
                { title: "PCA vs Linear Regression", url: "https://shankarmsy.github.io/posts/pca-vs-lr.html" },
                { title: "Kernel PCA", url: "http://fourier.eng.hmc.edu/e161/lectures/kernelPCA/node4.html" }
            ],
            codesAndDatasets: [
                { title: "PCA Practical Guide (AnalyticsVidhya)", url: "https://www.analyticsvidhya.com/blog/2016/03/pca-practical-guide-principal-component-analysis-python/" },
                { title: "PCA Sklearn (ShankarMsy)", url: "https://shankarmsy.github.io/posts/pca-sklearn.html" }
            ]
        },
        {
            // week: 13,
            topic: "Reinforcement Learning",
            youTubeLinks: [
                { title: "Reinforcement Learning Intro", url: "https://youtu.be/KEQhaBIZ9yk" },
                { title: "RL by Alexander Amini (YouTube)", url: "https://www.youtube.com/watch?v=nZfaHlxDD5w&ab_channel=AlexanderAmini" },
                { title: "RL Playlist 1 (YouTube)", url: "https://www.youtube.com/watch?v=zdIQkjtFX_I&list=PLKnIA16_RmvbMK0_fdp0DZHZKm4Q1sIAB" },
                { title: "RL Playlist 2 (YouTube)", url: "https://www.youtube.com/watch?v=WO3kmx4CVgg&list=PLycckD1ec_yNMjDI-Lq4-1ZqHcXqgm7" },
                { title: "RL Playlist 3 (YouTube)", url: "https://www.youtube.com/watch?v=yMk_XtIEzH8&list=PLQVvvaa0QuDezJFIOU5wDdfy4e9vdnx-7" },
                { title: "RL - L8ypSXwyBds (YouTube)", url: "https://www.youtube.com/watch?v=L8ypSXwyBds" },
                { title: "RL - ovlykchkW5I (YouTube)", url: "https://www.youtube.com/watch?v=ovlykchkW5I&t=1s" },
                { title: "RL - 2eeYqJ0uBKE (YouTube)", url: "https://www.youtube.com/watch?v=2eeYqJ0uBKE" }
            ],
            references: [],
            codesAndDatasets: [
                { title: "RL Index (Amunategui)", url: "https://amunategui.github.io/reinforcement-learning/index.html" },
                { title: "RL TicTacToe Implementation (TowardsDataScience)", url: "https://towardsdatascience.com/reinforcement-learning-implement-tictactoe-189582bea542" }, // Repeated
                { title: "Snake AI PyTorch (GitHub)", url: "https://github.com/patrickloeber/snake-ai-pytorch" },
                { title: "TicTacToe MTCS (GitHub)", url: "https://github.com/maksimKorzh/tictactoe-mtcs/blob/master/src/tutorials/board_class_definition/tictactoe.py" },
                { title: "Rock Paper Scissors Q-Learning (Kaggle)", url: "https://www.kaggle.com/code/nelver/rock-paper-scissors-q-learning" },
                { title: "RL Step-by-Step (Medium Vernacular AI)", url: "https://medium.com/vernacular-ai/reinforcement-learning-step-by-step-17cde7dbc56c" }
            ]
        },
        {
            // No week number in PDF for these last general topics
            topic: "Big data technologies & Information management in Big Data",
            youTubeLinks: [
                { title: "Big Data & Info Management", url: "https://youtu.be/5dSmXcKsEBo" }
            ],
            references: [
                { title: "Top Big Data Technologies (Edureka)", url: "https://www.edureka.co/blog/top-big-data-technologies/" },
                { title: "MapReduce Algorithm (Amherst)", url: "https://www.cs.amherst.edu/~ccmcgeoch/cs34/papers/p107-dean.pdf" },
                { title: "NPTEL course from IIT KGP (Big Data)", url: "https://nptel.ac.in/courses/106/105/106105186/" },
                { title: "Comparison: Hadoop vs Spark (Educba)", url: "https://www.educba.com/hadoop-vs-spark/" },
                { title: "Comparison: Hadoop vs Spark (PhoenixNAP)", url: "https://phoenixnap.com/kb/hadoop-vs-spark" },
                { title: "Comparison: Kafka vs Spark (Educba)", url: "https://www.educba.com/kafka-vs-spark/" },
                { title: "Comparison: Apache Kafka vs Flume (Educba)", url: "https://www.educba.com/apache-kafka-vs-flume/" }
            ],
            codesAndDatasets: []
        },
        {
            topic: "Emerging Issues in Data Science",
            youTubeLinks: [],
            references: [
                { title: "Emerging Problems in Data Science and ML", url: "https://towardsdatascience.com/emerging-problems-in-data-science-and-machine-learning-36d37f6531a8" },
                { title: "Explainable AI (Wikipedia)", url: "https://en.wikipedia.org/wiki/Explainable_artificial_intelligence" },
                { title: "AGI (Wikipedia)", url: "https://en.wikipedia.org/wiki/Artificial_general_intelligence" },
                { title: "Few Shot Learning (Medium)", url: "https://medium.com/quick-code/understanding-few-shot-learning-in-machine-learning-bede251a0f67" },
                { title: "Micro Services (Wikipedia)", url: "https://en.wikipedia.org/wiki/Microservices" },
                { title: "Functional Programming (Wikipedia)", url: "https://en.wikipedia.org/wiki/Functional_programming" }
            ],
            codesAndDatasets: []
        }
    ],
    // Textbooks are not explicitly listed in this ML PDF, but you can add them if you have a standard list.
    textbooks: [
        // { title: "Pattern Recognition and Machine Learning", url: "link_to_book" },
        // { title: "The Elements of Statistical Learning", url: "link_to_book" }
    ]
    // referencesForNLP/DeepLearning were specific to the DL syllabus, not this ML one.
};

// Helper function to extract YouTube Video ID (same as before)
function getYoutubeVideoId(url) {
    if (!url) return null;
    let videoId = null;
    const youtubeRegex = [
        /(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&#]+)/,
        /(?:https?:\/\/)?youtu\.be\/([^?#]+)/,
        /(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?#]+)/,
        /(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^?#]+)/,
        /(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?.*v=([^&]+)/
    ];
    for (const regex of youtubeRegex) {
        const match = url.match(regex);
        if (match && match[1]) {
            videoId = match[1];
            break;
        }
    }
    if (videoId) {
        const cleanedId = videoId.split('&')[0].split('#')[0];
        if (/^[a-zA-Z0-9\-_]{11}$/.test(cleanedId) || /^[a-zA-Z0-9\-_İусх]{11,}$/.test(cleanedId)) {
             return cleanedId;
        }
    }
    console.warn("Could not extract a valid video ID from URL:", url, "Attempted extraction:", videoId);
    return null;
}
