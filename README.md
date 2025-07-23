# **Project: Social Compatibility Analyzer**

**A browser extension that analyzes Twitter profiles to generate a "Social Compatibility Score" based on shared interests, hobbies, and communication style.**

## **1\. Project Overview**

This tool is designed to enhance social media by helping users discover new friends and potential romantic interests. It operates as a browser extension on Twitter, providing a seamless, "on-demand" analysis.

When a user hovers over a profile picture, the extension fetches the target user's recent tweets, compares them to the user's own profile, and displays a compatibility percentage along with key shared interests. The core goal is to facilitate personal connections by highlighting similarities in hobbies and sense of humor (approximated by sentiment analysis).

## **2\. Technology Stack**

This project is divided into two main components: a Python backend for the analysis and a JavaScript frontend for the browser extension.

* **Backend (The "Brain")**  
  * **Programming Language:** Python 3.x  
  * **Web Framework:** FastAPI or Flask (to serve the analysis results to the extension).  
  * **Core Libraries:**  
    * Tweepy: For interacting with the Twitter API.  
    * scikit-learn: For machine learning tasks, specifically for TF-IDF.  
    * nltk (Natural Language Toolkit): For text processing (tokenization, stopwords).  
    * vaderSentiment: For sentiment analysis.  
* **Frontend (The "Face")**  
  * **Platform:** Chrome Browser Extension  
  * **Languages:** JavaScript, HTML, CSS  
* **Database**  
  * For the **Minimum Viable Product (MVP)**, a persistent database is **not required**. The analysis is performed in real-time.  
  * **Future Enhancement:** A Redis or PostgreSQL database could be implemented to cache user scores and profiles, reducing API calls and improving performance.

## **3\. Core Analysis Logic**

The compatibility score is a weighted average of two key components: Hobby Similarity and Sentiment Similarity.

### **Hobby Analysis (Interest Matching)**

This measures how much two users talk about the same topics.

1. **Data Collection:** Fetch the last \~200 tweets for both the user and the target.  
2. **Text Cleaning:** Remove URLs, mentions, punctuation, and common "stopwords".  
3. **Vectorization with TfidfVectorizer:** The cleaned text from each user is converted into a numerical vector using the **TF-IDF (Term Frequency-Inverse Document Frequency)** algorithm from the scikit-learn library. This technique identifies words that are most significant and characteristic of each user's vocabulary.  
4. **Similarity Calculation with cosine\_similarity:** We calculate the **cosine similarity** between the two users' TF-IDF vectors. This produces a score from 0.0 (completely different topics) to 1.0 (identical topics).

### **Humor/Sentiment Analysis (Communication Style Matching)**

This approximates a user's communication style by measuring the average sentiment of their tweets.

1. **Sentiment Scoring:** Each tweet is analyzed using the vaderSentiment library, which assigns a "compound" sentiment score from \-1.0 (very negative) to \+1.0 (very positive).  
2. **Average Sentiment:** We calculate the average sentiment score for all of a user's tweets.  
3. **Similarity Calculation:** The similarity is calculated based on the absolute difference between the two users' average sentiment scores. A smaller difference results in a higher similarity score.

### **Final Scoring Formula**

The final compatibility score is calculated with a 60/40 weighting:

Final Score \= (0.6 \* Hobby\_Score) \+ (0.4 \* Sentiment\_Score)

## **4\. Project Roadmap**

### **Phase 1: The Foundation \- API & Data Handling**

* **Goal:** To successfully communicate with the Twitter API and fetch the necessary data.  
* **Tasks:**  
  * Apply for and secure Twitter API keys (this is the most crucial first step).  
  * Write the core backend logic to authenticate a user.  
  * Create functions to fetch the last N tweets for a given user ID, handling potential errors and API limits gracefully.

### **Phase 2: The Brains \- Building the Analysis Engine**

* **Goal:** To implement the logic that compares two users and generates a compatibility score.  
* **Tasks:**  
  * **Text Pre-processing:** Clean the raw tweet data by removing URLs, mentions, special characters, and common "stopwords" (like 'and', 'the', 'a') to prepare it for analysis.  
  * **Hobby Analysis:** Use a technique like TF-IDF (Term Frequency-Inverse Document Frequency). This algorithm is perfect for identifying keywords that are most significant to a user. In simple terms, it scores words based on how often a user tweets them, while down-weighting words that are common everywhere (like 'Twitter').  
  * **Humor/Sentiment Analysis:** For the MVP, we'll use a pre-trained sentiment analysis model to assign a score to each tweet (e.g., from \-1 for very negative to \+1 for very positive). We can then find the average sentiment for each user to gauge their overall communication style.  
  * **Scoring Logic:** Combine the hobby and sentiment scores using our weighted formula: Final Score \= (0.6 \* Hobby\_Score) \+ (0.4 \* Sentiment\_Score).

### **Phase 3: The Face \- Creating the Browser Extension**

* **Goal:** To build the user-facing component that lives in the browser.  
* **Tasks:**  
  * Set up the basic structure of a Chrome extension (manifest.json, content scripts, popup scripts).  
  * Develop the UI for the "hover-card" (the tooltip that shows the score).  
  * Write the JavaScript code that detects when a user hovers over a profile, gets the user's ID, and calls our backend to get the score.  
  * Display the score and shared interests in the hover-card.

### **Phase 4: Integration & Testing**

* **Goal:** Connect all the pieces, test thoroughly, and polish.  
* **Tasks:**  
  * Deploy the backend engine to a server.  
  * Connect the browser extension to the live backend.  
  * Test, test, test\! Does it work on different profiles? Is it fast enough? Are there bugs?

### **CSS Rules**
Never repeat a class name or an ID. Ever.

### **Folder Structure**

social-compatibility-analyzer/
│
├── .gitignore              # Specifies intentionally untracked files to ignore
├── README.md               # The main project documentation we already created
│
├── backend/                # All Python code for the analysis engine and API
│   │
│   ├── .env                # (Untracked) Stores secret API keys and environment variables
│   ├── main.py             # Main FastAPI/Flask app file: defines API endpoints (e.g., /analyze)
│   ├── requirements.txt    # Lists all Python dependencies (e.g., flask, scikit-learn)
│   │
│   └── analyzer/           # A Python module for the core analysis logic
│       │
│       ├── __init__.py     # Makes the 'analyzer' directory a Python package
│       ├── processing.py   # Contains functions for cleaning and pre-processing tweet text
│       ├── scoring.py      # Contains functions for calculating hobby and sentiment scores
│       └── twitter_api.py  # Handles all communication with the Twitter API
│
└── extension/              # All files for the Chrome Browser Extension
    │
    ├── manifest.json       # The core configuration file for the Chrome extension
    │
    ├── icons/              # Icons for the extension
    │   ├── icon16.png
    │   ├── icon48.png
    │   └── icon128.png
    │
    ├── css/                # Stylesheets for the UI components
    │   └── style.css       # Styles for the hover-card
    │
    └── js/                 # JavaScript files
        │
        ├── content.js      # Injected into Twitter pages to detect hovers and display the UI
        └── api.js          # Helper module to handle fetch requests to our backend API




## **Run the Analyzer**


Here is a complete guide to running the Social Compatibility Analyzer for the first time.

### Prerequisites

1.  **Python Installed:** Ensure you have Python 3.7+ installed on your system.
2.  **Dependencies Installed:** You have run `pip install -r requirements.txt` inside the `backend` folder.
3.  **Google Chrome:** You have the Google Chrome browser installed.

---