# mini_fb/views.py
# define the views for the mini_fb app
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import * ## import the models 

from django.urls import reverse_lazy, reverse
from .forms import *

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

class CreateProfileView(CreateView):
    '''Class based view for creating a new profile'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    success_url = reverse_lazy('show_all_profiles')

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs['pk']
        context['profile'] = get_object_or_404(Profile, pk=profile_pk)
        return context

    def form_valid(self, form):
        sm = form.save(commit=False)
        profile_pk = self.kwargs['pk']
        sm.profile = get_object_or_404(Profile, pk=profile_pk)
        sm.save()

        files = self.request.FILES.getlist('files')

        for f in files:
            img = Image(status_message=sm, image_file=f)
            img.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', args=[self.kwargs['pk']])
    
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    success_url = reverse_lazy('show_all_profiles')

class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk':self.obejct.profile.pk})
    
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm 
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})