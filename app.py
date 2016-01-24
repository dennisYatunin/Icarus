from flask import Flask, render_template, session, request, redirect, url_for, make_response
from utils import get_secret_key, initialize_database, check_login_info, randCSV, upload_data

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
		return render_template(
			'adminhome.html', name=session['admin_username']
			)
	return redirect(url_for('adminlogin'))

@app.route('/admintools/datagenerate')
def datagenerate():
	if 'admin_username' in session:
		return render_template(
			'datagenerate.html', name=session['admin_username']
			)
	return redirect(url_for('adminlogin'))

@app.route('/admintools/dataimport')
def dataimport():
	if 'admin_username' in session:
		return render_template(
			'dataimport.html', name=session['admin_username']
			)
	return redirect(url_for('adminlogin'))

@app.route('/download')
def download():
	d = request.args
	if d['filetype'] == 'CSV':
		result = randCSV(
			int(d['numPeople']), 'id' in a, 'grade' in a,
			'email' in a, 'dob' in a, 'address' in a,'phone' in a,
			d['delEntries'] == 'yes', float(d['prob']))
	response = make_response(result)
	response.headers["Content-Disposition"] = "attachment; filename=data.csv"
	return response

@app.route('/upload', methods=['POST'])
def upload():
	d = request.form
	return upload_data(
		request.files['file'], d['category'], d['numColumns'],
		d['id'], d['level'], d['email'], d['phone'], d['address'],
		d['dob'], d['name'], d['fname'], d['lname']
		)

if __name__ == "__main__":
	initialize_database()
	app.debug = True
	app.secret_key = get_secret_key()
	# Users are not allowed to upload more than 20 MB of data.
	app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
	app.run(host="0.0.0.0", port=8000, threaded=True)
