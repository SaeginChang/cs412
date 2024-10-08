# mini_fb/models.py
# Define the data objects for our application
from django.db import models
from django.utils import timezone

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
    
class StatusMessage(models.Model):
    '''Status Message for the Profiles'''
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        return f"{self.profile.first_name} Status: {self.message}"