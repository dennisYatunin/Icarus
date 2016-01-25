import sqlite3
from hashlib import sha512
from uuid import uuid4

conn = sqlite3.connect('data.db')
c = conn.cursor()

"""id TEXT, email TEXT, name TEXT, salt INT, hash_value INT, \
dob TEXT, address TEXT, phone TEXT, \
cursched TEXT, pastscheds TEXT \
)'"""

def getName(studentId):
	"""take in id, return name"""
	q = "select name from students where id = (?)"
	for result in c.execute(q, (studentId,)):
		return result
print getName(1)

def getCurrSched(studentId):
    """
    Input: studentId - int of id of student
    Returns: List of course codes, in order of sched
    """
    q = "select cursched from students where id = (?)"
    for result in  c.execute(q, (studentId,)):
    	raw_sched = result[0]
    #error checkin?
    sched = raw_sched.split(";");
    if len(sched) > 1:
    	return sched 
    return -1
print getCurrSched(1)

def getCurrGrades(studentId):
    """
    Input: studentId - int of id of student
    Output: dictionary with course code keys and values are grades
    """
    sched = getCurrSched(studentId)
    if (sched == -1):
    	return {"Sched not found": "Grades not found"}
    grades = {}
    for course_code in sched:
        q = "select grade from " + course_code + " where id = (?)"
        grade = c.execute(q, (studentId))[0]
        grades[course_code] = str(grade)
    return grades
print getCurrGrades(1)

def getAddress(studentId):
    """Input: studentid -- int
    Output : String of addr
    """
    q = "select address from students where id = (?)"
    addr = ""
    for result in c.execute(q, (studentId,)):
        addr += result[0]
    return addr
print getAddress(1)

def getTranscript(studentId):
    """input int of student id
    returns dict of all the courses and corresponding grades
    """
    allGrades = getCurrGrades(studentId)#import curr year first
    if "Sched not found" in allGrades.keys():
    	return {"Transcript not found": "Grades not found"}
    q = "select pastscheds from students where id = (?)"
    for result in c.execute(q, (studentId,)):
    	oldYears = result[0].split("|")
    oldClasses = []
    for year in oldYears:
        year = year.split(";")
        for section in year:
            oldClasses.append(section)
    for section in oldClasses:
        q = "select grade from " + course_code + " where id = (?)"
        grade = c.execute(q, (studentId))[0]
        allGrades[course_code] = grade
    return allGrades
print getTranscript(1)

def getEmail(studentId):
    """input id 
    get string email"""
    q = "select email from students where id = (?)"
    for result in c.execute(q, (studentId,)):
    	email = result[0]	
    return email
print getEmail(1)

def getAllEmails():
    """Returns a list of all emails
    for use when sending mass emails"""
    q = "select email from students"
    emailList = []
    for email in c.execute(q):
        emailList.append(email[0])
    return emailList
print getAllEmails()

def getEmailsSection(sectionId):
    q = "select students from (?) "
    classEmails = []
    for student in c.execute(q, sectionId):
        classEmails.append(getEmail(student))
    return classEmails


def getPhone(studentId):
    """input id
    get back string phone num"""
    q = "select phone from students where id = (?)"
    for result in c.execute(q, (studentId,)):
    	phone = result[0]
    return phone
print getPhone(1)   

def getAllPhones():
	"""
	return list of strings of phone numbers"""
	q = "select phone from students"
	nums = []
	for phone in c.execute(q):
		nums.append(phone[0])
	return nums
print getAllPhones()


    
    
