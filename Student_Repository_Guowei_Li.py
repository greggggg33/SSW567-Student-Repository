# author: Guowei Li
import os
from typing import Tuple, List, Iterator, Dict, DefaultDict
from prettytable import PrettyTable

class student:
    """class student that stores information for a single student"""
    def __init__(self, cwid: str, name: str, major: str) -> None:
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.summary: Dict[str, str] = dict() #summary contains a course as a key and its grade as value
        self.completedCourse: List[str] = [] #store courses that has a grade
    
    def addCourseGrade(self, course:str, grade: str) -> None:
        """add one course and its grade"""
        self.summary[course] = grade
        self.completedCourse.append(course)
        self.completedCourse = sorted(self.completedCourse)# sort in alpabetical order

class instructor:
    """class student that stores information for a single instructor"""
    def __init__(self, cwid: str, name: str, department: str) -> None:
        self.cwid: str = cwid
        self.name: str = name
        self.department: str = department
        self.summary: Dict[str, int] = dict() # summary contains a course and how many students in this course

    def addStduent(self, course: str) -> None:
        """add one student to its course"""
        if course in self.summary.keys():
            self.summary[course] += 1
        else:
            self.summary[course] = 1

class repository:
    def __init__(self,dirpath: str) -> None:
        """holds all of the data for a specific organization"""
        self.dirpath = dirpath
        self.studentList: List[str] = [] # Includes a container for all students
        self.instructorList: List[str] = [] # Includes a container for all instructors
        pts: PrettyTable = PrettyTable(field_names = ["CWID", "Name","major","Completed Course"]) # initialize a prettytable for students
        pti: PrettyTable = PrettyTable(field_names = ["CWID","Name","Dept","Course","Students"]) # initialize a prettytable for instuctors

        fp = self.file_reader(os.path.join(self.dirpath,'students.txt'),3,'\t',False)
        for i in fp:
            self.studentList.append(student(i[0],i[1],i[2]))# Read the students.txt file, creating a new instance of class Student for each line in the file, and add the new Student to the repository's container with all students.
        fp = self.file_reader(os.path.join(self.dirpath,'instructors.txt'),3,'\t',False)
        for i in fp:
            self.instructorList.append(instructor(i[0],i[1],i[2])) # Read the instructors.txt file, creating a new instance of class Instructor for each line in the file, and add the new Instructor to the repository's container with all Instructors.
        fp = self.file_reader(os.path.join(self.dirpath,'grades.txt'),4,'\t',False)
        for i in fp:
            for s in self.studentList:
                if i[0] == s.cwid:
                    s.addCourseGrade(i[1],i[2]) # Use the student cwid, course, and grade and ask the instance of class Student associated the student cwid to add the grade to the student information
        fp = self.file_reader(os.path.join(self.dirpath,'grades.txt'),4,'\t',False)
        for i in fp:
            for s in self.instructorList:
                if i[3] == s.cwid:
                    s.addStduent(i[1]) # Use the instructor cwid and course to ask the instance of class Instructor to note that the instructor taught another student in the specific course
                
        for i in self.studentList:
            pts.add_row([i.cwid, i.name, i.major, i.completedCourse]) # add row for each students in the repository
        for i in self.instructorList:
            for c in i.summary.keys():
                pti.add_row([i.cwid,i.name,i.department, c,i.summary[c]])# add row for each instructor in the repository and each instructor might have more than one course teaching
        print("Student Summary")
        print(pts) # print a student prettytable
        print("Instructor Summary")
        print(pti) # print an instructor prettytable

    def file_reader(self, path: str, field: int, sep: str, header: bool) -> Iterator[List[str]]:
        """THis functino a file reading helper that read every line in the file and seperate by the sep"""
        """if the header if True ignore the first row of the file"""
        """This is the file reader funciton in HW08"""
        try:
            fp = open(path, 'r')
        except FileNotFoundError:
            print("Can't open", path)# raise an error if the file can not open 
        else:
            with fp:
                lines = fp.readlines()
                counter = 0 # a counter that shows which line is being reading
                if header == True:
                    counter += 1
                else:
                    counter = 0
                while counter < len(lines):
                    line  = lines[counter].strip().split(sep)# seperate the line by sep
                    if len(line) != field:
                        raise ValueError(f"the fileds of line {counter} in {path} is not equal to {field}") # show which line has different field
                    counter += 1
                    yield line

def main():
    path = os.getcwd()
    path2 = 'Stevens'
    path = os.path.join(path,path2)
    repository(path)

if __name__ == "__main__":
    main()