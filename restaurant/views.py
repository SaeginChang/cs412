## restaurant/views.py
## description: write view functions to handle URL requests for the restaurant app
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import time
import random
from datetime import datetime

daily_specials = {
    "Monday": {
        "name": "Rice and Chicken",
        "price": 20.99,
        "description": "Breast chicken with white jasmine rice"
    },
    "Tuesday": {
        "name": "Vegetables",
        "price": 8.99,
        "description": "A healthy mix of fresh vegetables wrapped in a whole wheat tortilla."
    },
    "Wednesday": {
        "name": "BBQ Ribs",
        "price": 14.99,
        "description": "Served with coleslaw and cornbread."
    },
    "Thursday": {
        "name": "Spaghetti Bolognese",
        "price": 12.99,
        "description": "Traditional Italian pasta with a rich meat sauce."
    },
    "Friday": {
        "name": "Fish Tacos",
        "price": 11.99,
        "description": "Three fish tacos served with salsa and lime."
    },
    "Saturday": {
        "name": "Steak and Eggs",
        "price": 16.99,
        "description": "A grilled steak with two eggs cooked to order."
    },
    "Sunday": {
        "name": "Pancake Breakfast",
        "price": 7.99,
        "description": "Stack of pancakes served with syrup and butter."
    }
}

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

def show_order(request):
    '''
    Function to handle the URL request for /restaurant order page
    Delegate rendering to the template restaurant/order.html
    '''

    current_day = datetime.now().strftime("%A")

    daily_special = daily_specials.get(current_day, {
        "name": "Chef's Choice",
        "price": 10.00,
        "description": "Ask the Chef :)"
    })

    template_name = 'restaurant/order.html'

    context = {
        'daily_special':daily_special

    }

    return render(request, template_name, context)

def submit(request):
    '''
    Handle the form submission.
    Read the form data from the request,
    and send it back to a template
    '''

    template_name = 'restaurant/confirmation.html'

    if request.POST:
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']

        context = {
            'name' : name,
            'price' : price,
            'description' : description,
        }

        return render(request, template_name, context)
    
    return redirect("show_order")