# -*- coding: utf-8 -*-
#
# parnia/course_management/models.py
#

import datetime

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from common.model_mixins import ValidateOnSaveMixin
from common import generate_public_key

# ------------------------------Course------------------------------
class Course(ValidateOnSaveMixin, models.Model):
    public_id = models.CharField(
        verbose_name=_("Public Course ID"),
        max_length=30,
        unique=True,
        blank=True,
        editable=False,
        help_text=_("Public ID to identify an individual course."),
    )
    name = models.CharField(
        verbose_name=_("Course Name"),
        max_length=50,
        unique=True,
        help_text=_("The name of the course"),
    )
    prerequesits = models.ManyToManyField(
        "self",
        verbose_name=_("Prerequesit Courses"),
        help_text=_("The course(s) one must pass before taking this course."),
        symmetrical=False,
        blank=True,
    )
    credit = models.PositiveSmallIntegerField(
        verbose_name=_("Course Credit"), help_text=_("The credit of the course")
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("course-detail", kwargs={"public_id": self.public_id})

    def process_prerequesits(self, prerequesits):
        """
        This method adds and removes prerequesits to a course.

        """
        self.prerequesits.clear()
        prerequesits_list = [prerequesit.pk for prerequesit in prerequesits]
        self.prerequesits.set(prerequesits_list)

    def get_prerequesits(self):
        prerequesits = list(self.prerequesits.values_list("name", flat=True))
        return prerequesits or "No prerequesits set."


# ------------------------------Term------------------------------
class Term(ValidateOnSaveMixin, models.Model):

    SPRING = 1
    SUMMER = 2
    FALL = 3
    WINTER = 4
    SEASON = (
        (SPRING, _("SPRING")),
        (SUMMER, _("SUMMER")),
        (FALL, _("FALL")),
        (WINTER, _("WINTER")),
    )
    SEASON_MAP = {k: v for k, v in SEASON}
    SEASON_MAP_REV = {v: k for k, v in SEASON}

    public_id = models.CharField(
        verbose_name=_("Public Term ID"),
        max_length=30,
        unique=True,
        blank=True,
        editable=False,
        help_text=_("Public ID to identify an individual term."),
    )
    season = models.SmallIntegerField(
        verbose_name=_("Season"),
        default=1,
        help_text=_("Term Season"),
        choices=SEASON,
    )
    start_date = models.DateField(
        verbose_name=_("Term Start Date"),
        blank=True,
        help_text=_("The day on which the term starts."),
    )

    class Meta:
        ordering = ("start_date",)
        verbose_name = "Term"
        verbose_name_plural = "Terms"

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

    def __str__(self):
        return self.get_name()

    def get_absolute_url(self):
        return reverse("term-detail", kwargs={"pulic_id": self.pulic_id})

    def get_name(self):
        return "{0} {1:%Y}".format(
            self.SEASON_MAP[self.season], self.start_date
        )

    @property
    def name(self):
        return self.get_name()

    def get_classes(self):
        classes = list(self.classes.values_list("course__name", flat=True))
        return classes or "No classes set."


# ------------------------------Course Section------------------------------
class CourseSection(ValidateOnSaveMixin, models.Model):
    DAYS_OF_THE_WEEK = (
        ("Monday", "Monday"),
        ("Tueseday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    )

    HOURS_OF_THE_DAY = (
        ("8-10", "8-10"),
        ("10-12", "10-12"),
        ("2-4", "2-4"),
        ("4-6", "4-6"),
        ("6-8", "6-8"),
    )

    public_id = models.CharField(
        verbose_name=_("Public Course Section ID"),
        max_length=30,
        unique=True,
        blank=True,
        editable=False,
        help_text=_("Public ID to identify an individual course."),
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name=_("Corresponding Course"),
        help_text=_("The course for which this section is defined."),
        related_name="sections",
    )
    term = models.ForeignKey(
        Term,
        on_delete=models.CASCADE,
        verbose_name=_("Term"),
        help_text=_("The term in which this class section is held."),
        related_name="classes",
    )
    local_id = models.PositiveSmallIntegerField(
        verbose_name=_("Course Section Group"),
        blank=True,
        editable=False,
        help_text=_(
            "The identity of the course section among all sections of a course in a term."
        ),
    )
    total_capacity = models.PositiveSmallIntegerField(
        verbose_name=_("Total Capacity"),
        help_text=_("Total Capacity of this Section"),
    )
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Instructor"),
        help_text=_("The instructor of the class"),
        related_name="classes",
    )
    first_session_weekday = models.CharField(
        verbose_name=_("First Session Weekday"),
        max_length=30,
        help_text=_("The weekday of the first session."),
        choices=DAYS_OF_THE_WEEK,
    )
    second_session_weekday = models.CharField(
        verbose_name=_("Second Session Weekday"),
        max_length=30,
        help_text=_("The weekday of the second session."),
        choices=DAYS_OF_THE_WEEK,
    )
    hour_schedule = models.CharField(
        verbose_name=_("Hour of the Class"),
        max_length=30,
        help_text=_("Hours of the class"),
        choices=HOURS_OF_THE_DAY,
    )
    exam_date = models.DateField(
        verbose_name=_("Exam Date"),
        max_length=30,
        help_text=_("The date and time of the exam"),
    )

    class Meta:
        ordering = ("course__name",)
        verbose_name = "Course Section"
        verbose_name_plural = "Course Sections"

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

        # Populate local_id according the number of sections of the same course in the same term
        number = CourseSection.objects.filter(
            term=self.term, course=self.course
        ).count()
        self.local_id = number + 1

    def __str__(self):
        return "{0} G{1}".format(self.course, self.local_id)

    def get_absolute_url(self):
        return reverse(
            "coursesection-detail", kwargs={"public_id": self.public_id}
        )

    @property
    def filled_capacity(self):
        return CourseLog.objects.filter(section=self).count()


# ------------------------------Course Log------------------------------
class CorselogManager(models.Manager):
    def create(self, data):
        pass


class CourseLog(ValidateOnSaveMixin, models.Model):
    STATUS = (
        ("Unavailable", "Unavailable"),
        ("Not Approved", "Not Approved"),
        ("Approved", "Approved"),
    )

    public_id = models.CharField(
        verbose_name=_("Public Course Log ID"),
        max_length=30,
        unique=True,
        blank=True,
        editable=False,
        help_text=_("Public ID to identify an individual course log."),
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Student"),
        blank=True,
        help_text=_("The student corresponding to this course log"),
    )
    section = models.ForeignKey(
        CourseSection,
        on_delete=models.CASCADE,
        verbose_name=_("Section"),
        blank=False,
        help_text=_("The course section of this class"),
    )
    midterm_exam = models.PositiveSmallIntegerField(
        verbose_name=_("Midterm Exam Grade"),
        blank=True,
        null=True,
        help_text=_("The grade of the midterm exam"),
    )
    final_exam = models.PositiveSmallIntegerField(
        verbose_name=_("Final Exam Grade"),
        blank=True,
        null=True,
        help_text=_("The grade of the final exam"),
    )
    final_grade = models.PositiveSmallIntegerField(
        verbose_name=_("Final Grade"),
        blank=True,
        null=True,
        help_text=_("The final grade of the course"),
    )
    status = models.CharField(
        verbose_name=_("Grade Status"),
        max_length=20,
        choices=STATUS,
        default="Unavailable",
        help_text=_(
            "Designates if the grade is not entered, entered or finalized."
        ),
    )

    class Meta:
        verbose_name = "Course Log"
        verbose_name_plural = "Course Logs"

    def clean(self):
        # Populate the public_id on record creation only.
        print("in clean")
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

    def __str__(self):
        return f"{self.student}'s {self.section.course} log "

    def save(self, *args, **kwargs):
        print("in save")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("courselog-detail", kwargs={"public_id": self.public_id})

    def change_status(self, status):
        # I think we would better off doing it in a manager
        # This way we can run bulk_update
        # I'm still not sure though
        pass


# ------------------------------Complain------------------------------


class ComplainQuerySet(models.QuerySet):
    def toggle_status(self, status):
        print("in the toggle")
        self.update(status=status)


class ComplainManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="Seen")


class Complain(ValidateOnSaveMixin, models.Model):
    STATUS = (("Seen", "Seen"), ("Unseen", "Unseen"))
    public_id = models.CharField(
        verbose_name=_("Public Complain ID"),
        max_length=30,
        unique=True,
        blank=True,
        editable=False,
        help_text=_("Public ID to identify an individual complain."),
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Student"),
        help_text=_("The student corresponding to this complain"),
    )
    section = models.ForeignKey(
        CourseSection,
        on_delete=models.CASCADE,
        verbose_name=_("Section"),
        help_text=_("The course section of this complain"),
    )
    text = models.TextField(
        verbose_name=_("Text"),
        max_length=300,
        help_text=_("The text of the complain."),
    )
    status = models.CharField(
        verbose_name=_("Complain Status"),
        max_length=10,
        choices=STATUS,
        default="Unseen",
        editable=False,
        help_text=_(
            "Designates if the complain is seen by the instructor or not."
        ),
    )
    objects = models.Manager()
    queryset = ComplainQuerySet.as_manager()
    manager = ComplainManager()

    class Meta:
        verbose_name = "Complain"
        verbose_name_plural = "Complains"
        unique_together = [["student", "section"]]

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()

    def __str__(self):
        return f"{self.student} {self.section.course.name}"

    def get_absolute_url(self):
        return reverse("complain-detail", kwargs={"public_id": self.public_id})


# ------------------------------Draft------------------------------

# choices
# database fields
# custom manager attributes
# Meta
# def __str__()
# def save()
# def get_absolute_url()
# custom methods
