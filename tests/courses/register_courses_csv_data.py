import pytest
import time
import unittest

from ddt import ddt, data, unpack

from pages.courses.register_courses_page import RegisterCoursesPage
from pages.home.navigation_page import NavigationPage
from utilities.read_data import getCSVData
from utilities.teststatus import TestStatus


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class RegisterCoursesCSVDataTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self):
        self.courses = RegisterCoursesPage(self.driver)
        self.ts = TestStatus(self.driver)
        self.nav = NavigationPage(self.driver)

    def setUp(self):
        time.sleep(3)
        self.nav.navigateToAllCourses()

    @pytest.mark.run(order=1)
    @data(*getCSVData("AutomationFramework\\testdata.csv"))
    @unpack
    def test_invalidEnrollment(self, courseName, ccNum, ccExp, ccCVV):
        self.courses.enterCourseName(courseName)
        self.courses.clickOnSearchButton()
        res = self.courses.selectCourseToEnroll(courseName)
        self.ts.mark(res, "Search Course Verification")
        self.courses.enrollCourse(num=ccNum, exp=ccExp, cvv=ccCVV)
        # result = self.courses.verifyEnrollFailed()
        time.sleep(3)
        self.courses.clickOnIcon()
        self.ts.markFinal("test_invalidEnrollment", res, "Enrollment Failed Verification")


