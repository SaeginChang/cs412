from django import forms
from .models import Recipe, MealPlan

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
        fields = ['user', 'date']  # Only include fields directly in the MealPlan model
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }