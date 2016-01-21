from flask import Flask, render_template, session, request, redirect, url_for, make_response
from utils import get_secret_key, check_login_info
from generate import randCSV

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/admintools/login', methods=['GET', 'POST'])
def adminlogin():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)

@app.route('/admintools/logout')
def adminlogout():
	session.pop('admin_username', None)
	return redirect(url_for('/admintools/login'))

@app.route('/admintools')
def admintools():
	if 'admin_username' in session:
		return render_template('adminhome.html')
	return redirect(url_for('/admintools/login'))

@app.route('/admintools/datagenerate')
def datagenerate():
	if 'admin_username' in session:
		return render_template('datagenerate.html')
	return redirect(url_for('/admintools/login'))

@app.route('/admintools/dataimport')
def dataimport():
	if 'admin_username' in session:
		return render_template('dataimport.html')
	return redirect(url_for('/admintools/login'))

@app.route('/download')
def download():
	a = request.args
	if a['filetype'] == 'CSV':
		result = randCSV(int(a['numPeople']), 'id' in a, 'grade' in a, 'email' in a, 'dob' in a,
			'address' in a,'phone' in a, a['delEntries'] == 'yes', float(a['prob']))
	response = make_response(result)
	response.headers["Content-Disposition"] = "attachment; filename=data.csv"
	return response

if __name__ == "__main__":
	app.debug = True
	app.secret_key = urandom(24)
	app.run(host="0.0.0.0", port=8000, threaded=True)
