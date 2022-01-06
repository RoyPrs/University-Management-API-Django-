# -*- coding: utf-8 -*-
#
# parnia/user_management/serializers.py
#
"""
User Management serializers.
"""


from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework.permissions import SAFE_METHODS

from common.serializer_mixin import SerializerMixin
from user_management.models import User

UserModel = get_user_model()

#
# User
#


class UserSerializer(SerializerMixin, serializers.ModelSerializer):
    MESSAGE = _("You do not have permission to change the '{}' field.")
    # ADMINISTRATOR = UserModel.ROLE_MAP[UserModel.ADMINISTRATOR]

    full_name = serializers.SerializerMethodField()
    # role = serializers.CharField(
    #     max_length=20, required=False)
    href = serializers.HyperlinkedIdentityField(
        view_name="user-detail",
        lookup_field="public_id",
        label=_("Identity URI"),
    )

    def get_full_name(self, obj):
        return obj.get_full_name_or_username()

    def validate(self, data):
        request = self.get_request()
        is_active = data.get("is_active")
        is_staff = data.get("is_staff")
        is_superuser = data.get("is_superuser")
        # role = self.initial_data.get('role')
        # if role: data['role'] = role
        # if request.method in ('PUT', 'PATCH'):
        #     if (is_active is not None
        #         and self.instance.is_active != is_active and not
        #         (self.instance.is_superuser or
        #          self.instance.role == self.ADMINISTRATOR)):
        #         raise serializers.ValidationError(
        #             {'is_active': self.MESSAGE.format('is_active')})

        #     if (is_staff is not None
        #         and self.instance.is_staff != is_staff and not
        #         (self.instance.is_superuser or
        #          self.instance.role == self.ADMINISTRATOR)):
        #         raise serializers.ValidationError(
        #             {'is_staff': self.MESSAGE.format('is_staff')})

        #     if (is_superuser is not None
        #         and self.instance.is_superuser != is_superuser
        #         and not self.instance.is_superuser):
        #         raise serializers.ValidationError(
        #             {'is_superuser': self.MESSAGE.format('is_superuser')})
        #     if (role is not None
        #         and self.instance.role != role and not
        #         (self.instance.is_superuser or
        #          self.instance.role == self.ADMINISTRATOR)):
        #         raise serializers.ValidationError(
        #             {'role': self.MESSAGE.format('role')})
        return data

    def create(self, validated_data):
        username = validated_data.pop("username", "")
        password = validated_data.pop("password", "")
        email = validated_data.pop("email", "")
        obj = UserModel.members.create_user(
            username, email=email, password=password, **validated_data
        )
        # Token.objects.create(user=obj)
        return obj

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.set_password(validated_data.get("password", instance.password))
        instance.send_email = validated_data.get(
            "send_email", instance.send_email
        )
        instance.need_password = validated_data.get(
            "need_password", instance.need_password
        )
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.address = validated_data.get("address", instance.address)
        instance.dob = validated_data.get("dob", instance.dob)
        instance.email = validated_data.get("email", instance.email)
        # instance.role = validated_data.get(
        # 'role', instance.role)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.is_superuser = validated_data.get(
            "is_superuser", instance.is_superuser
        )
        instance.save()
        instance.process_groups(validated_data.get("groups", []))
        return instance

    class Meta:
        model = UserModel
        fields = (
            "public_id",
            "username",
            "password",
            "full_name",
            "groups",
            "send_email",
            "need_password",
            "first_name",
            "last_name",
            "address",
            "dob",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "href",
        )
        read_only_fields = (
            "public_id",
            "last_login",
            "date_joined",
        )
        extra_kwargs = {"password": {"write_only": True}}


#
# Login
#


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        fields = (
            "username",
            "password",
        )

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            msg = _("The entered username and/or password is invalid.")
            raise serializers.ValidationError({"username": msg})

        data["user"] = user
        return data
