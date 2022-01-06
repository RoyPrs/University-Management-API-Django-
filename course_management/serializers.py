# -*- coding: utf-8 -*-
#
# parnia/course_management/serializers.py
#

import datetime

from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Sum


from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from common.serializer_mixin import SerializerMixin
from course_management import models


def get_user(request):
    user = None
    if hasattr(request, "user"):
        user = request.user
    return user


# ------------------------------Course Section------------------------------


class CourseSectionSerializer(SerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.CourseSection
        fields = [
            "public_id",
            "course",
            "term",
            "total_capacity",
            "local_id",
            "filled_capacity",
            "instructor",
            "first_session_weekday",
            "second_session_weekday",
            "hour_schedule",
            "exam_date",
        ]
        read_only_fields = ("public_id", "local_id")

    # def create(self, validated_data):
    #     pass
    # def update(self, instance, validated_data):
    #     pass

    def validate_instructor(self, instructor):
        if "Instructor" in instructor.get_group():
            return instructor
        msg = _(f"Invalid instructor.")
        raise serializers.ValidationError(msg)


# ------------------------------Course------------------------------


class CourseSerializer(SerializerMixin, serializers.ModelSerializer):
    sections = CourseSectionSerializer(
        many=True, read_only=True, required=False
    )

    class Meta:
        model = models.Course
        fields = [
            "id",
            "public_id",
            "name",
            "credit",
            "prerequesits",
            "sections",
        ]
        read_only_fields = ("public_id",)

    def validate_credit(self, credit):
        if not 0 < credit < 5:
            msg = _("Invalid credit. Must be an integer in the [1,4] interval")
            raise serializers.ValidationError(msg)
        return credit

    def create(self, validated_data):
        prerequesits = validated_data.pop("prerequesits", [])
        obj = super().create(validated_data)
        if prerequesits:
            obj.process_prerequesits(prerequesits)
        return obj

    def update(self, instance, validated_data):
        prerequesits = validated_data.pop("prerequesits", [])
        super().update(instance, validated_data)

        if prerequesits:
            instance.process_prerequesits(prerequesits)
        return instance


# ------------------------------Term------------------------------
class TermSerializer(SerializerMixin, serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    season = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = models.Term
        fields = ["public_id", "name", "season", "start_date", "get_classes"]
        read_only_fields = ("public_id",)
        validators = [
            UniqueTogetherValidator(
                queryset=models.Term.objects.all(),
                fields=["season", "start_date"],
            )
        ]

    def get_name(self, obj):
        return obj.get_name()

    # def create(self, validated_data):
    #     pass
    # def update(self, instance, validated_data):
    #     pass

    def validate_season(self, season):
        if season not in self.Meta.model.SEASON_MAP_REV:
            msg = _(
                f"Invalid season, must be one of "
                f"{list(models.Term.SEASON_MAP_REV.keys())}."
            )
            raise serializers.ValidationError({"season": msg})
        return self.Meta.model.SEASON_MAP_REV[season]

    def to_representation(self, instance):
        season = instance.season
        representation = super().to_representation(instance)
        representation["season"] = self.Meta.model.SEASON_MAP[season]
        return representation


# ------------------------------Course Log------------------------------


class ListCourseLogSerializer(SerializerMixin, serializers.ListSerializer):
    def validate(self, data):
        MESSAGE1 = _(
            "You may not take more than 18 credits each term. you have already {} credits."
        )
        MESSAGE2 = _("You can not excceed the credit limit which is 18.")

        student = data[0].get("student", None)
        if not student:
            student = self.get_request().user
            if "Student" not in student.get_group():
                MESSAGE = _(
                    "Student can not be blank. You should either login as a student or specify a student."
                )
                raise serializers.ValidationError({"student": MESSAGE})

        section = data[0].get("section", None)
        if section:
            term = section.term
            newly_credits = sum(
                [item.get("section", None).course.credit for item in data]
            )
            if newly_credits and newly_credits > 18:
                raise serializers.ValidationError({"total credit": MESSAGE2})
            current_credits = models.CourseLog.objects.filter(
                section__term__pk=term.pk, student__pk=student.pk
            ).aggregate(soc=Sum("section__course__credit"))["soc"]
            if current_credits and (newly_credits + current_credits > 18):
                raise serializers.ValidationError(
                    {"total credit": MESSAGE1.format(current_credits)}
                )
        return data

    def update(self, instances, validated_data):
        result = []

        dinstances = {item.public_id: item for item in instances}
        dvalidated = {item["public_id"]: item for item in validated_data}
        for id, data in dvalidated.items():
            instance = dinstances.get(id, None)
            result.append(self.child.update(instance, data))
        return result

    # def create(self, validated_data):
    # return [self.child.create(attrs) for attrs in validated_data]


class CourseLogSerializer(SerializerMixin, serializers.ModelSerializer):
    public_id = serializers.CharField()
    # public_id = serializers.SerializerMethodField()

    class Meta:
        model = models.CourseLog
        fields = [
            "pk",
            "public_id",
            "student",
            "section",
            "midterm_exam",
            "final_exam",
            "final_grade",
            "status",
            "my_public_id",
        ]
        read_only_fields = ("public_id",)
        list_serializer_class = ListCourseLogSerializer
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=models.CourseLog.objects.all(),
        #         fields=["student", "section"],
        #     )
        # ]

    # def get_public_id(self, obj):
    #     return obj.public_id

    def validate(self, data):
        # to be added
        # Make sure that all data entries belong to the same user

        student = data.get("student", None)
        if not student:
            student = self.get_request().user
            if "Student" not in student.get_group():
                MESSAGE = _(
                    "Student can not be blank. You should either login as a student or specify a student."
                )
                raise serializers.ValidationError({"student": MESSAGE})
        return data

    def validate_section(self, section):
        MESSAGE = _("This section is filled.")
        if section.filled_capacity == section.total_capacity:
            raise serializers.ValidationError({"Section Capacity": MESSAGE})
        return section

    def validate_student(self, student):
        if "Student" in student.get_group():
            return student
        msg = _("Must be a student.")
        raise serializers.ValidationError(msg)

    def validate_midterm_exam(self, midterm):
        if midterm:
            if 0 <= midterm <= 20:
                return midterm
            msg = _(f"Grade must be in the [0,20] interval.")
            raise serializers.ValidationError(msg)

    def validate_final_exam(self, final):
        if final:
            if 0 <= final <= 20:
                return final
            msg = _(f"Grade must be in the [0,20] interval.")
            raise serializers.ValidationError(msg)

    def validate_final_grade(self, final):
        if final:
            if 0 <= final <= 20:
                return final
            msg = _(f"Grade must be in the [0,20] interval.")
            raise serializers.ValidationError(msg)

    def create(self, validated_data):
        obj = super().create(validated_data)
        return obj


# ------------------------------Complain------------------------------


class ComplainSerializer(SerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Complain
        fields = ["public_id", "student", "section", "text", "status"]
        read_only_fields = ("public_id", "status")

    # def create(self, validated_data):
    # pass

    # def update(self, instance, validated_data):
    # pass
