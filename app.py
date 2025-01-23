import os
from dotenv import load_dotenv
import pyodbc
from flask import (Flask, redirect, render_template, request, send_from_directory, url_for)

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
      return render_template('index.html', transactions=transactions)
   except Exception as e:
      # This will log any database or query-related error to the console
      print(f"Error: {e}")
      return "An error occurred while fetching the transactions."


if __name__ == '__main__':
   app.run()