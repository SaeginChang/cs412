from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from .models import Recipe, Ingredient, MealPlan, MealPlan, MealPlanRecipe
from .forms import RecipeForm, MealPlanForm, MealPlanRecipeForm, IngredientForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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
    success_url = '/recipes/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'project/recipe_form.html'
    success_url = reverse_lazy('recipe_list')

class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'project/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')

# Ingredient Views
class IngredientListView(ListView):
    model = Ingredient
    template_name = 'project/ingredient_list.html'
    context_object_name = 'ingredients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IngredientForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)
        
# Meal Plan Views
class MealPlanListView(LoginRequiredMixin, ListView):
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
    success_url = '/mealplans/'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class AddRecipesToMealPlanView(CreateView):
    model = MealPlanRecipe
    form_class = MealPlanRecipeForm
    template_name = 'project/add_recipes_to_mealplan.html'

    def form_valid(self, form):
        form.instance.meal_plan_id = self.kwargs['pk']
        return super().form_valid(form)

class UpdateMealPlanView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MealPlan
    form_class = MealPlanForm
    template_name = 'project/mealplan_form.html'
    success_url = '/mealplans/'

    def test_func(self):
        mealplan = self.get_object()
        return self.request.user == mealplan.user # only allow owner to edit

class DeleteMealPlanView(DeleteView):
    model = MealPlan
    template_name = 'project/mealplan_confirm_delete.html'
    success_url = '/mealplans/'

    def test_func(self):
            mealplan = self.get_object()
            return self.request.user == mealplan.user # only allow owner to delete