Expense Tracker Application
===========================

Overview
--------
The Expense Tracker application is a web-based tool that helps students manage their personal finances by tracking account balances, income, and expenses. Users can input details about their income sources and expenses, including the amount, category, and date of each transaction. The application provides features to view the current balance, generate summaries of income and expenses over specified periods (e.g., weekly, monthly), and categorize expenses to show spending patterns. Additionally, users can update or delete existing entries and offer search and filter options to easily find specific transactions.

Features
--------
- Add, update, and delete accounts
- Add, update, and delete transactions (income and expenses)
- View account balances
- Generate summaries of expenses by category
- View account balance over time with a line graph
- Confirmation dialogs to prevent accidental deletions

Technologies Used
-----------------
- Python
- Flask
- SQLite
- HTML/CSS
- Chart.js

Setup Instructions
------------------
1. Clone the repository to your local machine.
2. Navigate to the `expense-tracker` directory.
3. Create a virtual environment:
python3 -m venv venv
4. Activate the virtual environment:
- On macOS/Linux:
  ```
  source venv/bin/activate
  ```
- On Windows:
  ```
  .\venv\Scripts\activate
  ```
5. Install the required packages:
pip install flask
6. Run the application:
python app.py
7. Open your web browser and navigate to `http://127.0.0.1:5000/` to access the Expense Tracker application.

Project Structure
-----------------
- `app.py`: The main application file containing the Flask routes and database interactions.
- `templates/`: Directory containing HTML templates for the application.
  - `index.html`: The main page for viewing and managing accounts.
  - `transactions.html`: Page for viewing and managing transactions.
  - `update_transaction.html`: Page for updating a transaction.
  - `summary.html`: Page for viewing summaries of expenses and account balance over time.
- `static/`: Directory containing static files such as CSS and JavaScript.
  - `css/`: Directory containing CSS files for styling the application.
  - `js/`: Directory containing JavaScript files for rendering charts.

Database Schema
---------------
- `accounts` table:
  - `id`: INTEGER PRIMARY KEY
  - `name`: TEXT NOT NULL
  - `balance`: REAL NOT NULL DEFAULT 0.0
- `transactions` table:
  - `id`: INTEGER PRIMARY KEY
  - `date`: TEXT NOT NULL
  - `category`: TEXT NOT NULL
  - `amount`: REAL NOT NULL
  - `description`: TEXT
  - `type`: TEXT NOT NULL (income or expense)
  - `account_id`: INTEGER NOT NULL (FOREIGN KEY referencing `accounts` table)

Contact
-------
For any questions or issues, please contact ryvdas@gmail.com
