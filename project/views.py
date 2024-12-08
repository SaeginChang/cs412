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
    '''
    displays list of all recipes
    supports filtering recipes based on a selected ingredient
    '''
    model = Recipe
    template_name = 'project/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        '''
        overrides the default queryset to filter recipes
        based on ingredient from query parameters
        '''
        queryset = super().get_queryset()
        ingredient_filter = self.request.GET.get('ingredient')  # Get the ingredient from query params
        if ingredient_filter:
            queryset = queryset.filter(recipeingredient__ingredient__name__icontains=ingredient_filter)
        return queryset

    def get_context_data(self, **kwargs):
        '''
        adds a list of ingredients to the context for the filter dropdown
        and keeps track of the selected ingredient
        '''
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.all()  # Pass all ingredients for dropdown
        context['selected_ingredient'] = self.request.GET.get('ingredient', '')  # To keep track of the selected ingredient
        return context
    
class RecipeDetailView(DetailView):
    '''
    displays the details of a single recipe, including
    instructions and ingredients
    '''
    model = Recipe
    template_name = 'project/recipe_detail.html'
    context_object_name = 'recipe'

class RecipeCreateView(CreateView):
    '''
    allows authenticated users to create new recipe
    automatically assigns the currently logged-in user as the creator
    '''
    model = Recipe
    form_class = RecipeForm
    template_name = 'project/recipe_form.html'
    success_url = reverse_lazy('recipe_list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        '''
        assigns the current suer as the creator of the recipe
        '''
        form.instance.user = get_user_model().objects.get(pk=self.request.user.pk)
        messages.success(self.request, 'Recipe created successfully')
        return super().form_valid(form)

class RecipeUpdateView(UpdateView):
    '''
    allows user to update a recipe they own
    '''
    model = Recipe
    form_class = RecipeForm
    template_name = 'project/recipe_form.html'
    success_url = reverse_lazy('recipe_list')

class RecipeDeleteView(DeleteView):
    '''
    allows users to delete a recipe they own
    '''
    model = Recipe
    template_name = 'project/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')

class AddIngredientToRecipeView(CreateView):
    '''
    displays a list of all ingredients
    allows users to add a new ingredient 
    '''
    model = RecipeIngredient
    form_class = RecipeIngredientForm
    template_name = 'project/add_ingredient_form.html'

    def form_valid(self, form):
        '''
        checks whether the form is allowed with valid entries
        '''
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_success_url(self):
        ''' 
        where to go once the form is submitted
        '''
        return reverse('recipe_detail', kwargs={'pk': self.kwargs['recipe_pk']})
    
    def get_context_data(self, **kwargs):
        '''
        adds an empty form for adding a new ingredient
        '''
        context = super().get_context_data(**kwargs)
        context['recipe'] = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        return context


# Instruction Views
class AddInstructionStepView(CreateView):
    '''
    add a new instruction step to a recipe
    automatically assigns the correct recipe and increments the step number
    '''
    model = InstructionStep
    fields = ['description']
    template_name = 'project/instruction_form.html'

    def get_context_data(self, **kwargs):
        '''
        add the parent recipe object to the context for use in the template
        '''
        context = super().get_context_data(**kwargs)
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        context['recipe'] = recipe
        return context

    def form_valid(self, form):
        '''
        assigns the parent recipe to the instruction step
        auto increments step number
        '''
        # Assign the recipe to the instruction step
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        form.instance.recipe = recipe

        # Auto-increment the step number
        last_step = InstructionStep.objects.filter(recipe=recipe).order_by('step_number').last()
        next_step_number = last_step.step_number + 1 if last_step else 1
        form.instance.step_number = next_step_number

        return super().form_valid(form)

    def get_success_url(self):
        '''
        redirect after form is successfully filled to recipe detail page
        '''
        return reverse_lazy('recipe_detail', kwargs={'pk': self.kwargs['recipe_pk']})

    
class UpdateInstructionStepView(UpdateView):
    '''
    update an existing instruction step for a recipe
    allows users to edit step number and description
    '''
    model = InstructionStep
    fields = ['step_number', 'description']
    template_name = 'project/instruction_form.html'

    def get_context_data(self, **kwargs):
        '''
        parent recipe to the context to use in template
        '''
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object.recipe  # Add the related recipe to the context
        return context

    def get_success_url(self):
        '''
        redirect to recipe detail page after updating step
        '''
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk})
    
class DeleteInstructionStepView(DeleteView):
    '''
    delete an existing instruction step from a recipe
    '''
    model = InstructionStep
    template_name = 'project/instruction_confirm_delete.html'
    
    def get_success_url(self) -> str:
        '''
        redirect to recipe detail page after successfully deleting step
        '''
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.recipe.pk})

# Ingredient Views
class IngredientListView(ListView):
    '''
    displays a list of all ingredients
    allows users to add a new ingredient with a form
    '''
    model = Ingredient
    template_name = 'project/ingredient_list.html'
    context_object_name = 'ingredients'

    def get_context_data(self, **kwargs):
        '''
        adds an empty form for creating a new ingredient
        '''
        context = super().get_context_data(**kwargs)
        context['form'] = IngredientForm()
        return context
    
    def post(self, request, *args, **kwargs):
        '''
        handles creation of a new ingredient when form is submitted
        '''
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)
        
# Meal Plan Views
class MealPlanListView(LoginRequiredMixin, ListView):
    '''
    displays list of all meal plans for the logged in user
    redirects unauthorized users to the login page
    '''
    model = MealPlan
    template_name = 'project/mealplan_list.html'
    context_object_name = 'mealplans'

    def dispatch(self, request, *args, **kwargs):
        '''
        if unauthorized, takes them to please login page
        '''
        if not request.user.is_authenticated:
            return render(request, 'project/please_login.html')
        return super().dispatch(request, *args, **kwargs)

class MealPlanDetailView(DetailView):
    '''
    displays the details of a single meal plan, including its recipes
    '''
    model = MealPlan
    template_name = 'project/mealplan_detail.html'
    context_object_name = 'mealplan'

    def dispatch(self, request, *args, **kwargs):
        '''
        if not authorized, takes to please login page
        '''
        if not request.user.is_authenticated:
            return render(request, 'project/please_login.html') 
        return super().dispatch(request, *args, **kwargs)

class CreateMealPlanView(LoginRequiredMixin, CreateView):
    '''
    allows logged in users to create a new meal plan
    '''
    model = MealPlan
    form_class = MealPlanForm
    template_name = 'project/mealplan_form.html'
    success_url = reverse_lazy('mealplan_list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        '''
        assigns the current user as the owner of the meal plan
        '''
        form.instance.user = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        '''
        if not logged in, takes to please login page
        '''
        if not request.user.is_authenticated:
            return render(request, 'project/please_login.html') 
        return super().dispatch(request, *args, **kwargs)
    
class AddRecipesToMealPlanView(CreateView):
    '''
    add a new instruction step to a meal plan
    allows users to associate a recipe with a mealplan
    '''
    model = MealPlanRecipe
    form_class = MealPlanRecipeForm
    template_name = 'project/add_recipes_to_mealplan.html'

    def form_valid(self, form):
        '''
        assigns mealplan ID from url to the form instance
        makes sure the recipe is linked to the correct meal plan
        '''
        form.instance.meal_plan_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        '''
        redirect back to mealplan detail page after adding in a recipe
        '''
        return reverse('show_mealplan', kwargs={'pk': self.kwargs['pk']})

class UpdateMealPlanView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    update an existing mealplan
    only owner of mealplan can edit
    '''
    model = MealPlan
    form_class = MealPlanForm
    template_name = 'project/mealplan_form.html'
    success_url = reverse_lazy('mealplan_list')

    def test_func(self):
        '''
        makes sure only owner of mealplan can access
        '''
        mealplan = self.get_object()
        return self.request.user == mealplan.user # only allow owner to edit

    def handle_no_permission(self):
        '''
        if unauthorized
        redirects to no permissions page
        '''
        # Redirect to a custom page when the user doesn't have permission
        if self.request.user.is_authenticated:
            return redirect('custom_no_permission')  # Use a named URL for your custom page
        return super().handle_no_permission()  # Default behavior for non-authenticated users

class DeleteMealPlanView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''
    delete an existing meal plan
    only owner can delete
    '''
    model = MealPlan
    template_name = 'project/mealplan_confirm_delete.html'
    success_url = reverse_lazy('mealplan_list')

    def test_func(self):
            '''
            only owner of meal plan can access
            '''
            mealplan = self.get_object()
            return self.request.user == mealplan.user # only allow owner to delete
    
    def handle_no_permission(self):
        '''
        redirect users to a no permissions page if not authorized'''
        # Redirect to a custom page when the user doesn't have permission
        if self.request.user.is_authenticated:
            return redirect('custom_no_permission')  # Use a named URL for your custom page
        return super().handle_no_permission()  # Default behavior for non-authenticated users
    
class MealPlanWeeklyView(LoginRequiredMixin, TemplateView):
    '''
    displays weekly view of mealplans grouped by day
    only accessible to logged in users
    '''
    template_name = "project/mealplan_weekly.html"

    def get_context_data(self, **kwargs):
        '''
        grabs all meal plans for the current week and groups
        '''
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
        '''
        if not logged in, takes to please login page
        '''
        if not request.user.is_authenticated:
            return render(request, 'project/please_login.html') 
        return super().dispatch(request, *args, **kwargs)

# Login Authentication Helper
class CustomLoginView(LoginView):
    '''
    custom login view to redirect users to the recipe list after logging in
    '''
    template_name = 'project/login.html'

    def get_success_url(self) -> str:
        '''
        redirect to the recipe list after a successful login
        '''
        return self.request.GET.get('next') or reverse('recipe_list')
    
# User Creation / Delete
def register_user(request):
    '''
    handles user registration
    '''
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
    '''
    allows users to delete their account
    '''
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted')
        return redirect('login')
    return render(request, 'project/delete_user.html')

class NoPermissionView(TemplateView):
    '''
    if they are not logged in correctly for specific pages
    '''
    template_name = "project/no_permission.html"
