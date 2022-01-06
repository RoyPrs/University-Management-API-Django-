from django.test import TestCase
from course_management import models


class CourseTestCase(TestCase):
    def setUp(self):
        models.Course.objects.create(name="Linear Control", credit=3)
        models.Course.objects.create(name="Signals&Systems", credit=3)

    def test_course_model(self):
        control = models.Course.objects.get(name="Linear Control")
        signal = models.Course.objects.get(name="Signals&Systems")
        self.assertEqual(control.__str__(), "Linear Control")
        self.assertEqual(signal.__str__(), "Signals&Systems")
