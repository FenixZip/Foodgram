from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """Модель для хранения категорий: завтрак, обед, ужин"""
    name = models.CharField(
        max_length=100,
        unique=True, db_index=True,
        verbose_name="Название категории")

    def __str__(self):
        """Отображение категорие по ее названию"""
        return f'Категория -> {self.name}'


class Recipe(models.Model):
    """Модель для хранения рецептов.
    Рецепт может иметь несколько категорий (через связь ManyToMany)
    """
    title = models.CharField(max_length=100, null=False, blank=False,
                             verbose_name="Название рецепта")
    description = models.TextField(max_length=100, verbose_name="Описание")
    steps = models.TextField(verbose_name="Шаги приготовления")
    cook_time = models.PositiveIntegerField(
                                        help_text="Укажите время в минутах",
                                        verbose_name="Время приготовления")
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True,
                                verbose_name="Изображение")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes",
                                verbose_name="Автор")
    categories = models.ManyToManyField('Category', through='RecipeCategory',
                                        verbose_name="Категории")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        """Отображение рецепта по его названию"""
        return f'Название рецепта -> {self.title}'


class RecipeCategory(models.Model):
    """Модель для связи рецептов и категорий"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        """Отображение связи в админке: Бульон-суп"""
        return f'Связь {self.recipe.title} -> {self.category.name} '
