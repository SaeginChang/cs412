## restaurant/urls.py
## description: URL patterns for the restaurant app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs hat are part of this app
urlpatterns = [
    path('', views.base, name="base"),
    path(r'main/', views.main, name='main'),
    path(r'rest_submit/', views.rest_submit, name='rest_submit'),
    path(r'order/', views.show_order, name='show_order'),
    # path(r'confirmation/', views.confirmation, name='confirmation'),

]