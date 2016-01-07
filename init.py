import sqlite3

print("HALLOA! Welcome to the Icarus initialization stuffs. Please answer some questions for us.")
maxcourses = int(raw_input('How many periods are there in a day? '))
nummesters = int(raw_input('Do you have 2 mesters (semester system) or 3 mesters (trimester system) or something else? '))

conn = sqlite3.connect('data.db')
# NEED TO FIX ADDRESSES

c = conn.cursor()
q = 'CREATE TABLE students \
	( \
		id TEXT, username TEXT, offname TEXT, salt INT, hash_value INT, \
		dob TEXT, address TEXT, city TEXT, zip TEXT, email TEXT, phone TEXT, \
		cursched TEXT, pastscheds TEXT \
		)'
c.execute(q)

q = 'CREATE TABLE parents \
	( \
		id TEXT, studid TEXT \
		)'
c.execute(q)

q = 'CREATE TABLE facutly \
	( \
		id TEXT, username TEXT, offname TEXT, salt INT, hash_value INT, permissions INT\
		dob TEXT, address TEXT, city TEXT, zip TEXT, email TEXT, phone TEXT, \
		cursched TEXT, pastscheds TEXT \
		)'
c.execute(q)

keepadding = raw_input('Do you have some data to import? (y/n) ')
if keepadding == 'y':
	open('../data.csv')
