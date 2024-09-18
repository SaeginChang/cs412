## hw/views.py
## description: write view functions to handle URL requests for the hw app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# # Create your views here.
# def home(request):
#     '''Handle the main URL for the hw app.'''

#     response_text = '''
#     Hello, world!
#     '''

#     # create and return a reponse to the client
#     return HttpResponse(response_text)

def home(request):
    '''
    Function to handle the URL request for /hw (main page).
    Delegate redering to the temmplate hw/home.html
    '''

    # use this template to reder the response
    template_name = 'hw/home.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
        "letter1" : chr(random.randint(65,90)), # aletter from A to Z
        "letter2" : chr(random.randint(65,90)),
        "number" : random.randint(1,10), # number from 1 to 10
    }

    # delegate redering work to the template
    return render(request, template_name, context)
