# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Import your new, stable data fetcher and the AI analyzer
from scraper import scrape_product_reviews
from ai_analyzer import analyze_reviews
import config

# --- Pydantic Models ---

# The input now expects a clean product identifier (ASIN)
class AnalyzeRequest(BaseModel):
    product_asin: str
    product_name: str

# The response model remains the same
class AnalyzeResponse(BaseModel):
    product_name: str
    review_count: int
    analysis: str
    reviews: List[str]

# Initialize the FastAPI app
app = FastAPI(
    title=config.PROJECT_NAME,
    description="Analyzes product reviews using GenAI",
    version="0.1.0"
)

# --- API Endpoints ---
@app.get("/")
def get_root():
    """A simple 'Hello World' endpoint to confirm the server is running."""
    return {"message": f"Welcome to the {config.PROJECT_NAME} API"}


@app.post("/analyze_product/", response_model=AnalyzeResponse)
def analyze_product(request: AnalyzeRequest):
    """
    This is the main endpoint.
    1. It receives a clean product ASIN.
    2. It fetches reviews from the simulated Amazon API.
    3. It analyzes the reviews using our AI.
    4. It returns the analysis.
    """
    
    # 1. Fetch the reviews using the stable API fetcher
    # Note: We pass the ASIN instead of the URL
    reviews = scrape_product_reviews(request.product_asin)
    
    # 2. Call the AI analyzer function
    if reviews:
        analysis = analyze_reviews(reviews)
    else:
        analysis = "Fetching returned no reviews to analyze. (Check ASIN or API connection)."
    
    # 3. Return the new, complete response
    return {
        "product_name": request.product_name,
        "review_count": len(reviews),
        "analysis": analysis,
        "reviews": reviews
    }