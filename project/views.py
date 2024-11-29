from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy, reverse
from .models import *
from .forms import *
from django.shortcuts import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


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
    success_url = reverse_lazy('recipe_list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = get_user_model().objects.get(pk=self.request.user.pk)
        messages.success(self.request, 'Recipe created successfully')
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

# Instruction Views
class AddInstructionStepView(CreateView):
    model = InstructionStep
    fields = ['step_number', 'description']
    template_name = 'project/instruction_form.html'

    def form_valid(self, form):
        form.instance.recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Add the recipe to the context
        context = super().get_context_data(**kwargs)
        context['recipe'] = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        return context
    
    def get_success_url(self) -> str:
        return reverse_lazy('recipe_detail', kwargs={'pk': self.kwargs['recipe_pk']})
    
class UpdateInstructionStepView(UpdateView):
    model = InstructionStep
    fields = ['step_number', 'description']
    template_name = 'project/instruction_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object.recipe  # Add the related recipe to the context
        return context

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk})
    
class DeleteInstructionStepView(DeleteView):
    model = InstructionStep
    template_name = 'project/instruction_confirm_delete.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk})

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
    success_url = reverse_lazy('mealplan_list')

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

    def get_success_url(self):
        return reverse('show_mealplan', kwargs={'pk': self.kwargs['pk']})

class UpdateMealPlanView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MealPlan
    form_class = MealPlanForm
    template_name = 'project/mealplan_form.html'
    success_url = reverse_lazy('mealplan_list')

    def test_func(self):
        mealplan = self.get_object()
        return self.request.user == mealplan.user # only allow owner to edit

class DeleteMealPlanView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MealPlan
    template_name = 'project/mealplan_confirm_delete.html'
    success_url = reverse_lazy('mealplan_list')

    def test_func(self):
            mealplan = self.get_object()
            return self.request.user == mealplan.user # only allow owner to delete
    

# Login Authentication Helper
class CustomLoginView(LoginView):
    template_name = 'project/login.html'

    def get_success_url(self) -> str:
        return self.request.GET.get('next') or reverse('recipe_list')
    
# User Creation / Delete
def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'project/register.html', {'form': form})

def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted')
        return redirect('login')
    return render(request, 'project/delete_user.html')