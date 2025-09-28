from flask import Flask, request, redirect, url_for, send_from_directory
import mysql.connector
import os
import time

app = Flask(__name__, static_url_path='/static', static_folder='.')

# Connect to MySQL with retry
while True:
    try:
        db = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "database"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "kali"),
            database=os.getenv("MYSQL_DATABASE", "form")
        )
        print("✅ Database connected")
        break
    except mysql.connector.Error as err:
        print(f"❌ Connection error: {err}")
        time.sleep(5)

# Create messages table
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    company VARCHAR(100),
    subject VARCHAR(100),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.close()

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/send message', methods=['POST'])
def send_message():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    company = request.form.get('company')
    subject = request.form.get('subject')
    message = request.form.get('message')

    try:
        cursor = db.cursor()
        query = """
        INSERT INTO messages (full_name, email, company, subject, message)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (full_name, email, company, subject, message)
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        print("✅ Message saved:", values)
    except mysql.connector.Error as err:
        print(f"❌ Insert error: {err}")

    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return send_from_directory(os.getcwd(), 'thankyou.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
