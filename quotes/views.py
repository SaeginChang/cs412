## quotes/views.py
## description: write view functions to handle URL requests for the quotes app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
def index(request):
    '''
    Function to handle the URL request for /quotes (main page).
    Delegate redering to the temmplate quotes/index.html
    '''

    # use this template to reder the response
    template_name = 'quotes/index.html'

    # create a dictionary of context variables for the template:
    context = {
        "quotesList" : ["When you're in your darkest place, you give yourself hope and that's inner strength.", 
                        "Life happens wherever you are, whether you make it or not.",
                        "Sometimes the best way to solve your own problems is to help someone else"],
        "imagesList" : ["static/quotes/iroh1.jpg",
                        "images/iroh2.jpg",
                        "images/iroh3.jpg"]
    }

    # delegate redering work to the template
    return render(request, template_name, context)
