from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User, Recipe, Ingredient, MealPlan, MealPlanRecipe
from .forms import RecipeForm


class RecipeListView(ListView):
    model = Recipe
    template_name = 'project/recipe_list.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'

class IngredientListView(ListView):
    model = Ingredient
    template_name = 'project/ingredient_list.html'
    context_object_name = 'ingredients'

class MealPlanListView(ListView):
    model = MealPlan
    template_name = 'project/mealplan_list.html'
    context_object_name = 'mealplans'

class MealPlanDetailView(DetailView):
    model = MealPlan
    template_name = 'project/mealplan_detail.html'
    context_object_name = 'mealplan'

# Create, Update, and Delete Views

class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'project/recipe_form.html'
    success_url = reverse_lazy('recipe_list')

class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'project/recipe_form.html'
    success_url = reverse_lazy('recipe_list')

class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'project/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')

