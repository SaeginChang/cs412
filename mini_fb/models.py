# mini_fb/models.py
# Define the data objects for our application
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.timezone import now

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
    
class StatusMessage(models.Model):
    '''Status Message for the Profiles'''
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

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
    image_file = models.ImageField(upload_to='static/')
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Image {self.id} for {self.status_message}"