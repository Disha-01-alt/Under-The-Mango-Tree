// static/js/ml_course_data.js

const mlCourseData = {
    courseTitle: "Data Science & Machine Learning (Full semester course)",
    instructor: "Dr. Kushal Shah",
    generalLinks: [
        { text: "YouTube Channel", url: "#" }, // Replace # with actual channel URL if available
        { text: "ML Blog", url: "#" },         // Replace # with actual blog URL
        { text: "Self Shiksha", url: "#" }     // Replace # with actual Self Shiksha URL
    ],
    prerequisite: "Before starting to learn ML, make sure you have a good hold of Python Programming and Data Handling using Python.",
    topics: [
        // --- Section 1: Foundations ---
        {
            topicName: "Data Science & Machine Learning Overview",
            youtubeLinks: [
                "https://youtu.be/DwqbxP5BDFo",
                "https://youtu.be/UnjyNYco7uQ"
            ],
            references: [],
            codesAndDatasets: [
                { text: "NLTK Code [Jupyter Notebook]", url: "#" }, // Placeholder if direct link not in PDF
                { text: "Fictometer Paper @ ACL 2019", url: "#" }, // Placeholder
                { text: "Machine Learning Projects: Detecting Fake News", url: "https://data-flair.training/blogs/advanced-python-project-detecting-fake-news/" },
                { text: "ML Datasets (Curated by Kushal)", url: "https://bekushal.medium.com/curated-machine-learning-datasets-for-college-students-ba8cfbc98b6b" },
                { text: "UCI Machine Learning Repository", url: "http://archive.ics.uci.edu/ml/index.php" }
            ]
        },
        {
            topicName: "Random Variables and Probability Distributions",
            youtubeLinks: [
                "https://youtu.be/rGYqfhmdEmo"
            ],
            references: [],
            codesAndDatasets: []
        },
        {
            topicName: "Expectation, Moments and CLT",
            youtubeLinks: [
                "https://youtu.be/3-A2siEN8w8"
            ],
            references: [
                { text: "YouTube: Expectation, Variance, Covariance", url: "https://www.youtube.com/watch?v=JNm3M9cqWyc" },
                { text: "UChicago VIGRE Paper (Krokhmal)", url: "http://www.math.uchicago.edu/~may/VIGRE/VIGRE2011/REUPapers/Krokhmal.pdf" }
            ],
            codesAndDatasets: []
        },
        // --- Section 2: Bayesian Learning ---
        {
            topicName: "Bayes' Theorem",
            youtubeLinks: [
                "https://youtu.be/q0p6VWj8N4I" // Corrected ID
            ],
            references: [
                { text: "Conditional probability (MathIsFun)", url: "https://www.mathsisfun.com/data/probability-events-conditional.html" },
                { text: "Practice problems (StatisticsHowTo)", url: "https://www.statisticshowto.com/bayes-theorem-problems/" }
            ],
            codesAndDatasets: []
        },
        {
            topicName: "Naïve Bayes, Gaussian Naive Bayes, Bayes' Optimal Classifier",
            youtubeLinks: [
                "https://youtu.be/DV3F7AZOAE0"
            ],
            references: [
                { text: "Naive Bayes (YouTube)", url: "https://www.youtube.com/watch?v=O2L2Uv9pdDA" },
                { text: "Gaussian Naive Bayes (YouTube)", url: "https://www.youtube.com/watch?v=H3EjCKtlVog" },
                { text: "Bayesian Networks Introduction (Towards Data Science)", url: "https://towardsdatascience.com/introduction-to-bayesian-networks-81031eeed94e" }
            ],
            codesAndDatasets: [
                { text: "Spam filter using Naive Bayes (KDNuggets)", url: "https://www.kdnuggets.com/2020/07/spam-filter-python-naive-bayes-scratch.html" },
                { text: "Naive Bayes Classifier from Scratch (Machine Learning Mastery)", url: "https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/" },
                { text: "Sentiment Analysis of Tweets using Multinomial Naive Bayes (Towards Data Science)", url: "https://towardsdatascience.com/sentiment-analysis-of-tweets-using-multinomial-naive-bayes-1009ed24276b" }
            ]
        },
        // --- Section 3: Supervised Learning Fundamentals ---
        {
            topicName: "Supervised Learning: Regression vs Classification, Curse of Dimensionality",
            youtubeLinks: [
                "https://youtu.be/NYJZDRRUO84"
            ],
            references: [
                { text: "Regression vs Classification (Springboard)", url: "https://in.springboard.com/blog/regression-vs-classification-in-machine-learning/" }
            ],
            codesAndDatasets: [
                { text: "K-Nearest Neighbour (KNN) Algorithm (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/neighbors.html" },
                { text: "KNN from scratch (Machine Learning Mastery)", url: "https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/" }
            ]
        },
        {
            topicName: "Bayesian Parameter Estimation",
            youtubeLinks: [
                "https://youtu.be/8P7tdwFF0is"
            ],
            references: [],
            codesAndDatasets: []
        },
        {
            topicName: "Maximum Likelihood Estimation",
            youtubeLinks: [
                "https://youtu.be/WIPUh9yWM4c"
            ],
            references: [
                { text: "Deriving ML Cost Functions Part 1 (Allen Kunle)", url: "https://allenkunle.me/deriving-ml-cost-functions-part1" },
                { text: "Deriving ML Cost Functions Part 2 (Allen Kunle)", url: "https://allenkunle.me/deriving-ml-cost-functions-part2" }
            ],
            codesAndDatasets: []
        },
        {
            topicName: "Maximum A Posteriori Estimation",
            youtubeLinks: [
                "https://youtu.be/XKkfIU8ugjM"
            ],
            references: [
                { text: "MLE vs MAP (Towards Data Science)", url: "https://towardsdatascience.com/mle-vs-map-a989f423ae5c" }
            ],
            codesAndDatasets: []
        },
        // --- Section 4: Gradient Descent & Regularization ---
        {
            topicName: "Supervised Learning: Gradient Descent & Regularisation",
            youtubeLinks: [
                "https://youtu.be/lUmFzIU-Cp4"
            ],
            references: [
                { text: "Gradient Descent, Learning Rate, Feature Scaling (Towards Data Science)", url: "https://towardsdatascience.com/gradient-descent-the-learning-rate-and-the-importance-of-feature-scaling-6c0b416596e1" },
                { text: "Bias vs Variance (YouTube)", url: "https://www.youtube.com/watch?v=EuBBz3bl-aA" },
                { text: "Convex function (Wikipedia)", url: "https://en.wikipedia.org/wiki/Convex_function" },
                { text: "Visualization of Gradient Descent and SGD (YouTube)", url: "https://www.youtube.com/watch?v=k3AiUhwHQ28" },
                { text: "COMP 652 Lecture Notes (Fa Bianp)", url: "https://fa.bianp.net/teaching/2018/COMP-652/index.html" }
            ],
            codesAndDatasets: [
                { text: "Handling Class Imbalance (Medium)", url: "https://medium.com/data-science-in-your-pocket/handling-class-imbalance-in-classification-algorithms-explained-2b0b7377aa34" }
            ]
        },
        // --- Section 5: Linear Models ---
        {
            topicName: "Linear Regression: Normal Equation & Regularisation",
            youtubeLinks: [
                "https://youtu.be/BGiAcoU4yWk",
                "https://www.youtube.com/watch?v=VqKq78PVO9g"
            ],
            references: [
                { text: "Linear Regression for Machine Learning (Machine Learning Mastery)", url: "https://machinelearningmastery.com/linear-regression-for-machine-learning/" },
                { text: "Normal Equation and Matrix Calculation (Eli Bendersky)", url: "https://eli.thegreenplace.net/2015/the-normal-equation-and-matrix-calculus/" },
                { text: "Overfitting vs Underfitting (Towards Data Science)", url: "https://towardsdatascience.com/overfitting-vs-underfitting-a-complete-example-d05dd7e19765" },
                { text: "Plot Underfitting vs Overfitting (Scikit-learn)", url: "https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html" },
                { text: "Soft Thresholding (Stats StackExchange)", url: "https://stats.stackexchange.com/questions/123672/coordinate-descent-soft-thresholding-update-operator-for-lasso" },
                { text: "Coordinate Descent (CMU Slides)", url: "https://www.cs.cmu.edu/~ggordon/10725-F12/slides/25-coord-desc.pdf" }
            ],
            codesAndDatasets: [
                { text: "Linear Regression using Python (Towards Data Science)", url: "https://towardsdatascience.com/linear-regression-using-python-b136c91bf0a2" },
                { text: "Multiple Linear Regression with Python (StackAbuse)", url: "https://stackabuse.com/multiple-linear-regression-with-python/" },
                { text: "Linear Models with Regularization (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/linear_model.html" },
                { text: "Guide for Linear, Ridge and Lasso Regression (Analytics Vidhya)", url: "https://www.analyticsvidhya.com/blog/2017/06/a-comprehensive-guide-for-linear-ridge-and-lasso-regression/" },
                { text: "Ridge Regularization (Scikit-learn MOOC)", url: "https://inria.github.io/scikit-learn-mooc/python_scripts/linear_models_regularization.html" }
            ]
        },
        {
            topicName: "Logistic Regression: Loss Function, Convexity, Gradient Descent",
            youtubeLinks: [
                "https://youtu.be/sxaYUg6zc7I"
            ],
            references: [
                { text: "Applications of Logistic Regression (ActiveWizards)", url: "https://activewizards.com/blog/5-real-world-examples-of-logistic-regression-application" },
                { text: "Why not MSE for Logistic Regression (Towards Data Science)", url: "https://towardsdatascience.com/why-not-mse-as-a-loss-function-for-logistic-regression-589816b5e03c" },
                { text: "Decision boundaries (YouTube)", url: "https://www.youtube.com/watch?v=F_VG4LNjZZw" },
                { text: "Stanford NLP Book Ch5 (Jurafsky & Martin)", url: "https://web.stanford.edu/~jurafsky/slp3/5.pdf" },
                { text: "Classification Metrics (Precision, Recall, F1) (YouTube)", url: "https://www.youtube.com/watch?v=2osIZ-dSPGE" },
                { text: "AUC-ROC (YouTube)", url: "https://www.youtube.com/watch?v=4jRBRDbJemM" }
            ],
            codesAndDatasets: [
                { text: "Logistic Regression in Python (Heartbeat Fritz.ai)", url: "https://heartbeat.fritz.ai/logistic-regression-in-python-using-scikit-learn-d34e882eebb1" },
                { text: "Logistic Regression Detailed Overview (Towards Data Science)", url: "https://towardsdatascience.com/logistic-regression-detailed-overview-46c4da4303bc" },
                { text: "CMU Stat Lecture on Logistic Regression (Shalizi)", url: "https://www.stat.cmu.edu/~cshalizi/uADA/12/lectures/ch12.pdf" },
                { text: "Logistic Regression (Handwritten Digit Recog.) (Real Python)", url: "https://realpython.com/logistic-regression-python/#logistic-regression-in-python-handwriting-recognition" },
                { text: "Logistic Regression (University admission) (Towards Data Science)", url: "https://towardsdatascience.com/building-a-logistic-regression-in-python-301d27367c24" },
                { text: "Logistic Regression (Consumer Purchase) (GeeksForGeeks)", url: "https://www.geeksforgeeks.org/ml-logistic-regression-using-python/" },
                { text: "One-Hot Encoding for Logistic Regression (Analytics Vidhya)", url: "https://www.analyticsvidhya.com/blog/2020/03/one-hot-encoding-vs-label-encoding-using-scikit-learn/" }

            ]
        },
        {
            topicName: "Logistic Regression: Multiclass Classification",
            youtubeLinks: [
                "https://youtu.be/E6MNiNsESI4"
            ],
            references: [
                { text: "Naive Bayes vs. Logistic Regression (CMU Tom Mitchell)", url: "http://www.cs.cmu.edu/~tom/mlbook/NBayesLogReg.pdf" }
            ],
            codesAndDatasets: [
                { text: "Multiclass Classification Algorithm from Scratch (Towards Data Science)", url: "https://towardsdatascience.com/multiclass-classification-algorithm-from-scratch-with-a-project-in-python-step-by-step-guide-485a83c79992" },
                { text: "Logistic Regression using Python (MNIST) (Towards Data Science)", url: "https://towardsdatascience.com/logistic-regression-using-python-sklearn-numpy-mnist-handwriting-recognition-matplotlib-a6b31e2b166a" },
                { text: "One-vs-Rest and One-vs-One for Multi-class Classification (ML Mastery)", url: "https://machinelearningmastery.com/one-vs-rest-and-one-vs-one-for-multi-class-classification/" }
            ]
        },
        // --- Section 6: Support Vector Machines ---
        {
            topicName: "Support Vector Machines with Linear Kernel",
            youtubeLinks: [
                "https://youtu.be/Kvldyz0KdCU"
            ],
            references: [
                { text: "SVM Applications (Medium)", url: "https://medium.com/@rinu.gour123/8-unique-real-life-applications-of-svm-8a96ca43313" },
                { text: "SVM vs. Logistic Regression (Medium)", url: "https://medium.com/axum-labs/logistic-regression-vs-support-vector-machines-svm-c335610a3d16" },
                { text: "SVM vs. Linear Discriminant Analysis (Stats StackExchange)", url: "https://stats.stackexchange.com/questions/243932/what-is-the-difference-between-svm-and-lda" },
                { text: "SVM Intuition (YouTube)", url: "https://www.youtube.com/watch?v=_PwhiWxHK8o" }, // Corrected ID
                { text: "Understanding SVM Part 1: Lagrange Multipliers (Towards Data Science)", url: "https://towardsdatascience.com/understanding-support-vector-machine-part-1-lagrange-multipliers-5c24a52ffc5e" },
                { text: "Hinge Loss Formulation of SVM (YouTube)", url: "https://www.youtube.com/watch?v=9dPjKuTYkx4" },
                { text: "Lagrange Multiplier Intuition (Medium)", url: "https://medium.com/@andrew.chamberlain/a-simple-explanation-of-why-lagrange-multipliers-works-253e2cdcbf74" },
                { text: "Lagrange Multiplier (practice problems) (Lamar Math)", url: "https://tutorial.math.lamar.edu/problems/calciii/lagrangemultipliers.aspx" }
            ],
            codesAndDatasets: [
                { text: "SVM Modules (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/svm.html" },
                { text: "One-vs-Rest and One-vs-One for SVM (ML Mastery)", url: "https://machinelearningmastery.com/one-vs-rest-and-one-vs-one-for-multi-class-classification/" }, // Duplicate, but relevant to SVM too
                { text: "Classifying Data using SVMs in Python (GeeksForGeeks)", url: "https://www.geeksforgeeks.org/classifying-data-using-support-vector-machinessvms-in-python/" }
            ]
        },
        {
            topicName: "Support Vector Machines: Slack Variables and Nonlinear Kernels",
            youtubeLinks: [
                "https://youtu.be/kPuHAK4RCfM"
            ],
            references: [
                { text: "Intuitive understanding of RBF Kernel for SVM (Stanford OpenClassroom)", url: "http://openclassroom.stanford.edu/MainFolder/DocumentPage.php?course=MachineLearning&doc=exercises/ex8/ex8.html" } // URL is for ex8, implies RBF kernel
            ],
            codesAndDatasets: []
        },
        // --- Section 7: Tree-based Models ---
        {
            topicName: "Decision Trees",
            youtubeLinks: [
                "https://youtu.be/OlreMWwTJ_8"
            ],
            references: [
                { text: "Decision Tree Algorithm (Gini Index) (YouTube)", url: "https://www.youtube.com/watch?v=7VeUPuFGJHk" },
                { text: "Pruning of Decision Trees (CMU Bhiksha)", url: "https://www.cs.cmu.edu/~bhiksha/courses/10-601/decisiontrees/" },
                { text: "Decision Tree for Regression (YouTube)", url: "https://www.youtube.com/watch?v=g9c66TUyIZ4" },
                { text: "Understanding Decision Trees for Classification (Towards Data Science)", url: "https://towardsdatascience.com/understanding-decision-trees-for-classification-python-9663d683c952" }
            ],
            codesAndDatasets: [
                { text: "Decision Tree Implementation (GeeksForGeeks)", url: "https://www.geeksforgeeks.org/decision-tree-implementation-python/" },
                { text: "Decision Trees (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/tree.html" },
                { text: "Decision Tree Classification Python (DataCamp)", url: "https://www.datacamp.com/community/tutorials/decision-tree-classification-python" }
            ]
        },
        {
            topicName: "Random Forest + Comparison of Trees, SVM & Logistic Regression",
            youtubeLinks: [
                "https://youtu.be/pEFBH_371sU"
            ],
            references: [
                { text: "Bagging and Boosting (YouTube)", url: "https://www.youtube.com/watch?v=4EOCQJgqAOY" },
                { text: "Ensemble Learning (YouTube)", url: "https://www.youtube.com/watch?v=J4Wdy0Wc_xQ" }, // Assuming this is related to comparison
                { text: "Comparison of various ML algorithms (Towards Data Science)", url: "https://towardsdatascience.com/comparative-study-on-classic-machine-learning-algorithms-24f9ff6ab222" }
            ],
            codesAndDatasets: [
                { text: "Implementation and Explanation of Random Forest (Towards Data Science)", url: "https://towardsdatascience.com/an-implementation-and-explanation-of-the-random-forest-in-python-77bf308a9b76" },
                { text: "Implement Random Forest from Scratch (ML Mastery)", url: "https://machinelearningmastery.com/implement-random-forest-scratch-python/" }
            ]
        },
        // --- Section 8: Artificial Neural Networks ---
        {
            topicName: "Artificial Neural Networks: Introduction",
            youtubeLinks: [
                "https://youtu.be/6nkylSKqaAc"
            ],
            references: [
                { text: "Universal Approximation Theorem (Nielsen)", url: "http://neuralnetworksanddeeplearning.com/chap4.html" },
                { text: "How many hidden layers/neurons? (Towards Data Science)", url: "https://towardsdatascience.com/beginners-ask-how-many-hidden-layers-neurons-to-use-in-artificial-neural-networks-51466afa0d3e" },
                { text: "Difference between Brain and ANN (Towards Data Science)", url: "https://towardsdatascience.com/the-differences-between-artificial-and-biological-neural-networks-a8b46db828b7" },
                { text: "Are ANNs like human brain? (Medium)", url: "https://medium.com/digital-catapult/are-artificial-neural-networks-like-the-human-brain-and-does-it-matter-3add0f029273" },
                { text: "Perceptron Learning Algorithm (Towards Data Science)", url: "https://towardsdatascience.com/perceptron-learning-algorithm-d5db0deab975" },
                { text: "Weight initialisation in ANN (GeeksForGeeks)", url: "https://www.geeksforgeeks.org/weight-initialization-techniques-for-deep-neural-networks/" },
                { text: "Improving Deep Neural Networks: Initialization (Data Science Enthusiast)", url: "https://datascience-enthusiast.com/DL/Improving-DeepNeural-Networks-Initialization.html" },
                { text: "Regularization for ANN (Towards Data Science)", url: "https://towardsdatascience.com/how-to-improve-a-neural-network-with-regularization-8a18ecda9fe3" },
                { text: "Dropout (Towards Data Science)", url: "https://towardsdatascience.com/dropout-in-neural-networks-47a162d621d9" },
                { text: "Dropout (YouTube)", url: "https://www.youtube.com/watch?v=qfsacble9Al" },
                { text: "Embedding layer vs Dense layer (Medium)", url: "https://medium.com/logivan/neural-network-embedding-and-dense-layers-whats-the-difference-fa177c6d0304" }
            ],
            codesAndDatasets: [
                { text: "House Price Prediction using ANN (Medium)", url: "https://medium.com/@robertjohn_15390/simple-housing-price-prediction-using-neural-networks-with-tensorflow-8b486d3db3ca" },
                { text: "Image recognition using ANN (Nextjournal)", url: "https://nextjournal.com/gkoehler/digit-recognition-with-keras" },
                { text: "Multi-Class classification Keras (ML Mastery)", url: "https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/" },
                { text: "Reduce Overfitting with Dropout in Keras (ML Mastery)", url: "https://machinelearningmastery.com/how-to-reduce-overfitting-with-dropout-regularization-in-keras/" }
            ]
        },
        {
            topicName: "Artificial Neural Networks: Backpropagation",
            youtubeLinks: [
                "https://youtu.be/ntnwjWEpnkk"
            ],
            references: [
                { text: "Backpropagation Chapter (Nielsen)", url: "http://neuralnetworksanddeeplearning.com/chap2.html" },
                { text: "Visual Intuitive Understanding of Backprop (3Blue1Brown YouTube)", url: "https://www.youtube.com/watch?v=IHZwWFHWa-w&ab_channel=3Blue1Brown" },
                { text: "Stochastic Gradient Descent (Paperspace Blog)", url: "https://blog.paperspace.com/intro-to-optimization-in-deep-learning-gradient-descent/" },
                { text: "Gradient Descent Visualization (YouTube)", url: "https://www.youtube.com/watch?v=k3AiUhwHQ28" }, // Duplicate, but context relevant
                { text: "Stochastic vs Batch Gradient Descent (Medium)", url: "https://medium.com/@divakar_239/stochastic-vs-batch-gradient-descent-8820568eada1" },
                { text: "Weight initialisation (DeepLearning.ai Notes)", url: "https://www.deeplearning.ai/ai-notes/initialization/" }
            ],
            codesAndDatasets: [
                { text: "Implement Backpropagation from Scratch (ML Mastery)", url: "https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/" }
            ]
        },
        {
            topicName: "Artificial Neural Networks: Activation Functions, Loss functions & Optimization Algorithms",
            youtubeLinks: [
                "https://youtu.be/qctUEQn9Hj8"
            ],
            references: [
                { text: "Activation functions Comparison (Towards Data Science)", url: "https://towardsdatascience.com/comparison-of-activation-functions-for-deep-neural-networks-706ac4284c8a" },
                { text: "Optimization Algorithms (arXiv)", url: "https://arxiv.org/pdf/1609.04747" },
                { text: "Loss Functions (Towards Data Science)", url: "https://towardsdatascience.com/understanding-different-loss-functions-for-neural-networks-dd1ed0274718" },
                { text: "Vanishing Gradient Problem (Towards Data Science)", url: "https://towardsdatascience.com/the-vanishing-gradient-problem-69bf08b15484" }
            ],
            codesAndDatasets: []
        },
        {
            topicName: "Solving ODEs using ANN",
            youtubeLinks: [
                "https://youtu.be/-pMLqoMarEk"
            ],
            references: [
                 { text: "SVM vs ANN analysis and datasets (Archive.org)", url: "https://web.archive.org/web/20120304030602/http://indiji.com/svm-vs-nn.html" },
                 { text: "Solving ODEs with ANN (ScienceDirect)", url: "https://www.sciencedirect.com/science/article/pii/S0021999118307125" }
            ],
            codesAndDatasets: [
                 { text: "How to solve an ODE with a Neural Network (Towards Data Science)", url: "https://towardsdatascience.com/how-to-solve-an-ode-with-a-neural-network-917d11918932" }
            ]
        },
        {
            topicName: "Deep Learning (Intro/Overlap)", // Topic 9 from ML pdf, seems to transition to DL
            youtubeLinks: [
                "https://youtu.be/MTbBOu4M7_M"
            ],
            references: [
                { text: "MNIST Dataset Analysis (Yann LeCun)", url: "http://yann.lecun.com/exdb/mnist/" }
            ],
            codesAndDatasets: [
                { text: "GAN for MNIST (ML Mastery)", url: "https://machinelearningmastery.com/how-to-develop-a-generative-adversarial-network-for-an-mnist-handwritten-digits-from-scratch-in-keras/" } // Moved from Generative models to here as it relates to MNIST
            ]
        },
        // --- Section 9: Advanced Models & Unsupervised Learning ---
        {
            topicName: "Generative Vs. Discriminative Models",
            youtubeLinks: [
                "https://youtu.be/WSxUOIGuGi8"
            ],
            references: [],
            codesAndDatasets: []
        },
        {
            topicName: "Probabilistic Graphical Models: Bayesian Network and Markov Network",
            youtubeLinks: [
                "https://youtu.be/xJtyVQMV1A8",
                "https://youtu.be/PNrghbfK5r0" // Assuming this is for Markov Network
            ],
            references: [
                { text: "Bayesian Network Introduction (UBC CS)", url: "https://www.cs.ubc.ca/~murphyk/Bayes/bnintro.html" }
            ],
            codesAndDatasets: [
                 { text: "Bayesian Networks visualization (YouTube)", url: "https://www.youtube.com/watch?v=SkC8S3wulfg" }
            ]
        },
        {
            topicName: "Expectation Maximization",
            youtubeLinks: [
                // Link for EM was missing in PDF, but seems to be https://youtu.be/PNrghbfK5r0 based on prior item, or a new one is needed.
                // For now, assuming PNrghbfK5r0 was for Markov and EM needs one or is covered by GMM
            ],
            references: [
                { text: "Nature Paper on EM", url: "https://www.nature.com/articles/nbt1406" },
                { text: "EM Algorithm (Duke STA 663)", url: "https://people.duke.edu/~ccc14/sta-663/EMAlgorithm.html" }
            ],
            codesAndDatasets: []
        },
        {
            topicName: "K-Means clustering",
            youtubeLinks: [
                "https://youtu.be/92-h3_1Yfz8" // Corrected ID
            ],
            references: [
                { text: "K-Means vs KNN (BecomingHuman.ai)", url: "https://becominghuman.ai/comprehending-k-means-and-knn-algorithms-c791be90883d" },
                { text: "Explanation and code for K-Means (Analytics Vidhya)", url: "https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-k-means-clustering/" },
                { text: "Visualising K-Means (Naftali Harris Blog)", url: "https://www.naftaliharris.com/blog/visualizing-k-means-clustering/" },
                { text: "How to choose optimal K value (Towards Data Science)", url: "https://towardsdatascience.com/are-you-solving-ml-clustering-problems-using-k-means-68fb4efa5469" }
            ],
            codesAndDatasets: [
                { text: "K-Means Example in Python (Towards Data Science)", url: "https://towardsdatascience.com/machine-learning-algorithms-part-9-k-means-example-in-python-f2ad05ed5203" },
                { text: "KMeans (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html" },
                { text: "Image compression using K-Means (Towards Data Science)", url: "https://towardsdatascience.com/image-compression-using-k-means-clustering-aa0c91bb0eeb" },
                { text: "MNIST image classification using K-Means (Medium)", url: "https://medium.com/@joel_34096/k-means-clustering-for-image-classification-a648f28bdc47" }
            ]
        },
        {
            topicName: "Gaussian Mixture Models",
            youtubeLinks: [
                "https://youtu.be/he4ll0w1G-g"
            ],
            references: [
                { text: "Gaussian Mixture Model (Brilliant.org)", url: "https://brilliant.org/wiki/gaussian-mixture-model/" },
                { text: "Mixture Models (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/mixture.html" }
            ],
            codesAndDatasets: [
                { text: "Gaussian Mixture Models Clustering (Analytics Vidhya)", url: "https://www.analyticsvidhya.com/blog/2019/10/gaussian-mixture-models-clustering/" }
            ]
        },
        {
            topicName: "Principal Component Analysis (PCA) - I",
            youtubeLinks: [
                "https://youtu.be/cERNIfg9TLM"
            ],
            references: [
                { text: "Step-by-Step Explanation of PCA (Built In)", url: "https://builtin.com/data-science/step-step-explanation-principal-component-analysis" },
                { text: "One-Stop Shop for PCA (Towards Data Science)", url: "https://towardsdatascience.com/a-one-stop-shop-for-principal-component-analysis-5582fb7e0a9c" },
                { text: "PCA vs Linear Regression (Shankar MSy)", url: "https://shankarmsy.github.io/posts/pca-vs-lr.html" }
            ],
            codesAndDatasets: [
                { text: "PCA (Scikit-learn)", url: "https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html" },
                { text: "PCA Practical Guide (Analytics Vidhya)", url: "https://www.analyticsvidhya.com/blog/2016/03/pca-practical-guide-principal-component-analysis-python/" },
                { text: "PCA with Scikit-learn (Shankar MSy)", url: "https://shankarmsy.github.io/posts/pca-sklearn.html" }
            ]
        },
        {
            topicName: "Principal Component Analysis (PCA) - II",
            youtubeLinks: [
                "https://youtu.be/ml1d1zC0jsg"
            ],
            references: [
                { text: "Kernel PCA (Harvey Mudd College)", url: "http://fourier.eng.hmc.edu/e161/lectures/kernelPCA/node4.html" }
            ],
            codesAndDatasets: []
        },
        // --- Section 10: Reinforcement Learning & Big Data ---
        {
            topicName: "Reinforcement Learning",
            youtubeLinks: [
                "https://youtu.be/KEQhaBIZ9yk",
                "https://www.youtube.com/watch?v=nZfaHlxDD5w&ab_channel=AlexanderAmini",
                "https://www.youtube.com/watch?v=zdIQkjtFX_I&list=PLKnIA16_RmvbMK0_fdp0DZHZKm4Q1sIAB", // Playlist
                "https://www.youtube.com/watch?v=WO3kmx4CVgg&list=PLycckD1ec_yNMjDI-Lq4-1ZqHcXqgm7", // Playlist
                "https://www.youtube.com/watch?v=yMk_XtIEzH8&list=PLQVvvaa0QuDezJFIOU5wDdfy4e9vdnx-7", // Playlist
                "https://www.youtube.com/watch?v=L8ypSXwyBds",
                "https://www.youtube.com/watch?v=ovlykchkW5I&t=1s",
                "https://www.youtube.com/watch?v=2eeYqJ0uBKE"
            ],
            references: [
                 { text: "RL Step-by-step (Medium)", url: "https://medium.com/vernacular-ai/reinforcement-learning-step-by-step-17cde7dbc56c" }
            ],
            codesAndDatasets: [
                { text: "Reinforcement Learning Index (Amunategui)", url: "https://amunategui.github.io/reinforcement-learning/index.html" },
                { text: "RL TicTacToe Implementation (Towards Data Science)", url: "https://towardsdatascience.com/reinforcement-learning-implement-tictactoe-189582bea542" }, // Repeated
                { text: "Snake AI PyTorch (GitHub)", url: "https://github.com/patrickloeber/snake-ai-pytorch" },
                { text: "TicTacToe MCTS (GitHub)", url: "https://github.com/maksimKorzh/tictactoe-mtcs/blob/master/src/tutorials/board_class_definition/tictactoe.py" },
                { text: "Rock Paper Scissors Q-Learning (Kaggle)", url: "https://www.kaggle.com/code/nelver/rock-paper-scissors-q-learning" }
            ]
        },
        {
            topicName: "Big data technologies & Information management in Big Data",
            youtubeLinks: [
                "https://youtu.be/5dSmXcKsEBo"
            ],
            references: [
                { text: "Top Big Data Technologies (Edureka)", url: "https://www.edureka.co/blog/top-big-data-technologies/" },
                { text: "MapReduce Algorithm (Amherst CS)", url: "https://www.cs.amherst.edu/~ccmcgeoch/cs34/papers/p107-dean.pdf" },
                { text: "NPTEL course from IIT KGP (Big Data)", url: "https://nptel.ac.in/courses/106/105/106105186/" },
                { text: "Hadoop vs Spark (Educba)", url: "https://www.educba.com/hadoop-vs-spark/" },
                { text: "Hadoop vs Spark (PhoenixNAP)", url: "https://phoenixnap.com/kb/hadoop-vs-spark" },
                { text: "Kafka vs Spark (Educba)", url: "https://www.educba.com/kafka-vs-spark/" },
                { text: "Apache Kafka vs Flume (Educba)", url: "https://www.educba.com/apache-kafka-vs-flume/" }
            ],
            codesAndDatasets: []
        },
        // --- Section 11: Emerging Issues ---
        {
            topicName: "Emerging Issues in Data Science",
            youtubeLinks: [
                // No YouTube links listed for this specific sub-topic in PDF
            ],
            references: [
                { text: "Emerging Problems in Data Science (Towards Data Science)", url: "https://towardsdatascience.com/emerging-problems-in-data-science-and-machine-learning-36d37f6531a8" },
                { text: "Explainable AI (Wikipedia)", url: "https://en.wikipedia.org/wiki/Explainable_artificial_intelligence" },
                { text: "AGI (Wikipedia)", url: "https://en.wikipedia.org/wiki/Artificial_general_intelligence" },
                { text: "Few Shot Learning (Medium)", url: "https://medium.com/quick-code/understanding-few-shot-learning-in-machine-learning-bede251a0f67" },
                { text: "Micro Services (Wikipedia)", url: "https://en.wikipedia.org/wiki/Microservices" },
                { text: "Functional Programming (Wikipedia)", url: "https://en.wikipedia.org/wiki/Functional_programming" }
            ],
            codesAndDatasets: []
        }
    ],
    // General references mentioned at the end of ML PDF
    generalMlReferences: [
        { text: "References for Deep Learning", url: "#" }, // Link to your DL page or a specific resource
        { text: "References for NLP", url: "#" }         // Link to your NLP page or a specific resource
    ]
};
