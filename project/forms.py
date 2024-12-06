from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time', 'difficulty_level', 'user']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class InstructionStepForm(forms.ModelForm):
    class Meta:
        model = InstructionStep
        fields = ['step_number', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['user', 'date'] 
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class MealPlanRecipeForm(forms.ModelForm):
    class Meta:
        model = MealPlanRecipe
        fields = ['recipe', 'serving_size']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']
        widgets = {
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
            'unit': forms.Select(attrs={'placeholder': 'Select unit'}),
        }
