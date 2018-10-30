from django.urls import path, re_path
from .views import *
from login.views import *

urlpatterns = [
    re_path(r'^$', main_page_views, name='index'),
    re_path(r'view/(\d+)/', view_views, name='view'),
    re_path(r'picture/', show_pict, name='picture'),
    re_path(r'goods/', show_goods, name='goods'),
    re_path(r'logout/', logout, name='logout')
]