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


#when importing data, csv is same as query, in order EXCEPT
#salt, hash, permissions, and schedule fields are omitted
#teacher csv is the same
#we need more parent info (ie name??)
#made parent data same as student (2 parents two diff addresses possibly)
#with the exception of an inserted id right after their own, its their child id
#prolly need list of child ids
#unless we institute a one child policy??
#i don't think we have that power

#and we didnt get to sections yet to *shrug*

