## quotes/views.py
## description: write view functions to handle URL requests for the quotes app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

quotesList = ["When you're in your darkest place, you give yourself hope and that's inner strength.", 
                        "Life happens wherever you are, whether you make it or not.",
                        "Sometimes the best way to solve your own problems is to help someone else"]
    
imagesList = ["/static/iroh1.jpg",
                        "/static/iroh2.jpg",
                        "/static/iroh3.jpg"]

# Create your views here.
def quote(request):
    '''
    Function to handle the URL request for /quotes (main page).
    Delegate redering to the temmplate quotes/quote.html
    '''

    # use this template to reder the response
    template_name = 'quotes/quote.html'

    random_quote = random.choice(quotesList)
    random_image = random.choice(imagesList)

    # Create the context dictionary with the selected quote and image
    context = {
        "quote": random_quote,
        "image": random_image,
    }

    # delegate redering work to the template
    return render(request, template_name, context)

def show_all(request):
    '''
    Function to handle the URL request for /show_all.
    Delegate redering to the template quotes/show_all.html
    '''

    # use this template to reder the response
    template_name = 'quotes/show_all.html'

    # Create the context dictionary with the selected quote and image
    context = {
        "allQuote": quotesList,
        "allImage": imagesList,
    }

    # delegate redering work to the template
    return render(request, template_name, context)

def about(request):
    '''
    Function to handle the URL request for /about.
    Delegate redering to the template quotes/about.html
    '''

    # use this template to reder the response
    template_name = 'quotes/about.html'

    random_quote = random.choice(quotesList)
    random_image = random.choice(imagesList)

    # Create the context dictionary with the selected quote and image
    context = {
        "quote": random_quote,
        "image": random_image,
    }

    # delegate redering work to the template
    return render(request, template_name, context)

def base(request):
    '''
    Function to handle the URL request for /base.
    Delegate redering to the template quotes/base.html
    '''

    # use this template to reder the response
    template_name = 'quotes/base.html'

    random_quote = random.choice(quotesList)
    random_image = random.choice(imagesList)

    # Create the context dictionary with the selected quote and image
    context = {
        "quote": random_quote,
        "image": random_image,
    }

    # delegate redering work to the template
    return render(request, template_name, context)