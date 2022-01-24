# Imports
from flask import Flask, render_template, request
from paddleocr import PaddleOCR
import cv2
import os
import sys
import psycopg2

app = Flask(__name__)

# Elephant SQL connection
POSTGRESQL_URI = # db connection here
connection = psycopg2.connect(POSTGRESQL_URI)
with connection:
		with connection.cursor() as cursor:
			cursor.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

# Create users table
try:
	with connection:
		with connection.cursor() as cursor:
			cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL, securityq1 TEXT NOT NULL, securityq2 TEXT NOT NULL);")
except psycopg2.errors.DuplicateTable:
	pass

# Create posts table
try:
	with connection:
		with connection.cursor() as cursor:
			cursor.execute("CREATE TABLE posts (id SERIAL PRIMARY KEY, email TEXT NOT NULL UNIQUE, image );")
except psycopg2.errors.DuplicateTable:
	pass

### Web pages ###
# login page
@app.route("/", methods=["GET", "POST"])
def login():
	print(request.args)

	return render_template("login.html")

# register page
@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":
		print(request.args)

		with connection:
			with connection.cursor() as cursor:
				cursor.execute("INSERT INTO users (email, password, securityq1, securityq2) VALUES (%s, %s, %s, %s);",
					(
						request.form.get("email"),
						request.form.get("password"),
						request.form.get("securityq1"),
						request.form.get("securityq2"),
					),
				)

	return render_template("register.html")

# profile page
@app.route("/profile")
def hello():
	list = []
	ocr_model = PaddleOCR(lang='en')
	img_path = os.path.join('.', 'testRX.jpg')
	result = ocr_model.ocr(img_path)

	for res in result:
		list.append(res[1][0])


	with connection:
			with connection.cursor() as cursor:
				cursor.execute("INSERT INTO users (email, password, securityq1, securityq2) VALUES (%s, %s, %s, %s);",
					(
						request.form.get("email"),
						request.form.get("password"),
						request.form.get("securityq1"),
						request.form.get("securityq2"),
					),
				)

	return render_template("profile.html", list = list)

# main
if __name__ == '__main__':
    app.debug = True
    app.run()


