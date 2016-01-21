from os import urandom
from hashlib import sha512
from uuid import uuid4
from sqlite3 import connect

def get_secret_key():
	'''Returns a key that may be used to secure a Flask session

	The key is a 32-character string generated with the os.urandom function.
	'''
	return urandom(32)

def initialize_accounts():
	# Create the connection and cursor for the SQLite database.
	conn = connect("data.db")
	c = conn.cursor()
	q = 'CREATE TABLE IF NOT EXISTS students \
	(user_id INT, username TEXT, salt INT, hash_value INT, email TEXT)'
	c.execute(q)

def check_login_info(username, password, table):
	'''Returns whether the accounts database contains a user with the given information

	'''
	# Create the connection and cursor for the SQLite database.
	conn = connect("data.db")
	c = conn.cursor()
	# Get the salt and hash for the given user.
	q = 'SELECT salt, hash_value FROM ? WHERE username = ?'
	salt_n_hash = c.execute(q, (table, username)).fetchone()
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