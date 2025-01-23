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


@app.route('/index')
def index():
   user_id = 1

   query = """
        SELECT t.id, t.amount, t.description, t.date, c.name AS category_name
        FROM Transactions t
        JOIN Categories c ON t.category_id = c.id
        WHERE t.user_id = ?
        ORDER BY t.date DESC
        LIMIT 10;
    """
   cursor.execute(query, user_id)
   transactions = cursor.fetchall()
   return render_template('index.html', transactions)


if __name__ == '__main__':
   app.run(debug=True)