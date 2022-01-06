from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from requests.auth import HTTPBasicAuth

from course_management import models
from user_management.models import User


class CourseViewTest(APITestCase):
    """Tests to verify that the course views work as per expectations."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.client = APIClient()
        cls.client.login(username="roya", password="royapassword")
        cls.url = reverse("course-list")
        cls.user = User.members.create(
            username="roya", password="testpassword", is_superuser=True
        )
        cls.token = Token.objects.create(user=cls.user)

    def test_post_course(self):
        data_dict = {"name": "testcourse1", "credit": 3}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.url, data_dict)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_repeated_course_name(self):
        data_dict1 = {"name": "testcourse2", "credit": 3}
        data_dict2 = {"name": "testcourse2", "credit": 3}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.url, data_dict1)
        response = self.client.post(self.url, data_dict2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_credit(self):
        data_dict = {"name": "testcourse4", "credit": 6}
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.url, data_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
