# -*- coding: utf-8 -*-
#
# parnia/common/permissions.py
#
"""
Authorization permissions.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework import permissions

UserModel = get_user_model()


def get_user(request):
    user = None
    if hasattr(request, "user"):
        user = request.user
    return user


#
# User based permissions
#
class IsAdminSuperUser(permissions.BasePermission):
    """
    Allows access only to admin super users.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)
        if user and user.is_superuser:
            result = True
        print("IsAdminSuperuser:", result)
        return result


class IsAdministrator(permissions.BasePermission):
    """
    Allows access only to an administrator.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if user and hasattr(user, "groups") and "Admin" in user.get_group():
            result = True
        print("IsAdministrator:", result)
        return result


class IsStudent(permissions.BasePermission):
    """
    Allows access only to a student with a profile.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if user and hasattr(user, "groups") and "Student" in user.get_group():
            result = True
        print("IsStudent:", result)
        return result


class IsInstructor(permissions.BasePermission):
    """
    Allows access only to an instructor with a profile.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if (
            user
            and hasattr(user, "groups")
            and "Instructor" in user.get_group()
        ):
            result = True
        print("IsInstructor:", result)
        return result


class IsStaff(permissions.BasePermission):
    """
    Allows access only to a staff with a profile.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if user and hasattr(user, "groups") and "Staff" in user.get_group():
            result = True
        print("IsStaff:", result)
        return result


class IsAnyUser(permissions.BasePermission):
    """
    Allows any registered user.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)
        groups = set(Group.objects.all().values_list("name"))
        # This permission is broken
        if (
            user
            and hasattr(user, "groups")
            and (user.is_superuser or user.get_group().intersection(groups))
        ):
            result = True
        print("IsAnyuser:", result)
        return result


class IsSelf(permissions.BasePermission):
    """
    Allow users to see just their own profile
    """

    def has_permission(self, request, view):
        print("in has permission")
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        result = False
        user = get_user(request)
        print("user:", user.username)
        print("obj", obj)
        if obj == user:
            result = True
        print("IsSelf:", result)
        return result


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        result = False
        print(obj)
        if obj.student == request.user:
            result = True
        print("IsOwner:", result)
        return result


#
# Miscellaneous permissions
#


class IsReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        result = False

        if request.method in permissions.SAFE_METHODS:
            result = True
        print("IsReadonly:", result)
        return result


class IsUserActive(permissions.BasePermission):
    """
    The request is authenticated if user is active.
    """

    def has_permission(self, request, view):
        result = False
        user = get_user(request)

        if user and user.is_active:
            result = True
        print("IsActive:", result)
        return result


## class IsUserRecord(permissions.BasePermission):
##     """
##     Disallows writing to non-user-own record.
##     """

##     def has_permission(self, request, view):
##         result = False
##         user = get_user(request)
##         instance = view.get_object()

##         if user == instance:
##             result = True

##         log.debug(": %s, method: %s, user: %s, view: %s",
##                   result, request.method, user, view.__class__.__name__)
##         return result


class CanDelete(permissions.BasePermission):
    """
    Allows deletion of records.
    """

    def has_permission(self, request, view):
        result = False

        if request.method == "DELETE":
            result = True
        print("CanDelete:", result)
        return result


class IsPostOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        result = False

        if request.method == "POST":
            result = True
        print("IsPostonly:", result)
        return result
