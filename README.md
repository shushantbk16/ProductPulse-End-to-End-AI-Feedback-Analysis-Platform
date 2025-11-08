
# 🚀 ProductPulse AI: End-to-End Generative AI Analysis Platform

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)

A full-stack, containerized AI microservice that analyzes product sentiment. This project demonstrates a production-ready MLOps workflow, from a backend API to a live, interactive web application.

## 🔴 Live Demo

**[Click here to use the live application](https://insight-engine-end-to-end-ai-feedback-analysis-platform.streamlit.app/)**

The backend is deployed on Render and the frontend on Streamlit Community Cloud.


---

## 🎯 Project Overview

In today's market, product managers must sift through thousands of customer reviews to understand sentiment. This process is manual, slow, and expensive.

**ProductPulse** solves this by providing an instant, AI-driven analysis. It simulates a data pipeline by consuming product data, feeding it to a generative AI, and returning a concise, actionable summary—reducing research time from hours to seconds.

### Key Features
* **AI-Powered Insights:** Uses the Google Gemini API to perform generative analysis on 100+ reviews at once.
* **Actionable Summaries:** Extracts the top 3 positive themes, top 3 negative themes, and a single actionable insight for product teams.
* **Full-Stack Architecture:** A robust FastAPI backend containerized with Docker and a clean, interactive Streamlit UI.
* **Reliable & Deployed:** The entire application is live on the web, demonstrating a complete, stable deployment.

---

## 🛠️ Tech Stack & Architecture

This project is separated into a backend microservice and a frontend client, which is a modern, scalable design.

* **Backend (API):** **FastAPI**, **Uvicorn**
* **AI Core:** **LangChain (LCEL)**, **Google Gemini API**
* **Frontend (UI):** **Streamlit**
* **Deployment (MLOps):** **Docker**, **Render** (for API), **Streamlit Cloud** (for UI)
* **Language:** **Python 3.10**

### Architecture Diagram

[User on Streamlit Cloud]
        |
        v
[1. Streamlit UI (app.py)]
        |
        v (HTTPS API Request)
[2. Render Cloud Server]
        |
        v
[3. Docker Container (Dockerfile)]
        |
        v
[4. FastAPI Backend (main.py)]
        |
        v
[5. Mock Data Module (scraper.py)] <--- (Stable Data Input)
        |
        v
[6. AI Analyzer (ai_analyzer.py)]
        |
        v (LangChain + Gemini API Call)
[7. Google Gemini AI]
        |
        v
[Response Sent Back to UI]
## 💡 Project Evolution: From Unstable Scraper to Stable API

This project's design demonstrates a key MLOps principle: **stability over complexity.**

1.  **Phase 1 (Scraping):** The initial version used **Playwright** to scrape live data from Reddit. While functional locally, this proved unstable in a deployed Docker environment due to robust anti-bot detection, causing the live demo to fail.
2.  **Phase 2 (Stable MLOps):** I made a strategic decision to pivot. I **modularized the data-fetching component** and replaced the unstable scraper with a **stable mock data module** (`scraper.py`).

This pivot proves the architecture is sound and demonstrates an understanding of production systems: **the AI/MLOps pipeline is the core asset**, and its data source should be reliable and swappable.

---

## 🏁 Getting Started (Local Development)

You can run this entire full-stack application on your local machine.

### Prerequisites
* Python 3.10+
* Docker Desktop
* A Google Gemini API Key

### 1. Set Up Your Environment

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/shushantbk16/ProductPulse-End-to-End-AI-Feedback-Analysis-Platform.git](https://github.com/shushantbk16/ProductPulse-End-to-End-AI-Feedback-Analysis-Platform.git)
    cd ProductPulse-End-to-End-AI-Feedback-Analysis-Platform
    ```

2.  **Create your secret `.env` file:**
    Create a file named `.env` in the root directory and add your API key:
    ```
    GOOGLE_API_KEY="AIzaSy...your...key...here"
    ```

3.  **Install requirements:**
    It's recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

### 2. Run the Backend (Docker)

The backend runs in a Docker container, just like in production.

1.  **Build the Docker image:**
    ```bash
    docker build -t product-pulse-api .
    ```

2.  **Run the container:**
    This command injects your local `.env` file to provide the API key.
    ```bash
cmddocker run -d -p 8000:8000 --env-file .env -t product-pulse-api
    ```
    Your backend is now running at `http://localhost:8000`. You can see the API docs at `http://localhost:8000/docs`.

### 3. Run the Frontend (Streamlit)

1.  **Open a *new* terminal window.**

2.  **Run the Streamlit app:**
    ```bash
    python -m streamlit run app.py
    ```
    Your browser will automatically open to `http://localhost:8501`, and you can use the full application.
