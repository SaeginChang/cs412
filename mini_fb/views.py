# mini_fb/views.py
# define the views for the mini_fb app
from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView
from .models import * ## import the models 

# class-based view
class ShowAllProfileView(ListView):
    '''the view to show all Articles'''

    model = Profile #the model to display
    template_name = 'mini_fb/show_all_profiles.html'

    context_object_name = 'profiles' # this is the context variable to use in the template


