# -*- coding: utf-8 -*-
#
# parnia/common/serializer_mixin.py
#
"""
Global serializer mixins
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers

UserModel = get_user_model()


#
# SerializerMixin
#
class SerializerMixin:

    def get_request(self):
        return self.context.get('request', None)

    def get_user_object(self):
        request = self.get_request()
        user = None

        if request is not None:
            user = request.user

        return user
