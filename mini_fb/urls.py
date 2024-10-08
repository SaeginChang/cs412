## mini_fb/urls.py
## description: URL patterns for the mini_fb app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs hat are part of this app
urlpatterns = [
    # path(r'', views.home, name="home"),
    path('', views.ShowAllProfileView.as_view(), name='show_all_profiles'), 
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),

]