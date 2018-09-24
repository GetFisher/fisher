from django.urls import path, include, re_path
from django.contrib import admin
from login.views import login_views

urlpatterns = [
    re_path(r'^$', login_views)
]