import sqlite3
from hashlib import sha512
from uuid import uuid4

conn = sqlite.connect('data.db')
c = conn.cursor()

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
