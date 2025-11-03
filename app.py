import os
import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

# Detect whether to use PostgreSQL
USE_POSTGRES = os.environ.get("USE_POSTGRES", "0") == "1"

if USE_POSTGRES:
    # PostgreSQL connection
    DB_HOST = os.environ['DB_HOST']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_NAME = os.environ['DB_NAME']

    def get_pg_connection():
        return psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )

    # Initialize PostgreSQL table
    try:
        conn = get_pg_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                message TEXT
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Error initializing PostgreSQL:", e)

else:
    # SQLite local database
    DATABASE = os.path.join('/tmp', 'contacts.db')

    def get_sqlite_connection():
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # allows access by column name
        return conn

    # Initialize SQLite table
    conn = get_sqlite_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS contacts (name TEXT, email TEXT, message TEXT)')
    conn.close()

# Helper function to fetch rows as dicts
def fetch_all_as_dicts(cursor, use_postgres=False):
    if use_postgres:
        return cursor.fetchall()  # RealDictCursor already returns dicts
    else:
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if USE_POSTGRES:
        conn = get_pg_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)',
            (name, email, message)
        )
        conn.commit()
        cursor.close()
        conn.close()
    else:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)',
            (name, email, message)
        )
        conn.commit()
        conn.close()

    return jsonify({'message': f'Thank you, {name}. Your information has been added successfully.'})


@app.route('/submissions')
def submissions():
    if USE_POSTGRES:
        conn = get_pg_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM contacts")
        rows = fetch_all_as_dicts(cursor, use_postgres=True)
        cursor.close()
        conn.close()
    else:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = fetch_all_as_dicts(cursor)
        conn.close()

    html = "<h1>Submissions</h1><ul>"
    for row in rows:
        html += f"<li>{row['name']} - {row['email']} - {row['message']}</li>"
    html += "</ul>"
    return html


if __name__ == '__main__':
    app.run(debug=True)