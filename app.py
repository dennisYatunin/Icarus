from flask import Flask, render_template, session, request, redirect, url_for, make_response
from utils import get_secret_key, initialize_database, check_login_info
from generate import randCSV

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/admintools/login', methods=['GET', 'POST'])
def adminlogin():
	if request.method == 'POST':
		if check_login_info(
			request.form['username'],
			request.form['password'],
			'administrators'
			):
			session['admin_username'] = request.form['username']
			return redirect(url_for('adminhome'))
		return render_template('adminlogin.html', error=True)
	return render_template('adminlogin.html')

@app.route('/admintools/logout')
def adminlogout():
	session.pop('admin_username', None)
	return redirect(url_for('adminlogin'))

@app.route('/admintools')
@app.route('/admintools/home')
def adminhome():
	if 'admin_username' in session:
		return render_template('adminhome.html', name=session['admin_username'])
	return redirect(url_for('adminlogin'))

@app.route('/admintools/datagenerate')
def datagenerate():
	if 'admin_username' in session:
		return render_template('datagenerate.html', name=session['admin_username'])
	return redirect(url_for('adminlogin'))

@app.route('/admintools/dataimport')
def dataimport():
	if 'admin_username' in session:
		return render_template('dataimport.html', name=session['admin_username'])
	return redirect(url_for('adminlogin'))

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
	initialize_database()
	app.debug = True
	app.secret_key = get_secret_key()
	app.run(host="0.0.0.0", port=8000, threaded=True)
