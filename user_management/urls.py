# -*- coding: utf-8 -*-
#
# parnia/user_management/urls.py
#
"""
User_management API URLs
"""

__docformat__ = "restructuredtext en"

from django.urls import re_path, path

from rest_framework.authtoken import views as tview

from user_management import views


urlpatterns = [
    re_path(r"user/$", views.user_list, name="user-list"),
    re_path(
        r"user/(?P<public_id>[-\w]+)/$", views.user_detail, name="user-detail"
    ),
    re_path(r"login/$", views.login_view, name="login"),
    re_path(r"logout/$", views.logout_view, name="logout"),
    # To generate token
    re_path(r"token/$", tview.obtain_auth_token, name="token"),
    path("test/", views.test, name="test"),
]

# -------------------------------Draft-------------------------------
# re_path(r'groups/$', views.group_list,
#    name='group-list'),
# re_path(r'groups/(?P<pk>\d+)/$', views.group_detail,
#    name='group-detail'),
