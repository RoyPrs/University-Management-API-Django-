# -*- coding: utf-8 -*-
#
# parnia/user_management/views.py
#
"""
User Management API Views
"""

import base64
import re
import string
from decimal import Decimal

from django.contrib.auth import get_user_model, login, logout
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate

from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    GenericAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from rest_condition import C, And, Or, Not

from common.permissions import (
    IsAdminSuperUser,
    IsAdministrator,
    IsStudent,
    IsAnyUser,
    IsReadOnly,
    IsUserActive,
    IsPostOnly,
    IsSelf,
)
from common.view_mixins import (
    TrapDjangoValidationErrorCreateMixin,
    TrapDjangoValidationErrorUpdateMixin,
)
from user_management.serializers import UserSerializer, LoginSerializer

UserModel = get_user_model()

#
# User
#


class UserMixin:

    # ADMINISTRATOR = UserModel.ROLE_MAP[UserModel.ADMINISTRATOR]

    def get_serializer_class(self):
        serializer = UserSerializer
        return serializer

    def get_queryset(self):
        return UserModel.objects.all()


class UserList(
    TrapDjangoValidationErrorCreateMixin, UserMixin, ListCreateAPIView
):
    """
    User list endpoint.
    """

    permission_classes = (
        And(
            IsUserActive,
            IsAuthenticated,
            Or(
                IsAdminSuperUser,
                IsAdministrator,
            ),
        ),
    )
    # filter_backends = (SearchFilter,)
    # search_fields = ('username', 'first_name', 'last_name', 'email',)
    lookup_field = "public_id"


user_list = UserList.as_view()


class UserDetail(
    TrapDjangoValidationErrorUpdateMixin, UserMixin, RetrieveUpdateAPIView
):
    permission_classes = (
        And(
            And(
                IsUserActive,
                IsAuthenticated,
                Or(
                    IsAdminSuperUser,
                    IsAdministrator,
                    IsSelf,
                ),
            ),
            Or(IsSelf, IsAdministrator),
        ),
    )

    lookup_field = "public_id"


user_detail = UserDetail.as_view()


#
# Login
#
class LoginView(GenericAPIView):
    """
    Login view. Performs a login on a POST and provides the user's full
    name and the href to the user's endpoint. Credentials are required to
    login.
    """

    serializer_class = LoginSerializer
    permission_classes = ()

    CHARS = string.ascii_letters + string.digits + "+/="
    # The regex below will ignore any additional parameters as per RFC7617.
    RE_SEARCH = re.compile(
        r"^.*(Basic +)(?P<enc_creds>[{}]+) *.*$".format(CHARS)
    )

    def post(self, request, *args, **kwargs):

        basic = request.META.get("HTTP_AUTHORIZATION")
        sre = self.RE_SEARCH.search("" if basic is None else basic)
        enc_creds = sre.group("enc_creds") if sre is not None else ""
        data = {}

        # Parse out the username and password.
        if len(enc_creds) > 0:
            creds = base64.b64decode(bytearray(enc_creds, "utf-8")).decode()
            username, delm, password = creds.partition(":")
            data["username"] = username
            data["password"] = password

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        login(request, user)
        result = {}
        result["fullname"] = user.get_full_name_or_username()
        result["href"] = reverse(
            "user-detail", kwargs={"public_id": user.public_id}, request=request
        )
        return Response(result)


login_view = LoginView.as_view()

# class TokenLoginView(GenericAPIView):
#     permission_classes = ()

#     def post(self, request,):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)
#         if user:
#             return Response({"token": user.auth_token.key})
#         else:
#             return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
# token_login_view = TokenLoginView.as_view()

#
# Logout
#
class LogoutView(APIView):
    """
    Logout view. Performs the logout on a POST. No POST data is required
    to logout.
    """

    permission_classes = (And(IsUserActive, IsAuthenticated, IsAnyUser),)

    def post(self, request, *args, **kwargs):
        logout(request)
        status = HTTP_200_OK
        result = {"detail": _("Logout was successful.")}
        return Response(result, status=status)


logout_view = LogoutView.as_view()


# -------------------------------Draft-------------------------------
from rest_framework.decorators import api_view, permission_classes


@api_view(["GET", "POST"])
@permission_classes([IsAdministrator])
def test(request):

    if request.method == "POST":
        return Response({"msg": "hi post"})
    else:
        return Response({"msg": "hi get"})
