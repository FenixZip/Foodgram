import random

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm, RecipeIngredientFormSet, RegisterForm
from .models import Recipe


def home(request: HttpRequest) -> HttpResponse:
    """Главная страница сайта."""
    recipes = list(Recipe.objects.all())
    random_recipes = random.sample(recipes, min(len(recipes), 5)) if recipes else []
    return render(request, 'recipes/home.html', {'recipes': random_recipes})


def recipe_detail(request: HttpRequest, recipe_id: int) -> HttpResponse:
    """Подробная информация о рецепте"""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
def add_recipe(request: HttpRequest) -> HttpResponse:
    """Добавление нового рецепта, только для авторизованных юзеров"""
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
            return redirect('home')
    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    return render(request, 'recipes/add_recipe.html', {
        'form': form,
        'formset': formset,
        'edit': False,
    })


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'recipes/register.html', {'form': form})
