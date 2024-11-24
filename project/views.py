from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Recipe, Ingredient, MealPlan
from .forms import RecipeForm, MealPlanForm

# Recipe Views
class RecipeListView(ListView):
    model = Recipe
    template_name = 'project/recipe_list.html'
    context_object_name = 'recipes'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'project/recipe_form.html'
    success_url = reverse_lazy('show_all_recipes')

class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'project/recipe_form.html'
    success_url = reverse_lazy('show_all_recipes')

class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'project/recipe_confirm_delete.html'
    success_url = reverse_lazy('show_all_recipes')

# Ingredient Views
class IngredientListView(ListView):
    model = Ingredient
    template_name = 'project/ingredient_list.html'
    context_object_name = 'ingredients'

# Meal Plan Views
class MealPlanListView(ListView):
    model = MealPlan
    template_name = 'project/mealplan_list.html'
    context_object_name = 'mealplans'

class MealPlanDetailView(DetailView):
    model = MealPlan
    template_name = 'project/mealplan_detail.html'
    context_object_name = 'mealplan'

class CreateMealPlanView(CreateView):
    model = MealPlan
    form_class = MealPlanForm
    template_name = 'project/mealplan_form.html'
    success_url = reverse_lazy('show_all_mealplans')

class UpdateMealPlanView(UpdateView):
    model = MealPlan
    form_class = MealPlanForm
    template_name = 'project/mealplan_form.html'
    success_url = reverse_lazy('show_all_mealplans')

class DeleteMealPlanView(DeleteView):
    model = MealPlan
    template_name = 'project/mealplan_confirm_delete.html'
    success_url = reverse_lazy('show_all_mealplans')
