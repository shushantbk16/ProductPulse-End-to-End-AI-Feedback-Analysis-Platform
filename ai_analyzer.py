# ai_analyzer.py
import os 
from typing import List

# --- FINAL FREE IMPORTS ---
# We use the community package for Hugging Face integration
from langchain_community.llms import HuggingFaceHub 
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
# --------------------------

# --- LLM INITIALIZATION BLOCK ---

# 1. Retrieve the key that Render successfully injected into the environment
API_KEY_VALUE = os.getenv("HUGGINGFACE_API_KEY")

# 2. Check if the key is valid and initialize the LLM
if API_KEY_VALUE and API_KEY_VALUE.strip():
    # Initialize the LLM using the free, high-performance Mistral model
    llm = HuggingFaceHub(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        model_kwargs={"temperature": 0.1, "max_length": 1024}, # Increased output size for better summaries
        huggingfacehub_api_token=API_KEY_VALUE
    )
    print("DEBUG: AI Client Initialized with Mistral (Hugging Face).")
else:
    # Key is NOT present: Create a NULL client to prevent crashing the worker
    llm = None
    print("FATAL: HUGGINGFACE_API_KEY is missing or invalid. Using graceful fail.")

# --- PROMPT DEFINITION (Unchanged) ---
PROMPT_TEMPLATE = """
You are a world-class AI assistant for analyzing product reviews.
I have provided you with {doc_count} customer reviews.

Your task is to analyze them and provide a concise, actionable summary
for a product manager. Do not just list the reviews.

Please provide the following in markdown format:
1.  **Positive Themes:** 2-3 key things users consistently loved.
2.  **Negative Themes:** 2-3 key problems or complaints users consistently had.
3.  **Actionable Insight:** One key suggestion for the product team based on the sentiment.
4.  **Key Quotes:** 2-3 short, powerful quotes that exemplify the main themes.

REVIEWS:
{context}
"""

SUMMARY_PROMPT = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "doc_count"]
)

def format_docs_with_context(docs: List[Document]) -> str:
    """Joins all review texts into a single string, separated by a line."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def analyze_reviews(reviews: List[str]) -> str:
    """
    Analyzes a list of review strings using a modern LangChain (LCEL) chain.
    """
    if not reviews:
        return "No reviews provided to analyze."

    # --- FINAL CHECK FOR NULL CLIENT ---
    if llm is None:
        return "FATAL ERROR: AI Client failed to initialize. Please check HUGGINGFACE_API_KEY in Render dashboard."
    # ----------------------------------

    try:
        # Convert the raw strings into LangChain "Document" objects
        docs = [Document(page_content=text) for text in reviews]
        
        # Modern LangChain (LCEL) "stuff" chain
        chain = (
            {
                "context": lambda x: format_docs_with_context(x["input_documents"]),
                "doc_count": lambda x: len(docs)
            }
            | SUMMARY_PROMPT
            | llm
        )
        
        print(f"Sending {len(docs)} reviews to the Hugging Face Inference API for analysis...")
        
        # Run the chain!
        response = chain.invoke({
            "input_documents": docs,
            "doc_count": len(docs)
        })
        
        return response
        # Note: HuggingFaceHub often returns a string directly, not an AIMessage object.

    except Exception as e:
        # This catches any final errors during the API request
        return f"An error occurred during analysis: {e}"