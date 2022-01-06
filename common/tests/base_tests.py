# -*- coding: utf-8 -*-
#
# parnia/common/tests/base_tests.py
#

import json

from django.contrib.auth import get_user_model, models
from django.test import TestCase



UserModel = get_user_model()


# class BaseTest(RecordCreation, TestCase):
class BaseTest(TestCase):
    _TEST_USERNAME = 'BaseTestUser'
    _TEST_PASSWORD = 'TestPassword_007'
    _TEST_GROUP = 'TestGroup'

    def __init__(self, name):
        super().__init__(name)
        self.user = None

    def setUp(self):
        self.user = self._create_user()

    # def _create_user(self, username=_TEST_USERNAME, email=None,
    #                  password=_TEST_PASSWORD, is_superuser=True,
    #                  role=UserModel.DEFAULT_USER):
    def _create_user(self, username=_TEST_USERNAME, email=None,
                     password=_TEST_PASSWORD, is_superuser=True):
        # user = UserModel.members.create_user(username=username,
        #                                      password=password, role=role)
        user = UserModel.members.create_user(username=username,
                                             password=password)
        user.first_name = "Test"
        user.last_name = "User"
        user.is_active = True
        user.is_staff = True
        user.is_superuser = is_superuser
        user.save()
        return user
    
    def _create_group(self, name=_TEST_GROUP):
        group = models.group.objects.create(name=name)
        return group

    def _has_error(self, response, message=None):
        result = False

        if hasattr(response, 'context_data'):
            if response.context_data.get('form').errors:
                result = True
        elif hasattr(response, '__str__'):
            if message in str(response):
                result = True

        return result
