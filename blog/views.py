# blog/views.py
# define the views for the blog app
from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import * ## import the models (e.g., Article)

import random

# class-based view
class ShowAllView(ListView):
    '''the view to show all Articles'''

    model = Article #the model to display
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # this is the context variable to use in the template

class RandomArticleView(DetailView):
    """Display one article selected at random"""
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    # AttributeError: Generic detail view RandomArticleView must be called with either an object pk or a slug in the URLconf.
    # one olution implement get_object method
    def get_object(self):
        """Return one article chosen at random."""

        # retrieve all of the articles
        all_articles = Article.objects.all()
        #pick one at random
        article = random.choice(all_articles)
        return article
    
class ArticleView(DetailView):
    """display one article selected by PK"""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"