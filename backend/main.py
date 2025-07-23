from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Import our analysis function from the analyzer module
from analyzer.scoring import generate_compatibility_report

# --- Application Setup ---
app = FastAPI(
    title="Social Compatibility Analyzer API",
    description="An API that analyzes two Twitter users and returns a compatibility score.",
    version="0.1.0",
)

# --- CORS (Cross-Origin Resource Sharing) ---
# This allows our browser extension (running on twitter.com) to make requests to this API.
origins = [
    "https://twitter.com",
    "https://mobile.twitter.com",
    "https://x.com",
    "https://mobile.x.com",
    "http://localhost:3000", # Optional: for local frontend development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Data Models ---
# This defines the expected structure for the request body.
class AnalyzeRequest(BaseModel):
    user_a_id: str
    user_b_id: str

# --- API Endpoints ---
@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"status": "ok", "message": "Social Compatibility Analyzer API is running."}


@app.post("/analyze")
def analyze_users(request: AnalyzeRequest):
    """
    Analyzes two Twitter users and returns a compatibility report.
    """
    # --- !! IMPORTANT PLACEHOLDER !! ---
    # In a real application, we would use request.user_a_id and request.user_b_id
    # to call a function in `twitter_api.py` to fetch their actual tweets.
    # For now, we are using the same mock data for demonstration purposes.
    
    user_a_tweets = [
        "Just finished a great weekend project using Python and FastAPI. The world of AI is moving so fast!",
        "Anyone seen the latest sci-fi movie? Mind-blowing visuals. I love good world-building.",
        "My cat just knocked over my coffee. A classic Monday moment, lol.",
    ]
    user_b_tweets = [
        "I'm so impressed with the new generative AI models. The possibilities for creative coding are endless.",
        "Rewatching my favorite sci-fi series from the 90s. The practical effects still hold up!",
        "My dog is the goofiest animal on the planet. Never fails to make me laugh.",
    ]
    # --- End of Placeholder Section ---
    
    # Generate the report using our scoring module
    report = generate_compatibility_report(user_a_tweets, user_b_tweets)
    
    return report

# --- To run this server ---
# Open your terminal in the 'backend' directory and run:
# uvicorn main:app --reload
