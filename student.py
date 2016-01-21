import sqlite3
from hashlib import sha512
from uuid import uuid4

conn = sqlite.connect('data.db')
c = conn.cursor()

"""id TEXT, email TEXT, name TEXT, salt INT, hash_value INT, \
dob TEXT, address TEXT, city TEXT, zip TEXT, phone TEXT, \
cursched TEXT, pastscheds TEXT \
)'"""

def getCurrSched(studentId):
    """
    Input: studentId - int of id of student
    Returns: List of course codes, in order of sched
    """
    q = "select cursched from students where id = (?)"
    raw_sched = c.execute(q, (studentId))[0];
    #error checkin?
    sched = raw_sched.split(";");
    return sched

def getCurrGrades(studentId):
    """
    Input: studentId - int of id of student
    Output: dictionary with course code keys and values are grades
    """
    sched = getCurrSched(studentId)
    grades = {}
    for course_code in sched:
        q = "select grade from " + course_code + " where studentid = (?)"
        grade = c.execute(q, (studentId))[0]
        grades[course_code] = grade
    return grades

def getAddress(studentId):
    """Input: studentid -- int
    Output : String of addr
    """
    q = "select address, city, zip from students where id = (?)"
    addr = ""
    for result in c.execute(q, studentId):
        addr += result
    return addr


def getTranscript(studentId):
    """input int of student id
    returns dict of all the courses and corresponding grades
    """
    allGrades = getCurrGrades(studentId)#import curr year first
    q = "select pastsched from students where id = (?)"
    oldYears = c.execute(q, (studentId))[0].split("|")
    oldClasses = []
    for year in oldYears:
        year = year.split(";")
        for section in year:
            oldClasses.append(section)
    for section in oldClasses:
        q = "select grade from " + course_code + " where studentid = (?)"
        grade = c.execute(q, (studentId))[0]
        allGrades[course_code] = grade
    return allGrades


                
    
    
    
