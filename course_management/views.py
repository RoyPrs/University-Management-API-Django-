# -*- coding: utf-8 -*-
#
# parnia/course_management/views.py
#
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from functools import reduce
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import CharField

# from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_condition import C, And, Or, Not
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from common.view_mixins import (
    TrapDjangoValidationErrorCreateMixin,
    TrapDjangoValidationErrorUpdateMixin,
)
from common.permissions import (
    IsAdminSuperUser,
    IsAdministrator,
    IsReadOnly,
    IsUserActive,
    CanDelete,
    IsStudent,
    IsInstructor,
    IsStaff,
    IsOwner,
)

from course_management import serializers, models


UserModel = get_user_model()


def get_user(request):
    user = None
    if hasattr(request, "user"):
        user = request.user
    return user


# ------------------------------Course------------------------------


class CourseListCreate(
    TrapDjangoValidationErrorCreateMixin, generics.ListCreateAPIView
):
    serializer_class = serializers.CourseSerializer

    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsStaff, IsReadOnly),
        ),
    )

    def get_queryset(self):
        queryset = models.Course.objects.all()

        name = self.request.query_params.get("name")
        if name is not None:
            queryset = queryset.filter(name=name)

        prerequesits_string = self.request.query_params.get("prerequesits")
        if prerequesits_string is not None:
            prerequesits_list = prerequesits_string.split(sep=",")
            queryset_list = [
                models.Course.objects.filter(prerequesits__name__iexact=pre)
                for pre in prerequesits_list
            ]
            queryset = reduce(lambda x, y: x & y, queryset_list)
        return queryset

    lookup_field = "public_id"

    def create(self, request, *args, **kwargs):
        # If the input data is a list, set many=True
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


course_list = CourseListCreate.as_view()


class CourseRetrieveUpdateDestroy(
    TrapDjangoValidationErrorUpdateMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsStaff, IsReadOnly),
        ),
    )
    lookup_field = "public_id"


course_detail = CourseRetrieveUpdateDestroy.as_view()

# ------------------------------Term------------------------------


class TermListCreate(
    TrapDjangoValidationErrorCreateMixin, generics.ListCreateAPIView
):
    queryset = models.Term.objects.all()
    serializer_class = serializers.TermSerializer
    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsStaff, IsReadOnly),
        ),
    )
    lookup_field = "public_id"

    def create(self, request, *args, **kwargs):
        # If the input data is a list, set many=True
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


term_list = TermListCreate.as_view()


class TermRetrieveUpdateDestroy(
    TrapDjangoValidationErrorUpdateMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = models.Term.objects.all()
    serializer_class = serializers.TermSerializer
    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsStaff, IsReadOnly),
        ),
    )
    lookup_field = "public_id"


term_detail = TermRetrieveUpdateDestroy.as_view()

# ------------------------------Course Section------------------------------


class CourseSectionListCreate(
    TrapDjangoValidationErrorCreateMixin, generics.ListCreateAPIView
):
    queryset = models.CourseSection.objects.all()
    serializer_class = serializers.CourseSectionSerializer
    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsStaff, IsReadOnly),
        ),
    )

    def create(self, request, *args, **kwargs):
        # If the input data is a list, set many=True
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = models.CourseSection.objects.all()

        instructor = self.request.query_params.get("instructor")
        term = self.request.query_params.get("term")
        if instructor is not None:
            if term is not None:
                queryset = queryset.filter(instructor=instructor, term=term)
            else:
                queryset = queryset.filter(instructor=instructor)
        return queryset

    lookup_field = "public_id"


coursesection_list = CourseSectionListCreate.as_view()


class CourseSectionRetrieveUpdateDestroy(
    TrapDjangoValidationErrorUpdateMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = models.CourseSection.objects.all()
    serializer_class = serializers.CourseSectionSerializer
    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsStaff, IsReadOnly),
        ),
    )
    lookup_field = "public_id"


coursesection_detail = CourseSectionRetrieveUpdateDestroy.as_view()

# ------------------------------Course Log------------------------------


class CourseLogListCreate(
    TrapDjangoValidationErrorCreateMixin, generics.ListCreateAPIView
):
    queryset = models.CourseLog.objects.all()
    serializer_class = serializers.CourseLogSerializer
    filter_backends = [filters.SearchFilter]
    # search_fields = ['section__instructor', 'section__term']
    filterset_fields = ["section"]
    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(
                IsAdminSuperUser,
                IsAdministrator,
                IsReadOnly,
                IsStudent,
                IsStaff,
            ),
        ),
    )
    lookup_field = "public_id"

    def create(self, request, *args, **kwargs):
        data = request.data
        student = request.user
        many = isinstance(data, list)
        print("many= ", many)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save(student=student)
        # self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     # Do some validation here
    #     serializer.save()


courselog_list = CourseLogListCreate.as_view()


class CourseLogRetrieveUpdateDestroy(
    TrapDjangoValidationErrorUpdateMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = models.CourseLog.objects.all()
    serializer_class = serializers.CourseLogSerializer
    # permission_classes = (
    #     And(
    #         IsUserActive,
    #         IsAuthenticated,
    #         Or(
    #             IsOwner,
    #             IsAdminSuperUser,
    #             IsAdministrator,
    #             # IsReadOnly,
    #             #    IsInstructor
    #         ),
    #     ),
    # )
    permission_classes = [IsOwner]
    #     (IsUserActive & IsAuthenticated)
    #     | IsOwner
    #     | IsAdminSuperUser
    #     | IsAdministrator
    # ]

    def retrieve(self, request, public_id):

        instance = self.get_object()
        self.check_object_permissions(self.request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # def get(self, request, public_id, **kwargs):
    #     return self.retrieve(request, public_id)

    lookup_field = "public_id"


courselog_detail = CourseLogRetrieveUpdateDestroy.as_view()


class CourseLogBulkUpdate(
    TrapDjangoValidationErrorUpdateMixin, generics.UpdateAPIView
):
    """This endpoint is typically used by instructors to enter the grades."""

    queryset = models.CourseLog.objects.all()
    serializer_class = serializers.CourseLogSerializer
    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(
                IsAdminSuperUser,
                IsAdministrator,
                IsReadOnly,
                #    IsInstructor
            ),
        ),
    )
    lookup_field = "public_id"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        data = request.data
        public_ids = [item.get("public_id", None) for item in data]
        # instance = self.get_object()
        linstances = list(self.get_queryset().filter(public_id__in=public_ids))
        # instances = [get_object_or_404(self.get_queryset(), {'public_id': public_id}) for public_id in public_ids]
        serializer = self.get_serializer(
            linstances, data=data, partial=partial, many=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


courselog_update = CourseLogBulkUpdate.as_view()


# ------------------------------Complain------------------------------
class ComplainCreate(
    TrapDjangoValidationErrorCreateMixin, generics.CreateAPIView
):
    queryset = models.Complain.objects.all()
    serializer_class = serializers.ComplainSerializer
    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsReadOnly),
        ),
    )
    lookup_field = "public_id"


complain_create = ComplainCreate.as_view()


class ComplainList(generics.ListAPIView):
    queryset = models.Complain.objects.all()
    serializer_class = serializers.ComplainSerializer
    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsInstructor),
        ),
    )
    lookup_field = "public_id"

    def get_queryset(self):
        queryset = None
        instructor = self.request.user
        section = self.kwargs["section"]
        if instructor and section:
            queryset = models.Complain.objects.filter(
                section=section, section__instructor=instructor
            )
            queryset.toggle_status(status="Seen")
        return queryset


complain_list = ComplainList.as_view()


class ComplainRetrieveUpdateDestroy(
    TrapDjangoValidationErrorUpdateMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = models.Complain.objects.all()
    serializer_class = serializers.ComplainSerializer
    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(IsAdminSuperUser, IsAdministrator, IsReadOnly),
        ),
    )
    lookup_field = "public_id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instructor = self.request.user
        if "Instructor" in instructor.get_group():
            instance.update(status="Seen")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self):
        super.get_object()


complain_detail = ComplainRetrieveUpdateDestroy.as_view()

# -------------------------------Draft-------------------------------
# from user_management.models import User


@api_view(["GET", "POST"])
def test(request, *args, **kwargs):
    # to get all sections of a term
    if request.method == "GET":
        # data = User.students.all().values()
        print("in the view")
        print("data= ", request.data)
        return Response({"name": request.data})

    # cs = models.CourseLog.objects.get(public_id= public_id)
    # return Response({"res": "hallo"})


# A third common method is save() method which lets us customize how a model is saved.
# A common example is for a blog app that needs to automatically set the author of a blog pos
# t to the current logged-in user. You'd implement that functionality with save().
# To be applied for the view in which the instructor enters the grades.
# The name of the instructor should be extracted from the request.
