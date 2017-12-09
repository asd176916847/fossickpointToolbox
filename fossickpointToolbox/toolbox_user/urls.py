from django.conf.urls import url

from fossickpointToolbox import settings
from . import views
from django.conf.urls import include, url
urlpatterns = [
        url(r'^$', views.index, name="index"),
]