from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *
# Register your models here.
# admin.site.register(Userinfo, ModelAdmin)
class UserinfoAdmin(admin.ModelAdmin):
    fields = ('username', 'password', 'email', 'uphone', 'address', 'last_login')


admin.site.register(Userinfo, UserinfoAdmin)
admin.site.register(Article, ModelAdmin)
admin.site.register(Picture, ModelAdmin)
