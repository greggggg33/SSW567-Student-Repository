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
        self.majorList: Dict[str, Dict[str,List[str]]] = dict() #includes all the courses that in a major
        gpaDic: Dict[str,int] = {'A':4.0,'A-':3.75,'B+':3.25,'B':3.0,'B-':2.75,'C+':2.25,'C':2.0,'C-':0,'D+':0,'D':0,'D-':0,'F':0} # GPA mapping
        ptm: PrettyTable = PrettyTable(field_names= ["Major","Required Courses","Electives"]) # initialize a prettytable for majors
        pts: PrettyTable = PrettyTable(field_names = ["CWID","Name","major","Completed Course","Remaining Required","Remaining Electives","GPA"]) # initialize a prettytable for students
        pti: PrettyTable = PrettyTable(field_names = ["CWID","Name","Dept","Course","Students"]) # initialize a prettytable for instuctors

        """stores all the courses requirement in different majors"""
        fp = self.file_reader(os.path.join(self.dirpath,'majors.txt'),3,'\t',True)
        for i in fp:
            if i[0] not in self.majorList:
                self.majorList[i[0]] = {"Required": [],"Electives": []}
        fp = self.file_reader(os.path.join(self.dirpath,'majors.txt'),3,'\t',True)
        for i in fp:
            if i[1] == 'R':
                self.majorList[i[0]]["Required"].append(i[2])
            else:
                self.majorList[i[0]]["Electives"].append(i[2])

        """store all the students"""
        fp = self.file_reader(os.path.join(self.dirpath,'students.txt'),3,';',True)
        for i in fp:
            self.studentList.append(student(i[0],i[1],i[2]))# Read the students.txt file, creating a new instance of class Student for each line in the file, and add the new Student to the repository's container with all students.
        """store all the instructors"""
        fp = self.file_reader(os.path.join(self.dirpath,'instructors.txt'),3,'|',True)
        for i in fp:
            self.instructorList.append(instructor(i[0],i[1],i[2])) # Read the instructors.txt file, creating a new instance of class Instructor for each line in the file, and add the new Instructor to the repository's container with all Instructors.
        
        """"store all the grades"""
        fp = self.file_reader(os.path.join(self.dirpath,'grades.txt'),4,'|',True)
        for i in fp:
            for s in self.studentList:
                if i[0] == s.cwid:
                    s.addCourseGrade(i[1],i[2]) # Use the student cwid, course, and grade and ask the instance of class Student associated the student cwid to add the grade to the student information
        fp = self.file_reader(os.path.join(self.dirpath,'grades.txt'),4,'|',True)
        for i in fp:
            for s in self.instructorList:
                if i[3] == s.cwid:
                    s.addStduent(i[1]) # Use the instructor cwid and course to ask the instance of class Instructor to note that the instructor taught another student in the specific course
        
        """set up the pretty tables"""
        for i in self.majorList.keys():
            ptm.add_row([i, self.majorList[i]["Required"], self.majorList[i]["Electives"]]) # add row for courses that needed for the major
        for i in self.studentList:
            gpaList: List[int] = [] # a list that have all the compeleted course gpa value for a single student
            gpaAve: int = 0 # an average gpa value for a single student
            for j in i.summary.keys():
                try:
                    gpaList.append(gpaDic[i.summary[j]])
                    gpaAve = round((sum(gpaList)/len(gpaList)),2) # calculate the average gpa
                except ValueError:
                    print("there is something wrong with student's grade")
                if i.summary[j] in ['C-','D+','D','D-','F']:
                    i.completedCourse.remove(j) # Any student earning less than a 'C' must repeat the course until earning at least a 'C'.
            remaningR: List[str] = [k for k in self.majorList[i.major]["Required"] if k not in i.completedCourse] #a list that shows remaining required courses
            remaningE: List[str] = [] # a list that shows remaining electives
            if [k for k in i.completedCourse if k in self.majorList[i.major]["Electives"]] == []:
                remaningE = self.majorList[i.major]["Electives"] # student only need on electives to graduate
            pts.add_row([i.cwid, i.name, i.major, i.completedCourse, remaningR, remaningE, gpaAve]) # add row for each students in the repository
        for i in self.instructorList:
            for c in i.summary.keys():
                pti.add_row([i.cwid,i.name,i.department, c,i.summary[c]])# add row for each instructor in the repository and each instructor might have more than one course teaching
        print("Majors Summary")
        print(ptm) # print a major prettytable
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
    """please change the path at the main other wise the system wont work"""
    path = os.getcwd()
    path2 = 'Stevens'
    path = os.path.join(path,path2)
    repository(path)

if __name__ == "__main__":
    main()