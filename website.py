# author Guowei Li
# display the new student grades prettytable from HW11 as a web page
from flask import Flask, render_template
from typing import Dict, List
import os
import sqlite3

app: Flask = Flask(__name__,template_folder=os.getcwd())# change the template folder to the same defult folder with the python program

DB_FILE: str = os.path.join(os.getcwd(),"HW11_Guowei_Li.bd")

@app.route('/students')
def student_summary() -> str:
    query: str = """select students.Name, students.CWID, Course, Grade, instructors.Name 
                    from students join grades on students.CWID = grades.StudentCWID join instructors on grades.InstructorCWID = instructors.CWID 
                    order by students.Name""" #this is the query
    db: sqlite3.Connection = sqlite3.connect(DB_FILE) # connect to the database

    #get the query reults and tranfer into a list
    data: Dict[str, str] = [
        {'student': student,
        'cwid': cwid,
        'course': course,
        'grade': grade,
        'instructor': instuctor} for student, cwid, course, grade, instuctor in db.execute(query)]
    db.close() #close the connection

    return render_template('student_summary.html',
                            title = 'Stevens Repository',
                            table_title = 'Student Summary',
                            comment = 'Created by Guowei Li',
                            students = data)

app.run(debug = True)