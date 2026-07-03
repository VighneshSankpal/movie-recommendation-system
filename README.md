# Explainable Multi-Model Movie Recommendation System

An intelligent movie recommendation system built using **Machine Learning**, **Deep Learning**, and **Natural Language Processing (NLP)** techniques. The application combines **Content-Based Filtering**, **Collaborative Filtering**, and a **Hybrid Recommendation Engine** to deliver personalized and explainable movie recommendations through an interactive Streamlit web application.

---

## Features

* Content-Based Movie Recommendation
* Collaborative Filtering using SVD Matrix Factorization
* Hybrid Recommendation Engine
* Explainable AI (XAI) for recommendation transparency
* Movie posters and metadata from TMDB API
* Interactive Streamlit Dashboard
* Movie Information Explorer
* Fast recommendation generation using pre-trained models

---

## Live Demo

**Live Application:**  
https://vighnesh-movie-recommendation.streamlit.app

# 📸 Application Preview

<video src="screenshots/movie_recommendation_system_demo.mp4" width="100%" controls></video>

---

# Recommendation Models

## 1.Content-Based Filtering

This model recommends movies based on their semantic similarity.

### Information Used

* Genres
* Keywords
* Plot Overview
* Director
* Cast

### Workflow

```text
Movie Metadata
      │
      ▼
Sentence Transformer
(all-MiniLM-L6-v2)
      │
      ▼
Sentence Embeddings
      │
      ▼
Cosine Similarity
      │
      ▼
Top Similar Movies
```

### Explainability

For every recommendation, the system explains:

* Shared Genres
* Common Keywords
* Plot Similarity
* Same Director (if applicable)

---

## 2. Collaborative Filtering

This model learns user preferences from historical movie ratings.

### Algorithm

* Singular Value Decomposition (SVD)
* Matrix Factorization

### Workflow

```text
User Ratings
      │
      ▼
SVD Model
      │
      ▼
Predicted Ratings
      │
      ▼
Top Recommended Movies
```

### Explainability

Each recommendation includes:

* Predicted Rating
* User Preference Score
* Recommendation Confidence

---

## 3. 🤝 Hybrid Recommendation Engine

The hybrid engine combines both recommendation strategies.

### Workflow

```text
Content Score
        +
Collaborative Score
        │
        ▼
Weighted Score Fusion
        │
        ▼
Final Recommendation Ranking
```

This approach balances semantic similarity with user preferences to produce more accurate recommendations.

---

#  Explainable 

Unlike traditional recommendation systems, this project explains why a movie was recommended.

### Content-Based Explanation

* Matching Genres
* Matching Keywords
* Plot Similarity
* Director Match

### Collaborative Explanation

* Predicted User Rating
* Estimated Preference Percentage

### Hybrid Explanation

* Final Hybrid Score
* Content Similarity Score
* Collaborative Prediction Score

---

# Datasets

## MovieLens 25M Dataset

Used for:

* User ratings
* Collaborative Filtering
* SVD model training

Contains approximately:

* 25 Million Ratings
* 16,000+ Users
* Thousands of Movies

---

## TMDB 5000 Dataset

Used for:

* Movie metadata
* Genres
* Keywords
* Cast
* Crew
* Overview

The TMDB dataset is used to build semantic movie representations for the content-based recommendation engine.

---

# 🛠️ Technology Stack

## Programming Language

* Python

## Machine Learning & AI

* Sentence Transformers
* Deep Learning
* Natural Language Processing (NLP)
* Sentence Embeddings
* SVD Matrix Factorization
* Cosine Similarity
* Hybrid Recommendation

## Libraries

* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Scikit-Surprise
* PyTorch
* Transformers
* Requests



#  Installation

Clone the repository

```bash
git clone <repository-url>
cd Movie-Recommendation-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 📊 Recommendation Pipeline

```text
                User
                  │
                  ▼
      Select Movie / User
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
 Content     Collaborative   Hybrid
      │           │
      └───────┬───┘
              ▼
      Explainability Layer
              ▼
      Streamlit Dashboard
```

---

# 🎯 Key Highlights

* Three independent recommendation engines
* Explainable recommendations
* Hybrid recommendation strategy
* Interactive Streamlit interface
* Semantic movie understanding using transformers
* Personalized recommendations using collaborative filtering
* Real movie posters and metadata
* Clean, modular project architecture

---

# 🔮 Future Improvements

* User login and profile management
* Real-time rating updates
* Deep Learning Collaborative Filtering (Neural CF)
* Recommendation diversity optimization
* User feedback loop
* Movie trailer integration
* Model performance analytics
* Cloud deployment with CI/CD

---

# 👨‍💻 Author

**Vighnesh Sankpal**

B.Tech in Data Science

Machine Learning | Data Science | Artificial Intelligence

If you found this project useful, consider giving it a ⭐ on GitHub.
