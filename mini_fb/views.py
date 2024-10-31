from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, StatusMessage, Image
from django.urls import reverse_lazy, reverse
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm

# class-based view to show all profiles
class ShowAllProfileView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['status_messages'] = profile.get_status_messages()
        return context

# View for creating a new profile
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
    success_url = reverse_lazy('show_all_profiles')

    def get_context_data(self, **kwargs):
        # Call the superclass to retrieve existing context
        context = super().get_context_data(**kwargs)
        # Add an instance of UserCreationForm to the context
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        # Reconstruct the UserCreationForm with submitted POST data
        user_form = UserCreationForm(self.request.POST)
        
        # Validate both forms
        if user_form.is_valid() and form.is_valid():
            # Save the UserCreationForm to create a new User
            user = user_form.save()
            
            # Attach the new user to the profile instance (form.instance)
            form.instance.user = user
            
            # Save the Profile instance and complete form handling
            return super().form_valid(form)
        else:
            # If either form is invalid, re-render the form with errors
            return self.form_invalid(form)

# View for creating a status message
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context

    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user)
        if profile.user != self.request.user:
            raise PermissionDenied  # Only profile owner can add status messages
        form.instance.profile = profile
        response = super().form_valid(form)

        # Handling file uploads for images
        files = self.request.FILES.getlist('files')
        for f in files:
            Image.objects.create(status_message=form.instance, image_file=f)
        return response

    def get_success_url(self):
        # Redirect to the profile page after creating a status message
        profile = get_object_or_404(Profile, user=self.request.user)
        return reverse('show_profile', args=[profile.pk])

# View for updating a profile
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    success_url = reverse_lazy('show_all_profiles')

    def get_object(self):
        # Retrieve Profile associated with the logged in user
        return get_object_or_404(Profile, user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        return super().dispatch(request, *args, **kwargs)

# View for deleting a status message
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})

    def dispatch(self, request, *args, **kwargs):
        status_message = self.get_object()
        return super().dispatch(request, *args, **kwargs)

# View for updating a status message
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm 
    template_name = 'mini_fb/update_status_form.html'

    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})

    def dispatch(self, request, *args, **kwargs):
        status_message = self.get_object()
        return super().dispatch(request, *args, **kwargs)

# View for adding a friend
class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)

# View for showing friend suggestions
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'

    def get_object(self, **kwargs):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        if profile.user != self.request.user:
            raise PermissionDenied  # Only profile owner can see friend suggestions
        context['suggestions'] = profile.get_friend_suggestions()
        return context

# View for showing the news feed
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        if profile.user != self.request.user:
            raise PermissionDenied  # Only profile owner can view news feed
        context['news_feed'] = profile.get_news_feed()
        return context
