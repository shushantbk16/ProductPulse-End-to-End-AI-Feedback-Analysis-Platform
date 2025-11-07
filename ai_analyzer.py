# ai_analyzer.py
import config
from typing import List

# --- UPDATED IMPORTS (These are the correct, modern paths) ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# ai_analyzer.py

import os # <-- MUST BE AT THE TOP OF YOUR IMPORTS
from typing import List
# ... (rest of imports) ...
from langchain_google_genai import ChatGoogleGenerativeAI
# ... (rest of imports) ...

# --- LLM INITIALIZATION BLOCK (The Final Fix) ---

# We explicitly tell the Google client where to find the key in the environment
# The library will automatically look for GOOGLE_API_KEY if not specified, 
# but setting it here is the safest way to ensure Gunicorn finds it.
# We retrieve the key using os.getenv()
API_KEY_VALUE = os.getenv("GOOGLE_API_KEY")

# 1. We must ensure the client is initialized with the key
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0,
    google_api_key=API_KEY_VALUE # Passing the key retrieved from Render's environment
)

# ... (rest of the file remains the same, including the analyze_reviews function) ...

# 2. Define our Prompts (The "Instructions") - THIS IS UNCHANGED
PROMPT_TEMPLATE = """
You are a world-class AI assistant for analyzing product reviews.
I have provided you with {doc_count} reviews for a product.

Your task is to analyze them and provide a concise, actionable summary
for a product manager. Do not just list the reviews.

Please provide the following:
1.  **Positive Themes:** 2-3 key things users consistenly loved.
2.  **Negative Themes:** 2-3 key problems or complaints users consistenly had.
3.  **Actionable Insight:** One key suggestion for the product team.
4.  **Key Quotes:** 2-3 short, powerful quotes that exemplify the main themes.

REVIEWS:
{context}
"""

SUMMARY_PROMPT = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["context", "doc_count"]
)

# This helper function will format all our docs into one big string
def format_docs_with_context(docs: List[Document]) -> str:
    """Joins all review texts into a single string, separated by a line."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def analyze_reviews(reviews: List[str]) -> str:
    """
    Analyzes a list of review strings using a modern LangChain (LCEL) chain.
    """
    if not reviews:
        return "No reviews provided to analyze."

    if not config.GOOGLE_API_KEY:
        print("\n--- WARNING: GOOGLE_API_KEY not found. ---")
        print("--- Returning a MOCK AI response for testing. ---\n")
        return "--- MOCK ANALYSIS (GOOGLE_API_KEY not found) ---"

    try:
        # Convert the raw strings into LangChain "Document" objects
        docs = [Document(page_content=text) for text in reviews]
        
        # --- NEW: Modern LangChain (LCEL) "stuff" chain ---
        # This is the modern replacement for LLMChain and StuffDocumentsChain
        
        # This chain defines the data flow:
        # 1. We pass in our "docs" and "doc_count"
        # 2. A function formats the docs into the "context" string.
        # 3. The "context" and "doc_count" are fed into the prompt.
        # 4. The formatted prompt is sent to the LLM.
        # 5. We get the AI's response content.
        
        chain = (
            {
                "context": lambda x: format_docs_with_context(x["input_documents"]),
                "doc_count": lambda x: x["doc_count"]
            }
            | SUMMARY_PROMPT
            | llm
        )
        
        print(f"Sending {len(docs)} reviews to the Google Gemini API for analysis...")
        
        # Run the chain!
        response = chain.invoke({
            "input_documents": docs,
            "doc_count": len(docs)
        })
        
        # The new response object is an AIMessage. We just need its .content
        return response.content

    except Exception as e:
        print(f"Error during AI analysis: {e}")
        return f"An error occurred during analysis: {e}"