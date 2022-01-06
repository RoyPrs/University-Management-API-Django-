# -*- coding: utf-8 -*-
#
# parnia/course_management/admin.py
#
"""
Admin.
"""
from django.contrib import admin
from course_management.models import (
    Course,
    Term,
    CourseSection,
    CourseLog,
    Complain,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "pk", "get_prerequesits")


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("name", "get_classes", "public_id")


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ("course", "local_id", "pk", "instructor")


# To add "update" action to CourseLog in the admin panel
@admin.register(CourseLog)
class CourseLogAdmin(admin.ModelAdmin):
    list_display = ("student", "section", "final_grade", "status")
    actions = ["make_approved"]

    def make_approved(self, request, queryset):
        updated = queryset.filter(status="Not Approved").update(
            status="Approved"
        )

    make_approved.short_description = "Approve the final grades"


@admin.register(Complain)
class ComplainAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "section",
        "status",
    )


# The Django admin site documentation (Page 731)
# AN export function that uses Django’s serialization functions to dump some selected objects as JSON
# Note! Django's serialization, not DRF's ;-)
# from django.core import serializers
# from django.http import HttpResponse
# def export_as_json(modeladmin, request, queryset):
#     response = HttpResponse(content_type="application/json")
#     serializers.serialize("json", queryset, stream=response)
#     return response
# p736
# from django.contrib.contenttypes.models import ContentType
# from django.http import HttpResponseRedirect
# def export_selected_objects(modeladmin, request, queryset):
#     selected = queryset.values_list('pk', flat=True)
#     ct = ContentType.objects.get_for_model(queryset.model)
#     return HttpResponseRedirect('/export/?ct=%s&ids=%s' % (ct.pk,','.join(str(pk) for pk in selected),))

# Do we need ModelAdmin at all?
# If you are happy with the default admin interface, you don’t need
# to define a ModelAdmin object at all – you can register the model class
# without providing a ModelAdmin description;
# admin.site.register(Author)
