from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RecipeForm(forms.ModelForm):
    '''
    Form for recipe model to allow users to create or update a recipe
    includes fields that allow user to know what the recipe is and if they want to use it
    '''
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time', 'difficulty_level', 'user']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class InstructionStepForm(forms.ModelForm):
    '''
    Form for insturctionstep model to create or update steps in a recipe
    includes fields that say number and description
    '''
    class Meta:
        model = InstructionStep
        fields = ['step_number', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MealPlanForm(forms.ModelForm):
    '''
    form for mealplan model to create or update a meal plan
    fields include user and date
    '''
    class Meta:
        model = MealPlan
        fields = ['user', 'date'] 
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class MealPlanRecipeForm(forms.ModelForm):
    '''
    form for MealPlanRecipe model to link a recipe to a mealplan
    fields include recipe and serving_size
    '''
    class Meta:
        model = MealPlanRecipe
        fields = ['recipe', 'serving_size']

class IngredientForm(forms.ModelForm):
    '''
    form for ingredient Model to add or update an ingredient
    fields include the name
    '''
    class Meta:
        model = Ingredient
        fields = ['name']

class UserRegisterForm(UserCreationForm):
    '''
    form for user registration using Django's built in User model
    Username, email, and password'''
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RecipeIngredientForm(forms.ModelForm):
    '''
    form for RecipeIngredient model to associate an ingredient with a recipe
    Ingredient, quantity, and unit
    '''
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']
        widgets = {
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
            'unit': forms.Select(attrs={'placeholder': 'Select unit'}),
        }
