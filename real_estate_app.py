from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    with sqlite3.connect('properties.db') as conn:
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listings')
def listings():
    with sqlite3.connect('properties.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM properties")
        properties = cursor.fetchall()
    return render_template('listings.html', properties=properties)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # In a production app, you'd save this to a database or send an email
        print(f"Contact Form: {name}, {email}, {message}")
        return redirect(url_for('index'))
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)