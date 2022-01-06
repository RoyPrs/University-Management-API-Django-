# -*- coding: utf-8 -*-
#
# parnia/common/view_mixins.py
#

"""
Global view mixins
"""

from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.serializers import ValidationError


class TrapDjangoValidationErrorCreateMixin:

    def perform_create(self, serializer):
        try:
            instance = serializer.save()
        except DjangoValidationError as detail:
            raise ValidationError(detail.message_dict)


class TrapDjangoValidationErrorUpdateMixin:

    def perform_update(self, serializer):
        try:
            instance = serializer.save()
        except DjangoValidationError as detail:
            raise ValidationError(detail.message_dict)
