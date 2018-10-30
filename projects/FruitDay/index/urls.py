from django.conf.urls import url
from .views import *
# 正常访问路径
urlpatterns = [
    #访问路径是 /
    url(r'^$', index_views),
    #访问路径是 /login
    url(r'^login/$', login_views),
    #访问路径是 /register
    url(r'^register/$', register_views),
]
# 验证路径
urlpatterns += [
    url(r"^checkuphone/$", checkuphone_views),
    url(r"^checklogin/$", checklogin_views),
    url(r"^logout/$", logout_views),
    url(r"^loadgoods/$", loadgoods_views),
    url(r"^add_cart/$", add_cart_views),
    url(r"^cart_count/$", cart_count_views),
]







