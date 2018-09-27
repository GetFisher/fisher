from django.conf.urls import url
from userinfo import views

urlpatterns = [
    url(r'registerin/',views.register_,name="registerin" ),
    url(r'loginin/',views.login_,name="loginin" ),
]
