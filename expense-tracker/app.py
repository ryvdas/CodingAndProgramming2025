from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def init_db():
    os.makedirs('expense-tracker/db', exist_ok=True)  # Ensure the directory exists
    with sqlite3.connect('expense-tracker/db/finances.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            balance REAL NOT NULL DEFAULT 0.0
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY,
                            date TEXT NOT NULL,
                            category TEXT NOT NULL,
                            amount REAL NOT NULL,
                            description TEXT,
                            type TEXT NOT NULL,
                            account_id INTEGER NOT NULL,
                            FOREIGN KEY (account_id) REFERENCES accounts (id)
                          )''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect('expense-tracker/db/finances.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()
    return render_template('index.html', accounts=accounts)

@app.route('/add_account', methods=['POST'])
def add_account():
    name = request.form['name']
    balance = request.form['balance']
    with sqlite3.connect('expense-tracker/db/finances.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, balance))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete_account/<int:id>')
def delete_account(id):
    with sqlite3.connect('expense-tracker/db/finances.db') as conn:
        cursor = conn.cursor()
        # Delete all transactions associated with the account
        cursor.execute("DELETE FROM transactions WHERE account_id = ?", (id,))
        # Delete the account
        cursor.execute("DELETE FROM accounts WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    date = request.form['date']
    category = request.form['category']
    amount = float(request.form['amount'])
    description = request.form['description']
    type = request.form['type']
    account_id = request.form['account_id']
    
    with sqlite3.connect('expense-tracker/db/finances.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (date, category, amount, description, type, account_id) VALUES (?, ?, ?, ?, ?, ?)", 
                       (date, category, amount, description, type, account_id))
        
        # Update account balance
        if type == 'income':
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        elif type == 'expense':
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
        
        conn.commit()
    
    return redirect(url_for('index'))

@app.route('/transactions')
def view_transactions():
    with sqlite3.connect('expense-tracker/db/finances.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT transactions.*, accounts.name FROM transactions JOIN accounts ON transactions.account_id = accounts.id")
        transactions = cursor.fetchall()
    return render_template('transactions.html', transactions=transactions)

@app.route('/update_transaction/<int:id>', methods=['GET', 'POST'])
def update_transaction(id):
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form['description']
        type = request.form['type']
        account_id = request.form['account_id']
        
        with sqlite3.connect('expense-tracker/db/finances.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT amount, type FROM transactions WHERE id = ?", (id,))
            old_transaction = cursor.fetchone()
            old_amount, old_type = old_transaction
            
            # Revert the old transaction's effect on the account balance
            if old_type == 'income':
                cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (old_amount, account_id))
            elif old_type == 'expense':
                cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (old_amount, account_id))
            
            # Update the transaction
            cursor.execute("UPDATE transactions SET date = ?, category = ?, amount = ?, description = ?, type = ?, account_id = ? WHERE id = ?", 
                           (date, category, amount, description, type, account_id, id))
            
            # Apply the new transaction's effect on the account balance
            if type == 'income':
                cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
            elif type == 'expense':
                cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
            
            conn.commit()
        
        return redirect(url_for('view_transactions'))
    else:
        with sqlite3.connect('expense-tracker/db/finances.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE id = ?", (id,))
            transaction = cursor.fetchone()
            cursor.execute("SELECT * FROM accounts")
            accounts = cursor.fetchall()
        return render_template('update_transaction.html', transaction=transaction, accounts=accounts)

@app.route('/delete_transaction/<int:id>')
def delete_transaction(id):
    with sqlite3.connect('expense-tracker/db/finances.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT amount, type, account_id FROM transactions WHERE id = ?", (id,))
        transaction = cursor.fetchone()
        amount, type, account_id = transaction
        
        # Revert the transaction's effect on the account balance
        if type == 'income':
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
        elif type == 'expense':
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        
        cursor.execute("DELETE FROM transactions WHERE id = ?", (id,))
        conn.commit()
    
    return redirect(url_for('view_transactions'))

@app.route('/summary')
def summary():
    with sqlite3.connect('expense-tracker/db/finances.db') as conn:
        cursor = conn.cursor()
        
        # Fetch expenses by category
        cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type = 'expense' GROUP BY category")
        expenses_by_category = cursor.fetchall()
        
        # Fetch account balance over time
        cursor.execute("SELECT date, SUM(CASE WHEN type = 'income' THEN amount ELSE -amount END) OVER (ORDER BY date) AS balance FROM transactions")
        balance_over_time = cursor.fetchall()
    
    return render_template('summary.html', expenses_by_category=expenses_by_category, balance_over_time=balance_over_time)

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)