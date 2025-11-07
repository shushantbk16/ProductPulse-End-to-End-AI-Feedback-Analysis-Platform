# app.py
import streamlit as st
import requests
import json

# --- This URL points to your FastAPI backend ---
# When running locally, they both run on your machine
API_URL = "http://127.0.0.1:8000/analyze_product/"

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="ProductPulse AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 ProductPulse: AI Feedback Analyst")
st.write("Enter a Reddit URL to scrape, analyze, and summarize all product reviews.")

# --- Input Box ---
url_input = st.text_input(
    "Enter the 'old.reddit.com' URL:",
    value="https://old.reddit.com/r/LenovoLegion/comments/1j8sosh/6_months_with_the_legion_7i_gen_9_ama/"
)

# --- Submit Button ---
if st.button("Analyze Product Reviews"):
    if url_input:
        with st.spinner("Scraping reviews and running AI analysis... This may take a minute."):
            try:
                # 1. This is where the UI calls your FastAPI backend
                payload = {
                    "url": url_input,
                    "product_name": "Product" # We can make this dynamic later
                }
                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:
                    # 2. Get the results
                    data = response.json()

                    st.subheader(f"✅ Analysis Complete for: {data['product_name']}")
                    st.write(f"Found {data['review_count']} reviews.")

                    # 3. Display the AI Analysis in a clean way
                    st.markdown("---")
                    st.header("AI-Generated Summary")
                    st.markdown(data['analysis']) # Use markdown to render bold/lists

                    # 4. Show the raw reviews in an expander
                    with st.expander("Show Raw Scraped Reviews"):
                        st.json(data['reviews'])

                else:
                    st.error(f"Error from API: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(f"Failed to connect to the API. Is it running at {API_URL}?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a URL.")