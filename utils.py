from os import urandom
from os.path import isfile
from hashlib import sha512
from uuid import uuid4
from sqlite3 import connect

def get_secret_key():
	'''Returns a key that may be used to secure a Flask session

	The key is a 32-character string generated with the os.urandom function.
	'''
	return urandom(32)

def initialize_database():
	'''Creates the tables in the database

	If the app is being run for the first time, the administrators, students,
	teachers, and sections tables are created; also, the data for the username
	'admin' and password '' is inserted into the administrators table.
	'''
	if not isfile('data.db'):
		conn = connect('data.db')
		c = conn.cursor()
		q = 'CREATE TABLE administrators \
		( \
			name TEXT, salt INT, hash_value INT \
			)'
		c.execute(q)
		q = 'INSERT INTO administrators (rowid, name, salt, hash_value) \
		VALUES (?, ?, ?, ?)'
		c.execute(q, (1, 'admin', '', sha512('').hexdigest()))
		q = 'CREATE TABLE students \
		( \
			id TEXT UNIQUE, name TEXT, salt INT, hash_value INT, \
			email TEXT, dob TEXT, address TEXT, phone TEXT, \
			level TEXT, cursched TEXT, pastscheds TEXT \
			)'
		c.execute(q)
		q = 'INSERT INTO students (id, name, salt, hash_value, email, dob, ' + \
			'address, phone, level, cursched, pastscheds) VALUES (?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?)'
		c.execute(q, (1, 'Dennis Yatunin', '', sha512('').hexdigest(), 'dyatun@gmail.com', '06/19/98', '2121 Shore Pkwy.', '718-265-4895', '12', 'NOPE', 'NOPE'))
		q = 'CREATE TABLE teachers \
		( \
			id TEXT UNIQUE, name TEXT, salt INT, hash_value INT, \
			email TEXT, dob TEXT, address TEXT, phone TEXT, \
			level TEXT, cursched TEXT, pastscheds TEXT \
			)'
		c.execute(q)
		q = 'CREATE TABLE sections \
		( \
			id TEXT UNIQUE, className TEXT, teacherId TEXT, pd TEXT \
			)'
		c.execute(q)
		conn.close()

def check_login_info(username, password, table):
	'''Returns whether the database contains a user with the given information

	Checks the students, teachers, or administrators table for a user matching
	the given username and password.
	'''
	conn = connect('data.db')
	c = conn.cursor()
	q = 'SELECT salt, hash_value FROM %s WHERE name = ?' % table
	salt_n_hash = c.execute(q, (username,)).fetchone()
	conn.close()
	# If the username does not exist, return false.
	if not salt_n_hash:
		return False
	# If the password is wrong, return false.
	if (
		sha512((password + salt_n_hash[0]) * 10000).hexdigest() != salt_n_hash[1]
		):
		return False
	# Finally, return true.
	return True
