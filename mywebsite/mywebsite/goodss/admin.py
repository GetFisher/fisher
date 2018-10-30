from django.contrib import admin
from django.contrib.admin import ModelAdmin
from goodss.models import *
# Register your models here.

admin.site.register(Goods, ModelAdmin)
admin.site.register(Cart, ModelAdmin)
admin.site.register(Order, ModelAdmin)
