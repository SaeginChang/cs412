# mini_fb/models.py
# Define the data objects for our application
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the idea of one Profile'''

    #  data attributes of a Profile:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of the object.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        '''getting the status message for this profile'''
        status = StatusMessage.objects.filter(profile=self)
        return status
    
    def get_absolute_url(self):
        '''Return the URL to access a detail record for this profile'''
        return reverse('show_profile', args=[self.pk])
    
    def add_friend(self, other):
        """ adding a friend to a profile"""
        if self == other:
            return # to prevent self friending
        
        if not Friend.objects.filter(
            models.Q(profile1=self, profile2=other) |
            models.Q(profile1=other, profile2=self)
        ).exists():
            Friend.objects.create(profile1=self, profile2=other, timestamp=now())

    def get_friends(self):
        """Retrieve all friends for this profile"""
        friends = Friend.objects.filter(
            models.Q(profile1=self) | models.Q(profile2=self)
        )
        return [f.profile2 if f.profile1 == self else f.profile1 for f in friends]
    
    def get_friend_suggestions(self):
        """Find all profiles not already friends and not self"""
        friends = self.get_friends()
        return Profile.objects.exclude(id__in=[self.id] + [f.id for f in friends])
    
    def get_news_feed(self):
        """Collect status messages from the profile and all friends"""
        friends = self.get_friends()
        all_profiles = [self] + friends
        return StatusMessage.objects.filter(profile__in=all_profiles).order_by('-timestamp')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
class StatusMessage(models.Model):
    '''Status Message for the Profiles'''
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)

    def __str__(self):
        return f"{self.profile.first_name} Status: {self.message}"
    
    def get_images(self):
        """
        return all images related to this status message
        """
        return self.image_set.all()
    
class Image(models.Model):
    """Images for the profiles"""
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='profile_images/')
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Image {self.id} for {self.status_message}"
    
class Friend(models.Model):
    """Class for friends list"""
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"