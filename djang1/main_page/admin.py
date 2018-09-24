from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *
# Register your models here.
# admin.site.register(Userinfo, ModelAdmin)
class UserinfoAdmin(admin.ModelAdmin):
    fields = ('uname', 'upwd', 'uemail', 'uphone')

admin.site.register(Userinfo,UserinfoAdmin)