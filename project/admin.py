# File: admin.py
# Author: Nick Chang (nechang@bu.edu), 12/1/2024
# Registering Models so that they can be managed

from django.contrib import admin
from .models import *

# Register your models here.
# register models so that they can be management
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(MealPlan)
admin.site.register(MealPlanRecipe)
admin.site.register(InstructionStep)