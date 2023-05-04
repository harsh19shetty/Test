from flask import Flask, render_template, request
from datetime import date
import pymysql
import pymysql.cursors

_configVars = {"cdmDBHost": "10.40.0.2", "cdmDBuser": "root", "cdmDBpwd": "NNYp9XM4zkDnZvn5", "cdmDB": "cb_tesing", "cdmDBPort": 32048}
cur = pymysql.connect(host=_configVars["cdmDBHost"], user=_configVars["cdmDBuser"], password=_configVars["cdmDBpwd"], database=_configVars["cdmDB"], port= _configVars["cdmDBPort"], cursorclass=pymysql.cursors.DictCursor)
app = Flask(__name__)

# Function to calculate age from date of birth
def calculate_age(dob):
    birth_date = date.fromisoformat(dob)
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Define the index route
@app.route('/')
def index():
    return render_template('index.html')

# Define the submit route
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data from request
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    city = request.form['city']
    dob = request.form['dob']
    age = calculate_age(dob) # Calculate age using function defined earlier

    # Insert data into database
    with cur.cursor() as _cursor:
        _sqlStmt = "INSERT INTO customers (name, phone, email, city, dob, age) VALUES (%s, %s, %s, %s, %s, %s)"
        _cursor.execute(_sqlStmt, (name, phone, email, city, dob, age))

    cur.commit()

    with cur.cursor() as _cursor:
        _sqlStmt = "SELECT age FROM customers where name = %s and phone = %s and email = %s and city = %s and dob = %s"
        _cursor.execute(_sqlStmt, (name, phone, email, city, dob))
        user_age = _cursor.fetchall()
        user_age = [dict(row)["age"] for row in user_age][0]

    cur.commit()
    cur.close()

    return render_template('submit.html', name=name, age=user_age)

if __name__ == '__main__':
    app.run()
