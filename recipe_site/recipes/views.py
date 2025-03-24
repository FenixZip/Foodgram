from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm, RegisterForm, RecipeIngredientFormSet
from .models import Recipe
import random


def home(request: HttpRequest) -> HttpResponse:
    """Главная страница сайта"""
    recipes = list(Recipe.objects.all())
    random_recipes = random.sample(recipes, min(len(recipes), 5)) if recipes else []
    return render(request, 'recipes/home.html', {'recipes': random_recipes})


def recipe_detail(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """
    Подробная информация о рецепте.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
def add_recipe(request: HttpRequest) -> HttpResponse:
    """Добавление нового рецепта."""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            form.save_m2m()
            formset.instance = recipe
            formset.save()
            return redirect('recipes:home')
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    return render(request, 'recipes/add_recipe.html', {
        'form': form,
        'formset': formset,
        'edit': False,
    })


@login_required
def delete_recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """Удаление рецепта"""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author != request.user:
        return redirect('recipes:home')

    if  request.method == 'POST':
        recipe.delete()
        return redirect('recipes:profile')

    return render(request, 'recipes/delete_confirm.html', {'recipe': recipe})


def register_view(request: HttpRequest) -> HttpResponse:
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipes:home')
    else:
        form = RegisterForm()
    return render(request, 'recipes/register.html', {'form': form})


@login_required
def edit_recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """Редактирование рецепта. Доступно только автору рецепта."""
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author:
        return redirect('recipes:home')

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, instance=recipe)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('recipes:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(instance=recipe)

    return render(request, 'recipes/add_recipe.html', {
        'form': form,
        'formset': formset,
        'edit': True
    })


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """Страница профиля пользователя"""
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'recipes/profile.html', {'recipes': user_recipes})


def user_profile_view(request, username):
    """
    Публичная страница пользователя. Показывает все его рецепты.
    """
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=user).order_by('-created_at')
    return render(request, 'recipes/user_profile.html', {
        'recipes': recipes,
        'profile_user': user
    })