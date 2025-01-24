import os
from dotenv import load_dotenv
import pyodbc
from flask import (Flask, render_template, request)

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
   return render_template('index.html')

@app.route('/transactions')
def transactions():
   try:
      query = """
         SELECT TOP 10 t.amount, t.description, t.date, c.name AS category_name
         FROM Transactions AS t
         JOIN Categories AS c ON t.category_id = c.id
         WHERE t.user_id = 1
         ORDER BY t.date DESC;
      """
      cursor.execute(query)
      transactions = cursor.fetchall()
      return render_template('transactions.html', transactions=transactions)
   
   except Exception as e:
      print(f"Error: {e}")
      return "An error occurred while fetching the transactions."

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


if __name__ == '__main__':
   app.run()