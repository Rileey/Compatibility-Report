import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# --- NLTK Data Download ---
# A function to ensure the necessary NLTK data is available.
def download_nltk_data():
    """Checks for NLTK data and downloads it if missing."""
    try:
        # Check if 'punkt_tab' is available, if not, download it
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("NLTK 'punkt_tab' package not found. Downloading...")
        nltk.download('punkt_tab')
        print("Download complete.")
        
    try:
        # Check if 'stopwords' is available, if not, download it
        stopwords.words('english')
    except LookupError:
        print("NLTK 'stopwords' package not found. Downloading...")
        nltk.download('stopwords')
        print("Download complete.")

# Call the function to ensure data is ready when the module is loaded
download_nltk_data()


def preprocess_tweets(tweet_list: list[str]) -> list[str]:
    """
    Cleans a list of raw tweet strings.

    This function performs several key text pre-processing steps:
    1. Converts text to lowercase.
    2. Removes URLs.
    3. Removes mentions (@username) and the hashtag symbol (#) but keeps the word.
    4. Removes punctuation.
    5. Tokenizes the text into individual words.
    6. Removes common English "stopwords" (e.g., 'the', 'a', 'in').
    
    Args:
        tweet_list: A list of strings, where each string is a raw tweet.

    Returns:
        A list of strings, where each string is a cleaned version of the original tweet,
        ready for analysis.
    """
    # Load English stopwords once
    stop_words = set(stopwords.words('english'))
    
    cleaned_tweets = []
    
    for tweet in tweet_list:
        # Step 1: Convert to lowercase
        tweet = tweet.lower()
        
        # Step 2: Remove URLs
        tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
        
        # Step 3: Remove mentions and hashtag symbols
        tweet = re.sub(r'\@\w+|\#','', tweet)
        
        # Step 4: Remove punctuation
        tweet = tweet.translate(str.maketrans('', '', string.punctuation))
        
        # Step 5: Tokenize the tweet
        tokens = word_tokenize(tweet)
        
        # Step 6: Remove stopwords
        cleaned_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        
        # Join the tokens back into a single string
        cleaned_tweets.append(" ".join(cleaned_tokens))
        
    return cleaned_tweets

# Example Usage (for testing purposes)
if __name__ == '__main__':
    sample_tweets = [
        "Just finished a great weekend project using Python & FastAPI! The world of #AI is moving so fast! Check it out: https://example.com",
        "My cat just knocked over my coffee... A classic Monday moment, lol. @MyCat",
        "Trying to learn how to bake sourdough bread. It's harder than it looks. #baking"
    ]
    
    processed = preprocess_tweets(sample_tweets)
    
    print("--- Original Tweets ---")
    for t in sample_tweets:
        print(f"- {t}")
        
    print("\n--- Processed Tweets ---")
    for p in processed:
        print(f"- {p}")

