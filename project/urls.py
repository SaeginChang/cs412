from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logout.html'), name='logout'),

    # Home / Recipe URLs
    path('', views.RecipeListView.as_view(), name='recipe_list'),  # Home Page showing all recipes
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='show_recipe'),
    path('recipe/create/', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='update_recipe'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='delete_recipe'),

    # Ingredient URLs
    path('ingredients/', views.IngredientListView.as_view(), name='show_all_ingredients'),

    # Meal Plan URLs
    path('mealplans/', views.MealPlanListView.as_view(), name='mealplan_list'),
    path('mealplan/<int:pk>/', views.MealPlanDetailView.as_view(), name='show_mealplan'),

    # Additional Views for Meal Plans
    path('mealplan/create/', views.CreateMealPlanView.as_view(), name='create_mealplan'),
    path('mealplan/<int:pk>/update/', views.UpdateMealPlanView.as_view(), name='update_mealplan'),
    path('mealplan/<int:pk>/delete/', views.DeleteMealPlanView.as_view(), name='delete_mealplan'),
    path('mealplan/<int:pk>/add-recipes/', views.AddRecipesToMealPlanView.as_view(), name='add_recipes_to_mealplan'),
]
