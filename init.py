import sqlite3
from os import urandom
from hashlib import sha512
from uuid import uuid4
from re import search
from time import gmtime, strftime

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


q = 'CREATE TABLE faculty \
	( \
		id TEXT, email TEXT, name TEXT, salt INT, hash_value INT, permissions INT\
		dob TEXT, address TEXT, city TEXT, zip TEXT, phone TEXT, \
		cursched TEXT, pastscheds TEXT \
		)'
c.execute(q)

q = 'CREATE TABLE sections \
	( \
		id TEXT, className TEXT, teacherId TEXT, pd TEXT \
		)'
c.execute(q)

studentArray = []
students = open('data/students.csv').readlines()
for line in students:
	line = line.split(',')
        password = line[0]
        # Create a random salt to add to the hash.
        salt = uuid4().hex
        # Create a hash, and use string concatenation to make the hash function slow
        # for added security.
        hash_value = sha512((password + salt) * 10000).hexdigest()
        line.insert(3, salt)
        line.insert(4, hash_value)
        line = tuple(line)
        #print"printing line: "
        #print line 
        studentArray.append(line)
        
c.executemany('INSERT INTO students (id, email, name, salt, hash_value, dob, address, city, zip, phone, cursched, pastscheds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', studentArray  )

q = "Select * from students"
#for row in c.execute(q):
        #print "Entered Student:"
        #print row


facultyArray = []
faculty = open('data/faculty.csv').readlines()
for line in faculty:
	line = line.split(',')
        password = line[0]
        # Create a random salt to add to the hash.
        salt = uuid4().hex
        # Create a hash, and use string concatenation to make the hash function slow
        # for added security.
        hash_value = sha512((password + salt) * 10000).hexdigest()
        line.insert(3, salt)
        line.insert(4, hash_value)
        line = tuple(line)
        #print line
        facultyArray.append(line)
        
c.executemany('INSERT INTO faculty (id, email, name, permissions, salt, hash_value, address, city, zip, phone, cursched, pastscheds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', facultyArray  )
print "entered the faculty"

q = "Select * from faculty"
#for row in c.execute(q):
        #print "Entered faculty:"
        #print row



##now for the sections
#plan: one sectino table lists section name and metadata (teacher, numCredits, grades open, prereqs, etc)
#
sectionArray = []
sections = open("data/sections.csv").readlines()
for line in sections:
        line = line.split(',')
        q = "create table " + line[0] + " (studentid, attendence, grade)"
        c.execute(q)
        sectionArray.append(line)

c.executemany('Insert into sections(id, classname, teacherId, pd) Values (?, ?, ?, ?)', sectionArray)
q = "select * from sections"
for row in c.execute(q):
        print row

q = "select name from sqlite_master where type = 'table'"
for result in c.execute(q):
        print result

##now populate the secions databae using the students data



#open('../data/parents.csv')
#open('../data/faculty.csv')


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

