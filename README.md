# Crypto Portfolio & Sentiment API

A RESTful API built with Flask that allows users to track their cryptocurrency portfolio and analyze market sentiment from social media.

## 🚀 Features

- **Portfolio Management**: Full CRUD operations (via API) to track your cryptocurrency holdings and their current USD value.
- **Real-Time Market Data**: Fetches live prices, market cap, and 24h volume from the CoinGecko API for top cryptocurrencies.
- **Social Sentiment Analysis**: Analyzes sentiment from social media posts (via a mock X/Twitter API) using TextBlob's NLP to gauge market mood.
- **RESTful API**: A clean Flask backend serving JSON endpoints for all data.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: MySQL
- **Data & APIs**: Pandas, Requests, CoinGecko API
- **NLP**: TextBlob for Sentiment Analysis

## ⚡ Quick Start

1.  **Clone & Setup**:
    ```bash
    git clone <your-repo-url>
    cd crypto_portfolio_tracker
    pip install -r requirements.txt
    ```

2.  **Database Setup**:
    ```sql
    mysql -u root -p < crypto_db.sql
    ```

3.  **Run the Server**:
    ```bash
    python crypto_dashboard.py
    ```
    The API will be live at `http://localhost:5000`.

---
*Note: The X/Twitter API integration uses mock data for demonstration. Replace `fetch_x_posts()` with a real API client for production use.*
