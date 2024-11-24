from django.urls import path
from . import views

urlpatterns = [
    # Home / Recipe URLs
    path('', views.RecipeListView.as_view(), name='show_all_recipes'),  # Home Page showing all recipes
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='show_recipe'),
    path('recipe/create/', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='update_recipe'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='delete_recipe'),

    # Ingredient URLs
    path('ingredients/', views.IngredientListView.as_view(), name='show_all_ingredients'),

    # Meal Plan URLs
    path('mealplans/', views.MealPlanListView.as_view(), name='show_all_mealplans'),
    path('mealplan/<int:pk>/', views.MealPlanDetailView.as_view(), name='show_mealplan'),

    # Additional Views for Meal Plans
    path('mealplan/create/', views.CreateMealPlanView.as_view(), name='create_mealplan'),
    path('mealplan/<int:pk>/update/', views.UpdateMealPlanView.as_view(), name='update_mealplan'),
    path('mealplan/<int:pk>/delete/', views.DeleteMealPlanView.as_view(), name='delete_mealplan'),
]
