from django import forms
from .models import *

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time', 'difficulty_level', 'instructions', 'user']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'instructions': forms.Textarea(attrs={'rows': 6}),
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