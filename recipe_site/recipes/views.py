
import random

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (RecipeForm, RecipeIngredientFormSet, RegisterForm,
                    UserProfileForm)
from .models import Recipe, UserProfile


def home(request: HttpRequest) -> HttpResponse:
    """Главная страница сайта — отображает до 5 случайных рецептов."""
    recipes = list(Recipe.objects.all())
    random_recipes = random.sample(recipes, min(len(recipes), 5)) if recipes else []
    return render(request, 'recipes/home.html', {'recipes': random_recipes})


def recipe_detail(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """Подробная страница рецепта."""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
def add_recipe(request: HttpRequest) -> HttpResponse:
    """
    Добавление нового рецепта:
    - Авторизованный пользователь
    - Поддержка ингредиентов (formset)
    """
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
def edit_recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """Редактирование рецепта, только автор может редактировать."""
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
        'edit': True,
    })


@login_required
def delete_recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """Удаление рецепта (только автор)."""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author != request.user:
        return redirect('recipes:home')

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipes:profile')

    return render(request, 'recipes/delete_confirm.html', {'recipe': recipe})


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    """Страница профиля пользователя (авторизованного)."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'recipes/profile.html', {'recipes': recipes, 'profile': profile})


@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    """Редактирование профиля: описание и аватар."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('recipes:profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'recipes/edit_profile.html', {'form': form})


def user_profile_view(request: HttpRequest, username: str) -> HttpResponse:
    """Публичный профиль пользователя: список его рецептов."""
    user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    recipes = Recipe.objects.filter(author=user).order_by('-created_at')
    return render(request, 'recipes/user_profile.html', {
        'recipes': recipes,
        'profile_user': user,
        'profile': profile,
    })


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
