from os import urandom
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
	'admin' and password '' is inserted into administrators.
	'''
	conn = connect("data.db")
	c = conn.cursor()
	q = 'CREATE TABLE IF NOT EXISTS administrators \
	( \
		name TEXT, salt INT, hash_value INT \
		)'
	c.execute(q)
	q = 'INSERT OR IGNORE INTO administrators (rowid, name, salt, hash_value) \
	VALUES (?, ?, ?, ?)'
	c.execute(q, (1, 'admin', '', sha512('').hexdigest()))
	q = 'CREATE TABLE IF NOT EXISTS students \
	( \
		id TEXT, name TEXT, salt INT, hash_value INT, \
		email TEXT, dob TEXT, address TEXT, phone TEXT, \
		cursched TEXT, pastscheds TEXT \
		)'
	c.execute(q)
	q = 'CREATE TABLE IF NOT EXISTS teachers \
	( \
		id TEXT, name TEXT, salt INT, hash_value INT, \
		email TEXT, dob TEXT, address TEXT, phone TEXT, \
		cursched TEXT, pastscheds TEXT \
		)'
	c.execute(q)
	q = 'CREATE TABLE IF NOT EXISTS sections \
	( \
		id TEXT, className TEXT, teacherId TEXT, pd TEXT \
		)'
	c.execute(q)

def check_login_info(username, password, table):
	'''Returns whether the database contains a user with the given information

	Checks the students, teachers, or administrators table for a user matching
	the given username and password.
	'''
	# Create the connection and cursor for the SQLite database.
	conn = connect("data.db")
	c = conn.cursor()
	# Get the salt and hash for the given user.
	q = 'SELECT salt, hash_value FROM %s WHERE name = ?' % table
	salt_n_hash = c.execute(q, (username,)).fetchone()
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