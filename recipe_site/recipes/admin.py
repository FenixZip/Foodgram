from django.contrib import admin

from .models import (Category, Ingredient, Recipe, RecipeCategory,
                     RecipeIngredient, UserProfile)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'cook_time', 'created_at')
    list_filter = ('categories', 'cook_time')
    search_fields = ('title', 'description', 'author__username')
    # filter_horizontal = ('categories',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount', 'unit')
    list_filter = ('unit',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)
