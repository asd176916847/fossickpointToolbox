from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login/',views.user_login,name="login"),
    url(r'^home/',views.user_home,name="home"),
    url(r'^register/',views.user_register,name="register")
]