# mini_fb/views.py
# define the views for the mini_fb app
from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import * ## import the models 

# class-based view
class ShowAllProfileView(ListView):
    '''the view to show all Articles'''

    model = Profile #the model to display
    template_name = 'mini_fb/show_all_profiles.html'

    context_object_name = 'profiles' # this is the context variable to use in the template

class ShowProfilePageView(DetailView):
    '''the view for all detailed profiles'''
    model = Profile
    template_name = 'mini_fb/show_profile.html' 
    context_object_name = 'profile'

def profile_status_view(request, pk):
    profile = Profile.objects.get(pk=pk)
    status_messages = profile.get_status_messages()
    print(status_messages, "hhhhhhhhhhhhhhhhh")
    return render(request, 'mini_fb/show_profile.html', {'profile': profile, 'status_messages': status_messages})