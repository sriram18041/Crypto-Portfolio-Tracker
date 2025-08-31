from flask import Flask, render_template, request, jsonify, g
import mysql.connector
import requests
from textblob import TextBlob
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'root',  # Replace with your MySQL password
    'database': 'crypto_db'
}

# Database connection
def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(**db_config)
            print("Connected to database:", g.db.is_connected())
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            raise
    return g.db

# Function to get the cursor
def get_cursor():
    db = get_db()
    return db.cursor()

# CoinGecko API base URL
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Mock X API (replace with actual API or mock data for testing)
def fetch_x_posts(coin):
    mock_posts = [
        f"{coin} is going to the moon! 🚀 #crypto",
        f"Big dip in {coin}, time to buy? 📉",
        f"{coin} has great potential, but risky. #investing",
        f"Not sure about {coin}, too volatile. 😕"
    ]
    return mock_posts

# Sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return 'positive', polarity
    elif polarity < 0:
        return 'negative', polarity
    return 'neutral', polarity

# Fetch crypto prices
def fetch_crypto_prices(coins):
    try:
        url = f"{COINGECKO_API}/simple/price?ids={','.join(coins)}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching prices: {e}")
        return {}

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# API to add portfolio entry
@app.route('/api/add_holding', methods=['POST'])
def add_holding():
    print("Received /api/add_holding request")
    cursor = None
    try:
        data = request.get_json()
        print("Received data:", data)
        coin_id = data['coin_id']
        amount = float(data['amount'])
        
        cursor = get_cursor()
        query = "INSERT INTO portfolio (coin_id, amount) VALUES (%s, %s)"
        print("Executing query with values:", (coin_id, amount))
        cursor.execute(query, (coin_id, amount))
        get_db().commit()
        print("Database commit successful")
        return jsonify({'message': 'Holding added successfully'}), 201
    except (KeyError, ValueError) as e:
        print("Input error:", str(e))
        return jsonify({'error': 'Invalid input data'}), 400
    except mysql.connector.Error as err:
        print("MySQL error:", str(err))
        return jsonify({'error': str(err)}), 500
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({'error': 'Unexpected error occurred'}), 500

# API to get portfolio data
@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    try:
        cursor = get_cursor()
        cursor.execute("SELECT coin_id, amount FROM portfolio")
        holdings = cursor.fetchall()
        coins = [h[0] for h in holdings]
        prices = fetch_crypto_prices(coins)
        
        portfolio_data = []
        total_value = 0
        for coin_id, amount in holdings:
            price = prices.get(coin_id, {}).get('usd', 0)
            value = amount * price
            total_value += value
            portfolio_data.append({
                'coin_id': coin_id,
                'amount': amount,
                'price': price,
                'value': value
            })
        
        return jsonify({
            'portfolio': portfolio_data,
            'total_value': total_value
        })
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

# API to get market data
@app.route('/api/market_data', methods=['GET'])
def get_market_data():
    try:
        coins = ['bitcoin', 'ethereum', 'binancecoin']
        prices = fetch_crypto_prices(coins)
        market_data = []
        for coin in coins:
            data = prices.get(coin, {})
            market_data.append({
                'coin_id': coin,
                'price': data.get('usd', 0),
                'market_cap': data.get('usd_market_cap', 0),
                'volume_24h': data.get('usd_24h_vol', 0)
            })
        return jsonify(market_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API to get sentiment data
@app.route('/api/sentiment', methods=['GET'])
def get_sentiment():
    try:
        coins = ['bitcoin', 'ethereum', 'binancecoin']
        sentiment_data = []
        cursor = get_cursor()
        for coin in coins:
            posts = fetch_x_posts(coin)
            sentiments = [analyze_sentiment(post) for post in posts]
            positive = sum(1 for s in sentiments if s[0] == 'positive')
            negative = sum(1 for s in sentiments if s[0] == 'negative')
            neutral = sum(1 for s in sentiments if s[0] == 'neutral')
            
            query = """
                INSERT INTO sentiment (coin_id, positive_count, negative_count, neutral_count, analysis_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (coin, positive, negative, neutral, datetime.now()))
            get_db().commit()
            
            sentiment_data.append({
                'coin_id': coin,
                'positive': positive,
                'negative': negative,
                'neutral': neutral
            })
        return jsonify(sentiment_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Close database connection after each request
@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()
        print("Database connection closed")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)