from django.conf.urls import url

from fossickpointToolbox import settings
from . import views
from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login/',views.user_login,name="login"),
    url(r'^home/',views.user_home,name="home"),
    url(r'^register/',views.user_register,name="register"),
    url(r'^contents/',views.contents,name="contents"),
    url(r'^content/(?P<contentID>[0-9]+)/$',views.content,name="content"),
    url(r'^user/',views.user,name="user"),
    url(r'^programs/',views.programs,name="program"),
    url(r'^program/(?P<programID>[0-9]+)/$',views.program,name="programdetail"),
]
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()