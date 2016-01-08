import sqlite3

print("HALLOA! Welcome to the Icarus initialization stuffs. Please answer some questions for us.")
maxcourses = int(raw_input('How many periods are there in a day? '))
nummesters = int(raw_input('Do you have 2 mesters (semester system) or 3 mesters (trimester system) or something else? '))

conn = sqlite3.connect('data.db')
# NEED TO FIX ADDRESSES

c = conn.cursor()
q = 'CREATE TABLE students \
	( \
		id TEXT, email TEXT, name TEXT, salt INT, hash_value INT, \
		dob TEXT, address TEXT, city TEXT, zip TEXT, phone TEXT, \
		cursched TEXT, pastscheds TEXT \
		)'
c.execute(q)

q = 'CREATE TABLE parents \
	( \
		id TEXT, email TEXT, name TEXT, salt INT, hash_value INT, \
		studids TEXT, address TEXT, city TEXT, zip TEXT, phone TEXT \
		)'
c.execute(q)

q = 'CREATE TABLE facutly \
	( \
		id TEXT, email TEXT, name TEXT, salt INT, hash_value INT, permissions INT\
		dob TEXT, address TEXT, city TEXT, zip TEXT, phone TEXT, \
		cursched TEXT, pastscheds TEXT \
		)'
c.execute(q)

q = []
students = open('../data/students.csv').readlines()
for line in students:
	line = line.split(',')
	q.append('INSERT ')

q = ['INSERT INTO students (id, email, name, salt, hash_value, dob, address, city, zip, phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' % (line.split(',')[0], line.split(',')[1], line.split(',')[2], line.split(',')[3]) for line in open('../data/students.csv', 'r').readlines()]
open('../data/parents.csv')
open('../data/faculty.csv')


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

