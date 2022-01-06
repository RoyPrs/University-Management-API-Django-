
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

# from common.admin_mixins import UserAdminMixin
User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "pk", "get_group")
    # list_display = ("username",list("groups"), "pk")
#     fieldsets = (
#         (None, {'fields': ('public_id', 'username', 'password',)}),
#         (_("Personal Info"), {'fields': ('first_name', 'last_name',
#                                          'address','dob', 'email')}),
#         (_("Permissions"), {'classes': ('collapse',),
#                             'fields': ('_role', 'is_active', 'is_staff',
#                                        'is_superuser',
#                                        'user_permissions',)}),
#         (_("Status"), {'classes': ('collapse',),
#                        'fields': ('send_email', 'need_password', 'last_login',
#                                   'date_joined',)}),
#         )
#     readonly_fields = ('public_id', 'last_login', 'date_joined',)
#     list_display = ('public_id', 'username', 'email',
#                     'first_name', 'last_name', '_role',
#                     'is_staff', 'is_active',)
#     list_editable = ('is_staff', 'is_active', '_role',)
#     search_fields = ('username', 'last_name', 'email', 'public_id',)
#     filter_horizontal = ('groups', 'user_permissions',)
