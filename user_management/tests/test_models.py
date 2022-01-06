# -*- coding: utf-8 -*-
#
# parnia/user_management/tests/test_models.py
#
import unittest
from django.contrib.auth import get_user_model, models
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from common.tests.base_tests import BaseTest


UserModel = get_user_model()

# class BaseAccountModels(BaseTest):

#     def __init__(self, name):
#         super().__init__(name)

#     def setUp(self):
#         super(BaseAccountModels, self).setUp()
#         self.inventory_type = self._create_inventory_type()
#         self.project = self._create_project(self.inventory_type)


class TestUser(BaseTest):
    def __init__(self, name):
        super().__init__(name)

    def setUp(self):
        super().setUp()
        self.group = self._create_group()

    def test_create_superuser(self):
        """
        Test that a superuser was created.
        """
        # self.skipTest("Temporarily skipped")
        username = "TestSuperuser"
        email = "TSU@example.com"
        password = "{TSU_999}"
        user = UserModel.objects.create_superuser(username, email, password)
        # msg = (f"Username: {user.username}, email: {user.email}, "
        #        f"is_superuser: {user.is_superuser}, groups: {user.get_groups()}")
        msg = (
            f"Username: {user.username}, email: {user.email}, "
            f"is_superuser: {user.is_superuser}"
        )
        self.assertEqual(user.username, username, msg)
        self.assertEqual(user.email, email, msg)
        self.assertEqual(user.is_superuser, True, msg)
        # self.assertIn(user.get_groups(), 'Admin', msg)

    def test_create_user(self):
        """
        Test that a user was created.
        """
        # self.skipTest("Temporarily skipped")
        username = "TestCreateUser"
        email = "TCU@example.com"
        password = "{TCU_999}"
        user = UserModel.members.create_user(username, email, password)
        # msg = (f"Username: {user.username}, email: {user.email}, "
        #        f"is_superuser: {user.is_superuser}, groups: {user.get_groups()}")
        msg = (
            f"Username: {user.username}, email: {user.email}, "
            f"is_superuser: {user.is_superuser}"
        )
        self.assertEqual(user.username, username, msg)
        self.assertEqual(user.email, email, msg)
        self.assertEqual(user.is_superuser, False, msg)
        # self.assertIn(user.get_groups(), 'Student', msg)

        # No username
        with self.assertRaises(ValueError) as cm:
            user = UserModel.members.create_user("", email, password)

        # No password with email
        user = UserModel.members.create_user("SecondTestUser", email, None)
        msg = (
            f"send_email: {user.send_email}, "
            f"need_password: {user.need_password}"
        )
        self.assertTrue(user.send_email, msg)
        self.assertTrue(user.need_password, msg)

        # No password and email
        with self.assertRaises(ValueError) as cm:
            user = UserModel.members.create_user("ThirdTestUser", "", None)

    @unittest.skip("We have defactored to groups")
    def test_invalid_group(self):
        """
        Test that for invalid role.
        """
        # self.skipTest("Temporarily skipped")
        kwargs = {}
        kwargs["username"] = "TestUser_01"
        kwargs["password"] = "9876543210"
        groups = [group]

        with self.assertRaises(IntegrityError) as cm:
            user = UserModel(**kwargs)
            user.save()
            user.groups.set(groups)

        # msg = f"Found: {cm.exception}"
        # self.assertTrue("The role 999 is invalid, " in str(cm.exception), msg)

    def test_get_full_name_or_username(self):
        """
        Test that the users full name is returned or the username.
        """
        # self.skipTest("Temporarily skipped")
        # Test the full name.
        name = self.user.get_full_name_or_username()
        msg = (
            f"Username: {self.user.username}, First Name: "
            f"{self.user.first_name}, Last Name: {self.user.last_name}"
        )
        fullname = "{} {}".format(self.user.first_name, self.user.last_name)
        self.assertEqual(name, fullname, msg)
        # Test the username.
        username = "TestCreateUser"
        email = "TCU@example.com"
        password = "{TCU_999}"
        user = UserModel.objects.create_user(username, email, password)
        name = user.get_full_name_or_username()
        msg = f"name: {name}, username: {username}"
        self.assertTrue(name == username, msg)

    def test_get_full_name_reversed(self):
        """
        Test that the users name gets reversed so last name is first.
        """
        # self.skipTest("Temporarily skipped")
        name = self.user.get_full_name_reversed()
        msg = (
            f"Username: {self.user.username}, First Name: "
            f"{self.user.first_name}, Last Name: {self.user.last_name}"
        )
        reversed_name = f"{self.user.last_name}, {self.user.first_name}"
        self.assertEqual(name, reversed_name, msg)
        self.assertTrue(reversed_name == str(self.user), msg)
        # Test with no first and last names
        username = "TestCreateUser"
        email = "TCU@example.com"
        password = "{TCU_999}"
        user = UserModel.objects.create_user(username, email, password)
        name = user.get_full_name_reversed()
        msg = "name: {}, username: {}".format(name, username)
        self.assertTrue(name == username, msg)

    def test_get_absolute_url(self):
        """
        Test that the users API uri is returned.
        """
        # self.skipTest("Temporarily skipped")
        uri = self.user.get_absolute_url()
        msg = f"URI: {uri}, public_id: {self.user.public_id}"
        self.assertTrue(self.user.public_id in uri, msg)

    @unittest.skip("Because")
    def test_full_name_reversed_producer(self):
        """
        Test that the full_name_reversed_producer() method produces the
        reversed full name for the admin.
        """
        # self.skipTest("Temporarily skipped")
        name = self.user.full_name_reversed_producer()
        msg = (
            f"Username: {self.user.username}, First Name: "
            f"{self.user.first_name}, Last Name: {self.user.last_name}"
        )
        reversed_name = "{}, {}".format(
            self.user.last_name, self.user.first_name
        )
        self.assertEqual(name, reversed_name, msg)
        self.assertTrue(reversed_name == str(self.user), msg)
        # Test with no first and last names
        username = "TestCreateUser"
        email = "TCU@example.com"
        password = "{TCU_999}"
        user = UserModel.objects.create_user(username, email, password)
        name = user.full_name_reversed_producer()
        msg = f"name: {name}, username: {username}"
        self.assertTrue(name == username, msg)
