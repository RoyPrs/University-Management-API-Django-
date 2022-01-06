from typing import Text
from django.test import TestCase
from course_management import models
from user_management.models import User


class CourseTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.student = User.members.create(
            username="teststudent", password="testpassword"
        )
        instructor = User.members.create(
            username="testinstructor", password="testpassword"
        )
        course = models.Course.objects.create(name="Linear Control", credit=3)
        term = models.Term.objects.create(season=4, start_date="2021-12-12")
        cls.section = models.CourseSection.objects.create(
            course=course,
            term=term,
            total_capacity=45,
            instructor=instructor,
            first_session_weekday="Monday",
            second_session_weekday="Tueseday",
            hour_schedule="10-12",
            exam_date="2021-11-15",
        )

    def test_complain_model(self):
        testcomplain = models.Complain.objects.create(
            student=self.student, section=self.section, text="Hi teacher"
        )
        self.assertEqual(testcomplain.__str__(), "teststudent Linear Control")
