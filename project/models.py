from django.db import models

# Create your models here.
class User(models.Model):
    '''Each of the users that are gonig to be seeing / inputting meals'''
    username = models.CharField(max_length=100)
    email = models.EmailField()
    preferences = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class Recipe(models.Model):
    '''The recipes which is connected to the users and presents the basic summary of how to make'''
    title = models.CharField(max_length=200)
    description = models.TextField()
    cooking_time = models.IntegerField()
    difficulty_level = models.CharField(
        max_length=20, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')]
    )
    instructions = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class Ingredient(models.Model):
    '''Types of ingredients'''
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    '''Measurement of the ingredients'''
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(
        max_length=20, choices=[('grams', 'grams'), ('cups', 'cups'), ('tablespoons', 'tablespoons'), ('slices', 'slices')]
    )

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} in {self.recipe.title}"

class MealPlan(models.Model):
    '''meal plan to plan for future meals'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Meal Plan for {self.date} by {self.user.username}"
    
class MealPlanRecipe(models.Model):
    '''connects mealplan and recipe so that we don't need a many to many connection'''
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    serving_size = models.IntegerField(default=1)
    meal_type = models.CharField(
        max_length=20, choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')]
    )

    def __str__(self):
        return f"{self.meal_type}: {self.recipe.title} ({self.serving_size} servings)"