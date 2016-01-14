from flask import Flask, render_template, session, request, redirect, url_for
from os import urandom

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/admintools')
def admintools():
	return render_template('adminhome.html')

@app.route('/admintools/datagenerate')
def admintools():
	return render_template('datagenerate.html')

if __name__ == "__main__":
	app.debug = True
	app.secret_key = urandom(24)
	app.run(host="0.0.0.0", port=8000)
