# -*- coding: utf-8 -*-
#
# parnia/user_management/models.py
#

"""
User model.
"""
__docformat__ = "restructuredtext en"
import logging

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from common import generate_public_key
from common.model_mixins import ValidateOnSaveMixin

log = logging.getLogger(__name__)

class UserManager(BaseUserManager):
    def _create_user(
        self, username, email, password, is_staff, is_superuser, **extra_fields
    ):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()

        if not username:
            raise ValueError(_("The username must be set."))

        email = self.normalize_email(email)
        # role = extra_fields.pop('role', self.model.STUDENT)

        if not password:
            if email:
                password = self.make_random_password()
                extra_fields["send_email"] = True
                extra_fields["need_password"] = True
            else:
                raise ValueError(_("Must have a valid email or password."))
        else:
            extra_fields["send_email"] = False
            extra_fields["need_password"] = False
        groups = extra_fields.pop("groups", [1])
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        # user._role = role
        user.save(using=self._db)
        if user.is_superuser:
            user.groups.add(4)
        else:
            user.groups.set(groups)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(
            username, email, password, False, False, **extra_fields
        )

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(
            username, email, password, True, True, **extra_fields
        )


class StaffManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__in=[3])
        # return super().get_queryset().filter(_role = self.model.STAFF)


class InstructorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__in=[2])
        # return super().get_queryset().filter(_role=self.model.INSTRUCTOR)


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__in=[1])
        # return super().get_queryset().filter(_role=self.model.STUDENT)


class User(AbstractUser, ValidateOnSaveMixin, models.Model):

    # ADMINISTRATOR = 4
    # STAFF = 3
    # INSTRUCTOR = 2
    # STUDENT = 1
    # ROLE = (
    #     (ADMINISTRATOR, _("ADMINISTRATOR")),
    #     (STAFF, _("STAFF")),
    #     (INSTRUCTOR, _("INSTRUCTOR")),
    #     (STUDENT, _("STUDENT")),
    #     )
    # ROLE_MAP = {k: v for k, v in ROLE}
    # ROLE_MAP_REV = {v: k for k, v in ROLE}

    YES = True
    NO = False
    YES_NO = (
        (YES, _("Yes")),
        (NO, _("No")),
    )

    MALE = "Male"
    FEMALE = "Female"
    NOT_SELECTED = "Not selected"
    GENDERS = (
        (MALE, _("Male")),
        (FEMALE, _("Female")),
        (NOT_SELECTED, _("Not selected")),
    )

    public_id = models.CharField(
        verbose_name=_("Public User ID"),
        max_length=30,
        unique=True,
        blank=True,
        editable=False,
        help_text=_("Public ID to identify an individual user."),
    )
    password = models.CharField(
        verbose_name=_("password"), max_length=128, help_text=_("Password")
    )
    # _role = models.SmallIntegerField(
    #     verbose_name=_("Role"), choices=ROLE, default=STUDENT,
    #     help_text=_("The role of the user."))
    send_email = models.BooleanField(
        verbose_name=_("Send Email"),
        choices=YES_NO,
        default=NO,
        help_text=_(
            "Set to YES if this individual needs to be sent " "an email."
        ),
    )
    need_password = models.BooleanField(
        verbose_name=_("Need Password"),
        choices=YES_NO,
        default=NO,
        help_text=_(
            "Set to YES if this individual needs to reset their " "password."
        ),
    )
    dob = models.DateField(
        verbose_name=_("Date of Birth"),
        null=True,
        blank=True,
        help_text=_("The date of your birth."),
    )
    address = models.TextField(
        verbose_name=_("Address"),
        max_length=300,
        null=True,
        blank=True,
        help_text=_("Address"),
    )
    gender = models.CharField(
        verbose_name="Gender",
        max_length=20,
        choices=GENDERS,
        default=NOT_SELECTED,
    )

    members = UserManager()
    staffs = StaffManager()
    instructors = InstructorManager()
    students = StudentManager()

    def clean(self):
        # Populate the public_id on record creation only.
        if self.pk is None and not self.public_id:
            self.public_id = generate_public_key()
		    #log.info("Public ID created %s", self.public_id)

            # if self.is_superuser:
            # self._role = self.ADMINISTRATOR

        # if self._role not in self.ROLE_MAP:
        #     msg = _(f"Invalid user role, must be one of "
        #             f"{list(self.ROLE_MAP_REV.keys())}.")
        #     raise ValidationError({'role': msg})

    class Meta:
        ordering = (
            "last_name",
            "username",
        )
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.get_full_name_reversed()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("user-detail", args=[self.public_id])

    def get_group(self):
        groups = set(self.groups.values_list("name", flat=True))
        return groups or "No groups set yet"

    def process_groups(self, groups):
        """
        This method adds and removes groups to a member.

        """
        group_list = [group.pk for group in groups]
        self.groups.set(group_list)

    def get_full_name_or_username(self):
        result = self.get_full_name()

        if result.strip() == "":
            result = self.username

        return result

    def get_full_name_reversed(self):
        result = ""
        if self.last_name or self.first_name:
            result = "{}, {}".format(self.last_name, self.first_name)
        else:
            result = self.username
        return result

    def full_name_reversed_producer(self):
        return self.get_full_name_reversed()

    full_name_reversed_producer.short_description = _("User")
