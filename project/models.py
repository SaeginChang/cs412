from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Recipe(models.Model):
    '''
    Recipe model is for the cooking recipes created by users
    each recipe is made by a user and contains all of the necessary information
    to understand what the recipe is
    '''
    title = models.CharField(max_length=200)
    description = models.TextField()
    cooking_time = models.IntegerField()
    difficulty_level = models.CharField(
        max_length=20, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')]
    )
    # for the user who created the recipe, set_null makes sure that the recipe is still there even if the user is deleted
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recipes')

    def __str__(self):
        return self.title
    
class InstructionStep(models.Model):
    '''
    instructions for the recipe
    '''
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps")
    step_number = models.PositiveIntegerField()
    description = models.TextField()

    class Meta:
        # making sure that the steps appear in order by step_number
        ordering = ['step_number']

        def __str__(self):
            return f"Step {self.step_number} for {self.recipe.title}"


class Ingredient(models.Model):
    '''Types of ingredients'''
    # unique is to make sure there are no repeats of ingredients
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    '''
    connects recipes to the ingredients
    specifies quantity and unit of each ingredient in a recipe
    '''
    # assoociated recipe
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # associated ingredient
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(
        max_length=20, choices=[('grams', 'grams'), ('cups', 'cups'), ('tablespoons', 'tablespoons'), ('slices', 'slices')]
    )

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name} in {self.recipe.title}"

class MealPlan(models.Model):
    '''meal plan to plan for future meals
    linked to date and user'''
    # user that created the mealplan
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"Meal Plan for {self.date} by {self.user.username}"
    
class MealPlanRecipe(models.Model):
    '''connects mealplan and recipe so that we don't need a many to many connection
    allows sepcific recipes to a mealplan with additional details like 
    serving size and meal type'''
    # associated meal plan
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    # associated recipe
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    serving_size = models.IntegerField(default=1)
    meal_type = models.CharField(
        max_length=20,
        choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snack', 'Snack')]
    )

    def __str__(self):
        recipe_title = self.recipe.title if self.recipe else "No Recipe"
        servings = f"{self.serving_size} servings" if self.serving_size else "No serving size"
        return f"{recipe_title} ({servings})"