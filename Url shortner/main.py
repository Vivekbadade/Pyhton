import sqlite3
from flask import Flask, request, redirect, render_template
import string
import random

app = Flask(__name__)
# Connect to the SQLite database
conn = sqlite3.connect('url_shortener.db', check_same_thread=False)
# Create a table to store the URLs
conn.execute('''CREATE TABLE IF NOT EXISTS urls
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              original_url TEXT NOT NULL,
              short_code TEXT UNIQUE NOT NULL)''')

def generate_short_code(length=6):
    """Generate a random short code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_code = generate_short_code()
        # Insert the original URL and short code into the database
        conn.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)', (original_url, short_code))
        conn.commit()
        return render_template('index.html', short_code=short_code)
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    cursor = conn.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    row = cursor.fetchone()
    if row:
        return redirect(row[0])
    else:
        return 'URL not found', 404

@app.route('/stats')
def stats():
    #Delete duplicate entries
    conn.execute('DELETE FROM urls WHERE id NOT IN (SELECT MIN(id) FROM urls GROUP BY original_url)')
    conn.commit()
    cursor = conn.execute('SELECT short_code, original_url FROM urls')
    urls = cursor.fetchall()
    return render_template('stats.html', urls=urls)

if __name__ == '__main__':
    app.run(debug=True)