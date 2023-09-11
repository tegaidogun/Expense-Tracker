from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import os
import csv

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'your_fallback_secret_key'

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    expenses = cursor.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY month DESC, date DESC", (user_id,)).fetchall()
    conn.close()
    return render_template('home.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    amount = request.form.get('amount')
    description = request.form.get('description')
    date = datetime.now().strftime('%Y-%m-%d')
    month = datetime.now().strftime('%Y-%m')

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, description, date, month, user_id) VALUES (?, ?, ?, ?, ?)", (amount, description, date, month, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete_expense(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (id, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        amount = request.form.get('amount')
        description = request.form.get('description')
        date = request.form.get('date')
        month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')
        cursor.execute("UPDATE expenses SET amount = ?, description = ?, date = ?, month = ? WHERE id = ? AND user_id = ?", (amount, description, date, month, id, user_id))        
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    else:
        expense = cursor.execute("SELECT * FROM expenses WHERE id = ? AND user_id = ?", (id, user_id)).fetchone()
        conn.close()
        if expense:
            return render_template('edit.html', expense=expense)
        else:
            return "Access denied", 403
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')

        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        else:
            return 'Incorrect username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/import', methods=['GET', 'POST'])
def import_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            user_id = session['user_id']
            conn = sqlite3.connect('expenses.db')
            cursor = conn.cursor()
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("INSERT INTO expenses (amount, description, date, month, user_id) VALUES (?, ?, ?, ?, ?)", 
                               (row['Amount'], row['Description'], row['Date'], row['Month'], user_id))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
        else:
            return "Only CSV files are allowed", 400
    else:
        return render_template('import.html')

if __name__ == '__main__':
    app.run(debug=True)
