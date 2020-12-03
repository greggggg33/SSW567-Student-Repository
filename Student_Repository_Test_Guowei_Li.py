# author: Guowei Li
import os, unittest
from typing import Tuple, List, Iterator, Dict, DefaultDict
from prettytable import PrettyTable
from Student_Repository_Guowei_Li import student,instructor,repository

class studentTest(unittest.TestCase):
    def test_student(self) -> None:
        guowei = student('123','Guwoei Li','SSW')
        guowei.addCourseGrade("SSW810","A")
        self.assertEqual(guowei.cwid, '123')
        self.assertEqual(guowei.name, 'Guwoei Li')
        self.assertEqual(guowei.major, 'SSW')
        self.assertEqual(guowei.summary["SSW810"],"A")
        guowei.addCourseGrade("SSW 540","A")
        self.assertEqual(guowei.completedCourse,['SSW 540', 'SSW810'])
    
class instructorTest(unittest.TestCase):
    def test_instructor(self) -> None:
        guowei = instructor('123','Guowei Li','SSW')
        guowei.addStduent("SSW810")
        self.assertEqual(guowei.cwid, '123')
        self.assertEqual(guowei.name, 'Guowei Li')
        self.assertEqual(guowei.department, 'SSW')
        self.assertEqual(guowei.summary["SSW810"],1)
        guowei.addStduent("SSW810")
        self.assertEqual(guowei.summary["SSW810"],2)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit = False)