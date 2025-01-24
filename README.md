# Expense Tracker Web Application

An intuitive and interactive web application to track your expenses.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [TODO](#todo)

---

## Features

- **User Authentication**: Login system to manage individual user data.
- **Dashboard**:
  - Pie chart displaying expenses by category for the past 30 days.
  - Sidebar with navigational links to other features.
  - Randomized video ads displayed on each page refresh for somewhat aesthetic purposes.
- **Expense Management**:
  - Add transactions using a user-friendly form on the dashboard.
  - View and delete multiple transactions using checkboxes on the Transactions page.
  - Edit individual transactions with an inline form.
- **Database-Driven**: Data stored in and fetched from a SQL database for persistence.

---

## Technologies Used

- **Backend**:
  - [Flask](https://flask.palletsprojects.com/) (Python)
  - [pyodbc](https://pypi.org/project/pyodbc/) (Database connectivity)
  - Microsoft SQL Server
- **Frontend**:
  - HTML5, CSS3, JavaScript
  - Chart.js (for data visualization)
- **Other Tools**:
  - dotenv (for environment variable management)

  ---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/merito-pacba/lab10-Hozene.git
   cd lab10-Hozene
   ```

2. **Install Dependencies**:
   Create a virtual environment and install the required Python packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   pip install -r requirements.txt
   ```

3. **Set Up the Database**:
   - Create a SQL Server database and populate it.
   - Create `.env` file with your database credentials:
     ```
     DBSERVER=your_server
     DBNAME=your_database_name
     DBUSERNAME=your_username
     DBPASSWORD=your_password
     DBDRIVER={ODBC Driver 18 for SQL Server}
     ```

4. **Run the Application**:
   Run the app with the command `python app.py`.  

---

## Usage

### Adding a Transaction
- Navigate to the homepage.
- Fill out the **Add Transaction** form and click "Submit."
- The transaction will appear on the dashboard and be saved in the database.

### Viewing and Deleting Transactions
- Go to the **Transactions** page.
- Use the checkboxes to select multiple transactions and click "Delete" to remove them from the database.

### Editing Transactions
- On the Transactions page, hover over a transaction to reveal the **edit icon**.
- Click the icon to navigate to an edit page where you can update the transaction's details.

---

## TODO

1. Add user session management to maintain user-specific data across pages.
2. Add the database schema and sample data to the repository for easier setup.
3. Implement a user registration system for new users to create accounts.