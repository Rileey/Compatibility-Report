from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Import the pre-processing function from our other module
from .processing import preprocess_tweets

def calculate_hobby_similarity(tweets1: list[str], tweets2: list[str]) -> tuple[float, list[str]]:
    """
    Calculates interest similarity using TF-IDF and Cosine Similarity.

    Args:
        tweets1: A list of raw tweet strings for user 1.
        tweets2: A list of raw tweet strings for user 2.

    Returns:
        A tuple containing:
        - The cosine similarity score (float from 0.0 to 1.0).
        - A list of the top 5 most significant shared keywords.
    """
    processed_tweets1 = preprocess_tweets(tweets1)
    processed_tweets2 = preprocess_tweets(tweets2)
    
    # Combine all text from each user into a single document
    user1_doc = " ".join(processed_tweets1)
    user2_doc = " ".join(processed_tweets2)

    if not user1_doc or not user2_doc:
        return 0.0, []

    # Vectorize the documents
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user1_doc, user2_doc])
    
    # Calculate cosine similarity
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Find common interest keywords
    feature_names = vectorizer.get_feature_names_out()
    v1_weights = tfidf_matrix[0].toarray()[0]
    v2_weights = tfidf_matrix[1].toarray()[0]
    
    common_keywords_with_scores = []
    for i, name in enumerate(feature_names):
        # Find keywords with significant weight for both users
        if v1_weights[i] > 0.1 and v2_weights[i] > 0.1:
            # Score is the product of their weights
            score = v1_weights[i] * v2_weights[i]
            common_keywords_with_scores.append((name, score))

    # Sort keywords by their score in descending order and take the top 5
    common_keywords_with_scores.sort(key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, score in common_keywords_with_scores[:5]]
    
    return float(similarity_score), top_keywords

def calculate_sentiment_similarity(tweets1: list[str], tweets2: list[str]) -> float:
    """
    Calculates sentiment similarity using VADER.

    Args:
        tweets1: A list of raw tweet strings for user 1.
        tweets2: A list of raw tweet strings for user 2.

    Returns:
        A sentiment similarity score (float from 0.0 to 1.0).
    """
    analyzer = SentimentIntensityAnalyzer()
    
    # Calculate average sentiment for user 1
    total_sentiment1 = sum(analyzer.polarity_scores(tweet)['compound'] for tweet in tweets1)
    avg_sentiment1 = total_sentiment1 / len(tweets1) if tweets1 else 0
    
    # Calculate average sentiment for user 2
    total_sentiment2 = sum(analyzer.polarity_scores(tweet)['compound'] for tweet in tweets2)
    avg_sentiment2 = total_sentiment2 / len(tweets2) if tweets2 else 0
    
    # Calculate similarity (1 minus the normalized difference)
    # The range of compound scores is [-1, 1], so the max difference is 2.
    sentiment_difference = abs(avg_sentiment1 - avg_sentiment2)
    similarity_score = 1 - (sentiment_difference / 2)
    
    return float(similarity_score)

def generate_compatibility_report(user_a_tweets: list[str], user_b_tweets: list[str]) -> dict:
    """
    Generates the final compatibility report by combining scores.

    Args:
        user_a_tweets: A list of raw tweet strings for user A.
        user_b_tweets: A list of raw tweet strings for user B.

    Returns:
        A dictionary containing the final score and shared interests.
    """
    hobby_score, common_interests = calculate_hobby_similarity(user_a_tweets, user_b_tweets)
    sentiment_score = calculate_sentiment_similarity(user_a_tweets, user_b_tweets)
    
    # Apply weights: 60% for hobbies, 40% for sentiment
    final_score = (0.6 * hobby_score) + (0.4 * sentiment_score)
    
    report = {
        "final_score": round(final_score * 100), # As a percentage
        "shared_interests": common_interests
    }
    
    return report

# Example Usage (for testing purposes)
if __name__ == '__main__':
    # Sample data mimicking two different users
    user_a = [
        "Just finished a great weekend project using Python and FastAPI. The world of AI is moving so fast!",
        "Anyone seen the latest sci-fi movie? Mind-blowing visuals. I love good world-building.",
        "My cat just knocked over my coffee. A classic Monday moment, lol.",
    ]
    user_b = [
        "I'm so impressed with the new generative AI models. The possibilities for creative coding are endless.",
        "Rewatching my favorite sci-fi series from the 90s. The practical effects still hold up!",
        "My dog is the goofiest animal on the planet. Never fails to make me laugh.",
    ]
    
    full_report = generate_compatibility_report(user_a, user_b)
    print("--- Compatibility Report ---")
    print(f"Final Score: {full_report['final_score']}%")
    print(f"Shared Interests: {full_report['shared_interests']}")
