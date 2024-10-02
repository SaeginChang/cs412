# mini_fb/models.py
# Define the data objects for our application
from django.db import models

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