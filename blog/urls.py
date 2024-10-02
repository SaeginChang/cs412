## blog/urls.py
## description: URL patterns for the hw app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs hat are part of this app
urlpatterns = [
    # path(r'', views.home, name="home"),
    path(r'', views.ShowAllView.as_view(), name="show_all"),

]