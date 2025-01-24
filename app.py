import os
from dotenv import load_dotenv
import pyodbc
from flask import (Flask, render_template, request, redirect, url_for)
import random

load_dotenv()

server = os.environ.get("DBSERVER")
database = os.environ.get("DBNAME")
username = os.environ.get("DBUSERNAME")
password = os.environ.get("DBPASSWORD")
driver= os.environ.get("DBDRIVER")

conn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()

app = Flask(__name__)


@app.route('/')
def index():

   ads = ['ad1.mp4', 'ad2.mp4', 'ad3.mp4', 'ad4.mp4']
   selected_ad = random.choice(ads)

   query = """ 
      SELECT SUM(amount) AS total_spent
      FROM Transactions
      WHERE user_id = 1 AND date >= DATEADD(day, -30, GETDATE())
   """
   cursor.execute(query)
   total = cursor.fetchone()
   total_spent = total[0] if total[0] else 0
   return render_template('index.html', total=total_spent, selected_ad=selected_ad)


@app.route('/transactions')
def transactions():

   ads = ['ad1.mp4', 'ad2.mp4', 'ad3.mp4', 'ad4.mp4']
   selected_ad = random.choice(ads)

   try:
      query = """
         SELECT t.id, t.amount, t.description, t.date, c.name AS category_name
         FROM Transactions AS t
         JOIN Categories AS c ON t.category_id = c.id
         WHERE t.user_id = 1
         ORDER BY t.date DESC;
      """
      cursor.execute(query)
      transactions = cursor.fetchall()
      return render_template('transactions.html', transactions=transactions, selected_ad=selected_ad)
   
   except Exception as e:
      print(f"Error: {e}")
      return "An error occurred while fetching the transactions."


@app.route('/delete_transactions', methods=['POST'])
def delete_transactions():
   transaction_ids = request.form.getlist('transaction_ids')

   if transaction_ids:
      placeholders = ",".join("?" for _ in transaction_ids)
      query = f"DELETE FROM Transactions WHERE id IN ({placeholders})"
      cursor.execute(query, transaction_ids)
      conn.commit()
   else:
      return "No transactions selected to delete.", 400

   return redirect('/transactions')


@app.route('/api/expenses')
def get_expenses():
   query = """
      SELECT c.name AS category_name, SUM(t.amount) AS total_spent
      FROM Transactions t
      JOIN Categories c ON t.category_id = c.id
      WHERE t.user_id = 1 AND c.type != 'Income' AND t.date >= DATEADD(day, -30, GETDATE())
      GROUP BY c.name
   """
   cursor.execute(query)
   transactions = cursor.fetchall()

   labels = [row.category_name for row in transactions]  # Category names
   values = [row.total_spent for row in transactions]    # Corresponding amounts

   return {"labels": labels, "values": values}


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
   if request.method == 'POST':
      amount = request.form['amount']
      category_id = request.form['category_id']
      description = request.form['description']
      date = request.form['date']

      query = """
         INSERT INTO Transactions (user_id, category_id, amount, date, description)
         VALUES (?, ?, ?, ?, ?)
      """
      cursor.execute(query, (1, category_id, amount, date, description))
      conn.commit()

      return redirect(url_for('index'))

def fetch_categories():
    query = "SELECT id, name FROM Categories"
    cursor.execute(query)
    return cursor.fetchall()

@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'GET':
        query = """
            SELECT t.amount, t.description, t.date, c.id AS category_id, c.name AS category_name
            FROM Transactions t
            JOIN Categories c ON t.category_id = c.id
            WHERE t.id = ?
        """
        cursor.execute(query, transaction_id)
        transaction = cursor.fetchone()
        
        if not transaction:
            return "Transaction not found.", 404

        return render_template(
            'edit_transaction.html',
            transaction_id=transaction_id,
            amount=transaction.amount,
            description=transaction.description,
            date=transaction.date,
            category_id=transaction.category_id,
            category_name=transaction.category_name,
            categories=fetch_categories()
        )

    elif request.method == 'POST':
        new_amount = request.form['amount']
        new_description = request.form['description']
        new_date = request.form['date']
        new_category_id = request.form['category_id']

        query = """
            UPDATE Transactions
            SET amount = ?, description = ?, date = ?, category_id = ?
            WHERE id = ?
        """
        cursor.execute(query, (new_amount, new_description, new_date, new_category_id, transaction_id))
        conn.commit()

        return redirect('/transactions')
    

if __name__ == '__main__':
   app.run(debug=True, port=8000)