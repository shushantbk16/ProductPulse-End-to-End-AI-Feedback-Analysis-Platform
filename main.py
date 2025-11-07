# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Import our scraper and our NEW AI analyzer
from scraper import scrape_product_reviews
from ai_analyzer import analyze_reviews  # <-- 1. IMPORT THE NEW FUNCTION
import config

app = FastAPI(
    title=config.PROJECT_NAME,
    description="Analyzes product reviews using GenAI",
    version="0.1.0"
)

# --- Pydantic Models ---
class AnalyzeRequest(BaseModel):
    url: str
    product_name: str

# 2. UPDATE THE RESPONSE MODEL
class AnalyzeResponse(BaseModel):
    product_name: str
    review_count: int
    analysis: str                 # <-- 3. ADD THIS "analysis" FIELD
    reviews: List[str]

# --- API Endpoints ---
@app.get("/")
def get_root():
    return {"message": f"Welcome to the {config.PROJECT_NAME} API"}


@app.post("/analyze_product/", response_model=AnalyzeResponse)
def analyze_product(request: AnalyzeRequest):
    """
    This is the main endpoint.
    1. It validates and fixes the incoming URL.
    2. It scrapes the reviews from that URL.
    3. It analyzes the reviews using our AI.
    4. It returns the analysis and the raw reviews.
    """

    # --- THIS IS THE NEW FIX ---
    if "reddit.com" not in request.url:
        return {
            "product_name": request.product_name,
            "review_count": 0,
            "analysis": "Error: Not a valid Reddit URL.",
            "reviews": []
        }

    # Automatically convert 'www' links to 'old' links
    # This makes our API robust.
    url_to_scrape = request.url.replace("www.reddit.com", "old.reddit.com")
    if not url_to_scrape.startswith("https://old.reddit.com"):
         url_to_scrape = f"https://old.reddit.com{url_to_scrape}"
    # --- END OF FIX ---


    # 1. Call your scraper function (using the *fixed* URL)
    reviews = scrape_product_reviews(url_to_scrape)

    # 2. Call your new AI analyzer function
    if reviews:
        analysis = analyze_reviews(reviews)
    else:
        analysis = "Scraping returned no reviews to analyze. (The post may be removed or have no comments)."

    # 3. Return the new, complete response
    return {
        "product_name": request.product_name,
        "review_count": len(reviews),
        "analysis": analysis,
        "reviews": reviews
    }