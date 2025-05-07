from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def init_db():
    db_path = '/tmp/properties.db' if os.getenv('VERCEL') else 'properties.db'
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    address TEXT NOT NULL,
                    image_url TEXT,
                    created_at TIMESTAMP
                )
            ''')
            # Insert sample data if table is empty
            cursor.execute("SELECT COUNT(*) FROM properties")
            if cursor.fetchone()[0] == 0:
                sample_properties = [
                    ('Cozy Family Home', '3 bed, 2 bath home with modern amenities', 350000, '123 Maple St', '/static/images/house1.jpg', datetime.now()),
                    ('Luxury Condo', '2 bed, 2 bath with city views', 550000, '456 Oak Ave', '/static/images/condo1.jpg', datetime.now()),
                    ('Spacious Townhouse', '4 bed, 3 bath with large backyard', 450000, '789 Pine Rd', '/static/images/townhouse1.jpg', datetime.now())
                ]
                cursor.executemany("INSERT INTO properties (title, description, price, address, image_url, created_at) VALUES (?, ?, ?, ?, ?, ?)", sample_properties)
            conn.commit()
            logger.info(f"Database initialized at {db_path}")
    except sqlite3.Error as e:
        logger.error(f"SQLite error: {e}")
        raise

@app.route('/')
def index():
    logger.info("Accessing index route")
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Template error: {e}")
        return "Error loading index page", 500

@app.route('/listings')
def listings():
    logger.info("Accessing listings route")
    db_path = '/tmp/properties.db' if os.getenv('VERCEL') else 'properties.db'
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM properties")
            properties = cursor.fetchall()
        return render_template('listings.html', properties=properties)
    except sqlite3.Error as e:
        logger.error(f"SQLite error: {e}")
        return "Error loading listings", 500
    except Exception as e:
        logger.error(f"Template error: {e}")
        return "Error loading listings", 500

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    logger.info("Accessing contact route")
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        logger.info(f"Contact Form: {name}, {email}, {message}")
        return redirect(url_for('index'))
    try:
        return render_template('contact.html')
    except Exception as e:
        logger.error(f"Template error: {e}")
        return "Error loading contact page", 500

@app.route('/about')
def about():
    logger.info("Accessing about route")
    try:
        return render_template('about.html')
    except Exception as e:
        logger.error(f"Template error: {e}")
        return "Error loading about page", 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)