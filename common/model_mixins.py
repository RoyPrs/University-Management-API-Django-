# -*- coding: utf-8 -*-
#
# parnia/common/model_mixins.py
#

"""
Mixins used in Django models.
"""

# from datetime import datetime
# from dateutil.tz import tzutc

# from django.db import models
# from django.db.models import Q
# from django.utils.translation import gettext_lazy as _
# from django.conf import settings

#
# ValidateOnSaveMixin
#
class ValidateOnSaveMixin:

    def save(self, *args, **kwargs):
        """
        Execute ``full_clean``.

        """
        self.full_clean()
        super().save(*args, **kwargs)
