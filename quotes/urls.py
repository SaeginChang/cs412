## quotes/urls.py
## description: URL patterns for the quotes app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs hat are part of this app
urlpatterns = [
    path('', views.base, name="base"),
    path('show_all/', views.show_all, name='show_all'),
    path('about/', views.about, name='about'),
    path('quote/', views.quote, name='quote'),

]