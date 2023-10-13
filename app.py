from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
from flask_mysqldb import MySQL
import mysql.connector

load_dotenv()

# create flask
app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': 'customerfeedback'
}

# connect to mysql database
# conn = mysql.connector.connect(**db_config)

# basic route
@app.route('/')
def home():
    return redirect(url_for('login'))

# user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # get form data
            userDetails = request.form
            name = userDetails['name']
            email = userDetails['email']
            password = userDetails['password']

            # insert user data into the database
            conn = mysql.connector.connect(**db_config)
            cur = conn.cursor()
            cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, password))
            conn.commit()
            cur.close()
            conn.close()

            # redirect to login page after successful registration
            return redirect(url_for('login'))
        except Exception as e:
            print("Error:", e)
            return str(e)
    
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
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close() 
        conn.close()

        # if the credentials are valid, redirect to the dashboard
        if user:
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'

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
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("INSERT INTO feedback(title, feedback) VALUES(%s, %s)", (title, feedback))
        conn.commit()
        cur.close()
        conn.close()

        return 'Feedback Submitted'
    
    # render the feedback form
    return render_template('feedback.html')

# admin dashboard to manage feedback
@app.route('/dashboard')
def dashboard():
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()

    # retrieve all feedback from the database
    cur.execute("SELECT * FROM feedback")
    feedbacks = cur.fetchall()
    cur.close()
    conn.close()

    if feedbacks:
        # render the dashboard with feedback data
        return render_template('dashboard.html', feedbacks=feedbacks)
    else:
        return 'No Feedback Available'

if __name__ == '__main__':
    app.run(debug=True)