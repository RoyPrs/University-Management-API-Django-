# -*- coding: utf-8 -*-
#
# parnia/course_management/urls.py
#

from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from course_management import views

urlpatterns = [
    re_path(r"course/$", views.course_list, name="course-list"),
    re_path(
        r"course/(?P<public_id>[-\w]+)/$",
        views.course_detail,
        name="course-detail",
    ),
    re_path(r"term/$", views.term_list, name="term-list"),
    re_path(
        r"term/(?P<public_id>[-\w]+)/$", views.term_detail, name="term-detail"
    ),
    re_path(
        r"coursesection/$", views.coursesection_list, name="coursesection-list"
    ),
    re_path(
        r"coursesection/(?P<public_id>[-\w]+)/$",
        views.coursesection_detail,
        name="coursesection-detail",
    ),
    re_path(
        r"courselog/bulkupdate/$",
        views.courselog_update,
        name="courselog-bulk_update",
    ),
    re_path(r"courselog/$", views.courselog_list, name="courselog-list"),
    re_path(
        r"courselog/(?P<public_id>[-\w]+)/$",
        views.courselog_detail,
        name="courselog-detail",
    ),
    re_path(r"complain/$", views.complain_create, name="complain-create"),
    re_path(
        r"complain/(?P<section>[-\w]+)/$",
        views.complain_list,
        name="complain-list",
    ),
    re_path(
        r"complain/(?P<public_id>[-\w]+)/$",
        views.complain_detail,
        name="complain-detail",
    ),
    path("test/", views.test, kwargs={"name": "roya"}, name="test"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
