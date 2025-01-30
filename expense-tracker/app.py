from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('expense-tracker/db/expenses.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            category TEXT,
                            amount REAL,
                            description TEXT
                          )''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

@app.route('/add', methods=['POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']

        with sqlite3.connect('expense-tracker/db/expenses.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)", 
                           (date, category, amount, description))
            conn.commit()
        
        return redirect(url_for('index'))

@app.route('/expenses')
def view_expenses():
    with sqlite3.connect('expense-tracker/db/expenses.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
    return render_template('expenses.html', expenses=expenses)