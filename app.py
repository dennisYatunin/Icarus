from flask import Flask, render_template, session, request, redirect, url_for, make_response
from os import urandom
import json

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/admintools')
def admintools():
	return render_template('adminhome.html')

@app.route('/admintools/datagenerate')
def datagenerate():
	return render_template('datagenerate.html')

@app.route('/download', methods=['POST'])
def download():
	user = request.form['numStudents']
	password = request.form['filetype']
	return json.dumps({'status':'OK','user':user,'pass':password})

# This route will prompt a file download with the csv lines
@app.route('/downloads')
def downloads():
	csv = """"REVIEW_DATE","AUTHOR","ISBN","DISCOUNTED_PRICE"
	"1985/01/21","Douglas Adams",0345391802,5.95
	"1990/01/12","Douglas Hofstadter",0465026567,9.95
	"1998/07/15","Timothy ""The Parser"" Campbell",0968411304,18.99
	"1999/12/03","Richard Friedman",0060630353,5.95
	"2004/10/04","Randel Helms",0879755725,4.50"""
	# We need to modify the response, so the first thing we
	# need to do is create a response out of the CSV string
	response = make_response(csv)
	# This is the key: Set the right header for the response
	# to be downloaded, instead of just printed on the browser
	response.headers["Content-Disposition"] = "attachment; filename=books.csv"
	return response

if __name__ == "__main__":
	app.debug = True
	app.secret_key = urandom(24)
	app.run(host="0.0.0.0", port=8000, threaded=True)
