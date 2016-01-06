import sqlite3

print("HALLOA! Welcome to the Icarus initialization stuffs. Please answer some questions for us.")
maxcourses = int(input('How many periods are there in a day? '))
nummesters = int(input('Do you have 2 mesters (semester system) or 3 mesters (trimester system) or something else? '))

conn = sqlite3.connect('data.db')

# add student stuffs
c = conn.cursor()
q = 'CREATE TABLE students \
	(id TEXT, username TEXT, offname TEXT, salt INT, hash_value INT, address TEXT, email TEXT)'