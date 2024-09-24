from django.shortcuts import render

# Create your views here.

def show_form(request):
    '''
    Show the contact form.
    '''
    
    template_name = "formadata/form.html"
    return render(request, template_name)