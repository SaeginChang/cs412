from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import *
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
from collections import defaultdict
from datetime import datetime, timedelta
from django.utils.timezone import now

# Recipe Views
class RecipeListView(ListView):
    model = Recipe
    template_name = 'project/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = super().get_queryset()
        ingredient_filter = self.request.GET.get('ingredient')  # Get the ingredient from query params
        if ingredient_filter:
            queryset = queryset.filter(recipeingredient__ingredient__name__icontains=ingredient_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()  # Pass all ingredients for dropdown
        context['selected_ingredient'] = self.request.GET.get('ingredient', '')  # To keep track of the selected ingredient
        return context
    
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

class AddIngredientToRecipeView(CreateView):
    model = RecipeIngredient
    form_class = RecipeIngredientForm
    template_name = 'project/add_ingredient_form.html'

    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.kwargs['recipe_pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        return context


# Instruction Views
class AddInstructionStepView(CreateView):
    model = InstructionStep
    fields = ['description']
    template_name = 'project/instruction_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        context['recipe'] = recipe
        return context

    def form_valid(self, form):
        # Assign the recipe to the instruction step
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        form.instance.recipe = recipe

        # Auto-increment the step number
        last_step = InstructionStep.objects.filter(recipe=recipe).order_by('step_number').last()
        next_step_number = last_step.step_number + 1 if last_step else 1
        form.instance.step_number = next_step_number

        return super().form_valid(form)

    def get_success_url(self):
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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'project/please_login.html')
        return super().dispatch(request, *args, **kwargs)

class MealPlanDetailView(DetailView):
    model = MealPlan
    template_name = 'project/mealplan_detail.html'
    context_object_name = 'mealplan'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'project/please_login.html') 
        return super().dispatch(request, *args, **kwargs)

class CreateMealPlanView(LoginRequiredMixin, CreateView):
    model = MealPlan
    form_class = MealPlanForm
    template_name = 'project/mealplan_form.html'
    success_url = reverse_lazy('mealplan_list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'project/please_login.html') 
        return super().dispatch(request, *args, **kwargs)
    
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

    def handle_no_permission(self):
        # Redirect to a custom page when the user doesn't have permission
        if self.request.user.is_authenticated:
            return redirect('custom_no_permission')  # Use a named URL for your custom page
        return super().handle_no_permission()  # Default behavior for non-authenticated users

class DeleteMealPlanView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MealPlan
    template_name = 'project/mealplan_confirm_delete.html'
    success_url = reverse_lazy('mealplan_list')

    def test_func(self):
            mealplan = self.get_object()
            return self.request.user == mealplan.user # only allow owner to delete
    
    def handle_no_permission(self):
        # Redirect to a custom page when the user doesn't have permission
        if self.request.user.is_authenticated:
            return redirect('custom_no_permission')  # Use a named URL for your custom page
        return super().handle_no_permission()  # Default behavior for non-authenticated users
    
class MealPlanWeeklyView(LoginRequiredMixin, TemplateView):
    template_name = "project/mealplan_weekly.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()

        # Calculate the start and end of the current week
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Initialize all days of the week
        all_days = [start_of_week + timedelta(days=i) for i in range(7)]
        weekly_meals = {day.strftime("%A"): [] for day in all_days}

        # Fetch meal plans and group them by the day of the week
        mealplans = MealPlan.objects.filter(
            user=self.request.user,
            date__gte=start_of_week,
            date__lte=end_of_week
        )
        for mealplan in mealplans:
            day_name = mealplan.date.strftime("%A")
            meals = MealPlanRecipe.objects.filter(meal_plan=mealplan)
            weekly_meals[day_name].extend(meals)

        # Pass the ordered weekly meals
        context["weekly_meals"] = weekly_meals
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'project/please_login.html') 
        return super().dispatch(request, *args, **kwargs)

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

class NoPermissionView(TemplateView):
    template_name = "project/no_permission.html"
