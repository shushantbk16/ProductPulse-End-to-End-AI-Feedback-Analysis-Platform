# app.py
import streamlit as st
import requests
import json

# --- CONFIGURATION ---
# IMPORTANT: This URL points to your FastAPI backend, which is running inside Docker.
# Since the Docker container is running in the Codespace, 127.0.0.1:8000 is the correct address
API_URL = "http://127.0.0.1:8000/analyze_product/"

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ProductPulse AI",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 ProductPulse: E-commerce AI Analyst")
st.write("A professional microservice demo that fetches and summarizes live Amazon product reviews using GenAI.")

# --- INPUT SECTION ---
st.subheader("1. Enter Product ASIN (ID) for Analysis")

product_asin = st.text_input(
    "Enter an Amazon ASIN (e.g., B0BX4B4158 for a popular laptop):",
    value="B0BX4B4158" # Default ASIN for easy testing
)
product_name = st.text_input(
    "Enter Product Name (for labeling the analysis):",
    value="Lenovo Legion Pro 7i"
)

# --- SUBMIT BUTTON LOGIC ---
if st.button("Analyze Product Reviews", type="primary"):
    
    # 1. VALIDATE THE INPUT
    if not product_asin:
        st.warning("Please enter a valid ASIN.")
    else:
        with st.spinner("Calling API... Fetching 100+ reviews and running Gemini analysis. Please wait 15-30 seconds."):
            try:
                # 2. Build the payload with the CORRECT field names
                payload = {
                    "product_asin": product_asin, # Corrected key for the FastAPI model
                    "product_name": product_name
                }
                
                # 3. Call your FastAPI backend
                response = requests.post(API_URL, json=payload, timeout=300) 
                
                if response.status_code == 200:
                    # 4. Display the results
                    data = response.json()
                    
                    st.success(f"✅ Analysis Complete for: **{data['product_name']}**")
                    st.markdown(f"**Reviews Processed:** **`{data['review_count']}`**")
                    
                    if data['review_count'] > 0:
                        st.markdown("---")
                        st.header("AI-Generated Insights (from Gemini)")
                        
                        # 5. Display the Analysis
                        st.markdown(data['analysis']) 
                        
                        # Show raw data optionally
                        with st.expander("Show Raw Review Data"):
                            st.json(data['reviews'])
                    else:
                        st.error("No reviews were found for this ASIN. Check the ID or the API connection.")
                        
                else:
                    st.error(f"Error from API (Status {response.status_code}): Could not process request.")
                    st.code(response.text)

            except requests.exceptions.ConnectionError:
                st.error(f"Failed to connect to the API. Is your Docker container running at {API_URL}?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")