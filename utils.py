from os import urandom
from hashlib import sha512
from uuid import uuid4
from sqlite3 import connect
from random import choice, random, randint
from csv import reader

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
		id TEXT UNIQUE, name TEXT, salt INT, hash_value INT, \
		email TEXT, dob TEXT, address TEXT, phone TEXT, \
		level TEXT, cursched TEXT, pastscheds TEXT \
		)'
	c.execute(q)
	q = 'CREATE TABLE IF NOT EXISTS teachers \
	( \
		id TEXT UNIQUE, name TEXT, salt INT, hash_value INT, \
		email TEXT, dob TEXT, address TEXT, phone TEXT, \
		level TEXT, cursched TEXT, pastscheds TEXT \
		)'
	c.execute(q)
	q = 'CREATE TABLE IF NOT EXISTS sections \
	( \
		id TEXT UNIQUE, className TEXT, teacherId TEXT, pd TEXT \
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

def csvHeader(hasName, hasID, hasLevel, hasEmail, hasDOB, hasAddress, hasPhone):
	'''Creates a header for the randomly-generated csv file
	'''
	s = ''
	if hasName:
		s += 'name, '
	if hasID:
		s += 'id, '
	if hasLevel:
		s += 'level, '
	if hasEmail:
		s += 'email, '
	if hasDOB:
		s += 'dob, '
	if hasAddress:
		s += 'address, '
	if hasPhone:
		s += 'phone, '
	return s[:-2] + '\n'

'''List of global variables that are used to generate random data
'''
f = open('./static/random/firstNames.txt', 'r')
firstNames = f.read().splitlines()
f.close()
f = open('./static/random/lastNames.txt', 'r')
lastNames = f.read().splitlines()
f.close()
f = open('./static/random/streetSuffixes.txt', 'r')
streetSuffixes = f.read().splitlines()
f.close()
f = open('./static/random/cities.txt', 'r')
cities = f.read().splitlines()
f.close()
f = open('./static/random/states.txt', 'r')
states = f.read().splitlines()
f.close()
domains = ['aol.com', 'gmail.com', 'hotmail.com', \
	'mail.com' , 'mail.kz', 'yahoo.com']

def randCSV(
	numPeople, hasID, hasLevel, hasEmail, hasDOB,
	hasAddress, hasPhone, deleteEntries, probDeletion
	):
	# Name is generated by default
	s = csvHeader(True, hasID, hasLevel, hasEmail, hasDOB, hasAddress, hasPhone)
	for i in range(numPeople):
		name = [choice(firstNames), choice(lastNames)]
		s += ' '.join(name) + ', '
		if hasID:
			s += str(i) + ', '
		if hasLevel:
			level = False
			if not deleteEntries or random() > probDeletion:
				level = randint(9, 12)
				s += str(level)
			s += ', '
		if hasEmail:
			if not deleteEntries or random() > probDeletion:
				# first letter of first name and part of last name,
				# followed by random email domain
				s += name[0][0] + name[1][:randint(5, 7)] + \
					'@' + choice(domains)
			s += ', '
		if hasDOB:
			if not deleteEntries or random() > probDeletion:
				# random date between 1/1/1998 and 12/28/2001
				s += str(randint(1, 12)) + '/' + str(randint(1, 28)) + \
					'/' + (str(1989 + level) if (hasLevel and level)
						else str(randint(1998, 2001)))
			s += ', '
		if hasAddress:
			if not deleteEntries or random() > probDeletion:
				# street address, city, state, zip
				s += str(randint(1, 9999)) + ' ' + choice(lastNames) + ' ' + \
					choice(streetSuffixes) + ' ' + choice(cities) + ' ' + \
					choice(states) + ' ' + str(randint(3000, 99999))
			s += ', '
		if hasPhone:
			if not deleteEntries or random() > probDeletion:
				# random phone number such that area code doesn't start with
				# a zero, none of the middle three digits are a 9, the middle
				# three digits aren't 000, and the last 4 digits aren't identical
				n = '0000000000'
				while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
					n = str(randint(10**9, 10**10-1))
				s += n[:3] + '-' + n[3:6] + '-' + n[6:]
			s += ', '
		s = s[:-2] + '\n'
	return s[:-1]

def upload_data(
	csv, category, numColumns, idnum, level, email,
	phone, address, dob, name, fname, lname
	):
	f = open(csv, 'r')
	csvreader = reader(f)
	f.close()
	for row in reader:
		if int(numColumns) > len(row):
			return False
		n = row[int(name)] if name else \
			' '.join(row[int(i)] for i in [fname, lname] if i)
		header = csvHeader(n, idnum, level, email, dob, address, phone)
		q = 'INSERT OR REPLACE INTO %s (%s) VALUES (%s?)' % (
			category, header, header.count(',') * '?, '
			)
		c.execute(q, (n, ) + \
			tuple(row[int(i)] for i in [idnum, level, email, dob, address, phone])
			)
