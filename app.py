# Imports
from flask import Flask, render_template, request, session, redirect, url_for, flash
import sys
import psycopg2
import psycopg2.extras
import re
from functions import *
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

# secret key for flash messages
### [REMOVE THIS SECRET KEY FROM FILE BEFORE UPLOADING TO GITHUB OTHERWISE THE SECRET KEY WILL BE MADE PUBLIC (i.e. app.secret_key ='']) ###
app.secret_key = '\x9f\xed\xb7\xb4bo\xc4\xb5\xcb\x00W\x0b'

# Elephant SQL connection
### [REMOVE THIS POSTGRESQL WEBLINK FROM THIS FILE BEFORE UPLOADING TO GITHUB OTHERWISE DB ACCESS WILL BE MADE PUBLIC (i.e. POSTGRESQL_URI =""]) ###
POSTGRESQL_URI = "postgres://zvnmwduo:gjGsAHHJjKbCnQLSEmyS3H2VlnMk-ZIq@kashin.db.elephantsql.com/zvnmwduo"
connection = psycopg2.connect(POSTGRESQL_URI)

# Create users table
try:
	with connection:
		with connection.cursor() as cursor:
			cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, firstname VARCHAR (100) NOT NULL, lastname VARCHAR (100) NOT NULL, username VARCHAR (50) NOT NULL, password VARCHAR (255) NOT NULL, email VARCHAR (50) NOT NULL, securityq1 VARCHAR (50) NOT NULL, securityq2 VARCHAR (50) NOT NULL);")
except psycopg2.errors.DuplicateTable:
	pass

# Create posts table
try:
	with connection:
		with connection.cursor() as cursor:
			cursor.execute("CREATE TABLE posts (id SERIAL PRIMARY KEY, user_name VARCHAR (50) NOT NULL, content VARCHAR (100) NOT NULL);")
except psycopg2.errors.DuplicateTable:
	pass



### Web pages and FUnctions ###

# Homepage
@app.route('/', methods=["GET", "POST"])
def home():
	# Connect to db
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

	# Check if user is loggedin
	if 'loggedin' in session:

		# Display user's previous entries
		cursor.execute('SELECT * FROM posts WHERE user_name = %s', (session['username'],))
		posts = cursor.fetchall()

		# User is loggedin show them the home page
		return render_template('home.html', firstname=session['firstname'], posts=posts)
		
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))



# Function to add posts using OpenCV and PaddleOCR functions from functions.py file
@app.route("/add", methods=["GET", "POST"])
def add():

	errorCheck = False
	# Connect to db
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

	# Get pic of Prescription or text
	try:
		getPic() # OpenCV function in functions.py
	except:
		flash("Please reconnect webcam.")
		errorCheck = True
	
	# Translate picture to text
	try:
		list = getPrescription() # PaddleOCR function in functions.py
	except:
		flash("Error occured please try again.")
		errorCheck = True

	# Convert list of text elements into a String
	string1 = ""
	
	try:
		for l in list:
			string1 += (l + "||||")
	except:
		flash("Error occured please try again.")
		errorCheck = True

	if errorCheck == False:
		# Assign username field in users table to user_name field in posts
		session['user_name'] = session['username']
		user_name = session['username']

		# Create new post for specified user in posts db
		cursor.execute("INSERT INTO posts (user_name, content) VALUES (%s,%s)", (user_name, string1))
		connection.commit()

	# Reload the Homepage
	return redirect(url_for('home'))



# Function to delete posts
@app.route("/delete", methods=["GET", "POST"])
def delete():
	# Connect to db
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

	# Get user entered from form ID number
	ID = request.form['ID']

	# Delete the post
	cursor.execute("DELETE FROM posts WHERE id = %s", (ID,))
	connection.commit()

	return redirect(url_for('home'))



# Login page
@app.route("/login/", methods=["GET", "POST"])
def login():
	# Connect to db
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

	# Check if "username" and "password" POST requests exist (user submitted form)
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
 
		# Check if account exists using MySQL
		cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
		# Fetch one record and return result
		account = cursor.fetchone()
 
		if account:
			password_rs = account['password']
			print(password_rs)
			# If account exists in users table in db
			if check_password_hash(password_rs, password):
				# Create session data, we can access this data in other routes
				session['loggedin'] = True
				session['id'] = account['id']
				session['username'] = account['username']
				session['firstname'] = account['firstname']
				# Redirect to home page
				return redirect(url_for('home'))
			else:
				# Account doesnt exist or username/password incorrect
				flash("Either your account doesn't exist or you have entered the wrong username or password.")
		else:
			# Account doesnt exist or username/password incorrect
			flash("Either your account doesn't exist or you have entered the wrong username or password.")

	return render_template("login.html")



# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
	# Connect to db
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

	sent = False
 
	# Check if all fields POST requests exist (user submitted form)
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'password2' in request.form and 'email' in request.form  and 'firstname' in request.form  and 'lastname' in request.form  and 'securityq1' in request.form  and 'securityq2' in request.form:
		# Create variables for easy access
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		username = request.form['username']
		password = request.form['password']
		password2 = request.form['password2']
		email = request.form['email']
		securityq1 = request.form['securityq1']
		securityq2 = request.form['securityq2']
    
		_hashed_password = generate_password_hash(password)
 
		# Check if account exists using MySQL
		cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
		account = cursor.fetchone()
		# If account exists show error and validation checks
		if account:
			flash('Account already exists!')
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			flash('Invalid email address!')
		elif not re.match(r'[A-Za-z0-9]+', username):
			flash('Username must contain only characters and numbers!')
		elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$', password):
			flash('Password must contain one uppercase letter, one lowercase letter, one number, one special character(@, $, !, %, *, #, ?, &), and must be 8-18 characters long.')
		elif password != password2:
			flash('Passwords do not match.')
		elif not username or not password or not email:
			flash('Please fill out the form!')
		else:
			# Account doesnt exist and the form data is valid, now insert new account into users table
			cursor.execute("INSERT INTO users (firstname, lastname, username, password, email, securityq1, securityq2) VALUES (%s,%s,%s,%s,%s,%s,%s)", (firstname, lastname, username, _hashed_password, email, securityq1, securityq2))
			connection.commit()
			sent = True
			flash('You have successfully registered!')
	elif request.method == 'POST':
		# Form is empty... (no POST data)
		flash('Please fill out the form!')
	# Show registration form with message (if any)
	return render_template('register.html', sent=sent)



# Profile page
@app.route("/profile")
def profile():
	# Connect to db
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
	# Check if user is loggedin
	if 'loggedin' in session:
		cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
		account = cursor.fetchone()
		# Show the profile page with account info
		return render_template('profile.html', account=account, list=list)
	# User is not loggedin redirect to login page
	return redirect(url_for('login'))



@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))



# Main
if __name__ == '__main__':
	app.debug = True
	app.run()

