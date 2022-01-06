# -*- coding: utf-8 -*-
#
# parnia/urls.py
#
"""
Parent URL file.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
	path('um/', include('user_management.urls')),
	path('cm/', include('course_management.urls')),
]