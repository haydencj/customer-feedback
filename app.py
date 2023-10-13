from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
from flask_mysqldb import MySQL

load_dotenv()

# create flask
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'customerfeedback'

# import mysql.connector
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root  ",
#     password=os.getenv('MYSQL_PASSWORD'),
#     database="customerfeedback"
# )
# print(conn)

# connect to mysql database
mysql = MySQL(app)

# print("MYSQL Password:", os.getenv('MYSQL_PASSWORD'))
# print("MySQL Connection:", mysql.connection)

# basic route
@app.route('/')
def home():
    return redirect(url_for('login'))

# user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # get form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        password = userDetails['password']

        # insert user data into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur.close()

        # redirect to login page after successful registration
        return redirect(url_for('login'))
    
    # render the registration form
    return render_template('register.html')

# user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get login form data
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']

        # verify credentials in the database
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))

        # if the credentials are valid, redirect to the dashboard
        if result > 0:
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'
        cur.close()

    # render the login form
    return render_template('login.html')

# feedback submission
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # get feedback form data
        feedbackDetails = request.form
        title = feedbackDetails['title']
        feedback = feedbackDetails['feedback']

        # insert feedback into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback(title, feedback) VALUES(%s, %s)", (title, feedback))
        mysql.connection.commit()
        cur.close()

        return 'Feedback Submitted'
    
    # render the feedback form
    return render_template('feedback.html')

# admin dashboard to manage feedback
@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()

    # retrieve all feedback from the database
    result = cur.execute("SELECT * FROM feedback")
    cur.close()

    if result > 0:
        feedbacks = cur.fetchall()

        # render the dashboard with feedback data
        return render_template('dashboard.html', feedbacks=feedbacks)
    else:
        return 'No Feedback Available'

if __name__ == '__main__':
    app.run(debug=True)