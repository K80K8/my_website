import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
# import shutil
import os 


app = Flask(__name__)

CORS(app)

# src = os.path.join(os.path.dirname(__file__), 'contacts.db')
# dst = os.path.join('/tmp', 'contacts.db')

# if not os.path.exists(dst):
#     shutil.copy(src, dst)

DATABASE = os.path.join('/tmp', 'contacts.db')

def init_sqlite_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('CREATE TABLE IF NOT EXISTS contacts (name TEXT, email TEXT, message TEXT)')
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)', (name, email, message))
    conn.commit()
    conn.close()

    response_message = f'Thank you, {name}. Your information has been added successfully.'

    return jsonify({'message': response_message})

if __name__ == '__main__':
    app.run(debug=True)