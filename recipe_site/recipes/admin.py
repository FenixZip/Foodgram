from django.contrib import admin
from recipes.models import Category, Ingredient, Recipe, RecipeCategory

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(RecipeCategory)
admin.site.register(Ingredient)


