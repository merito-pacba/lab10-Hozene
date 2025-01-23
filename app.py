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

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


if __name__ == '__main__':
   app.run()