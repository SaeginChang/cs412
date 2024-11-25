# Generated by Django 5.1.3 on 2024-11-25 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_remove_mealplan_recipes_mealplanrecipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.user'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='unit',
            field=models.CharField(choices=[('grams', 'grams'), ('cups', 'cups'), ('tablespoons', 'tablespoons'), ('slices', 'slices')], max_length=20),
        ),
    ]