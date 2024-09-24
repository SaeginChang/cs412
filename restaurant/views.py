## restaurant/views.py
## description: write view functions to handle URL requests for the restaurant app
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

def base(request):
    '''
    Function to handle the URL request for /restaurant base page.
    Delegate redering to the template restaurant/base.html
    '''

    # use this template to reder the response
    template_name = 'restaurant/base.html'

    # create a dictionary of context variables for the template:
    context = {
        "current_time" : time.ctime(),
    }

    # delegate redering work to the template
    return render(request, template_name, context)

def main(request):
    '''
    Function to handle the URL request for /restaurant main page
    Delegate rendering to the template restaurant/main.html
    '''

    template_name = 'restaurant/main.html'

    context = {
        "current_time" : time.ctime(),

    }

    return render(request, template_name, context)

def order(request):
    '''
    Function to handle the URL request for /restaurant order page
    Delegate rendering to the template restaurant/order.html
    '''

    template_name = 'restaurant/order.html'

    context = {
        "current_time" : time.ctime(),

    }

    return render(request, template_name, context)

def confirmation(request):
    '''
    Function to handle the URL request for /restaurant confirmation page
    Delegate rendering to the template restaurant/confirmation.html
    '''

    template_name = 'restaurant/confirmation.html'

    context = {
        "current_time" : time.ctime(),

    }

    return render(request, template_name, context)
