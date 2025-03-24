from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Расширенный профиль пользователя (аватар + описание)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")

    def __str__(self):
        """Отображение"""
        return f"Профиль пользователя {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


class Category(models.Model):
    """Модель для хранения категорий: завтрак, обед, ужин"""
    name = models.CharField(
        max_length=100,
        unique=True, db_index=True,
        verbose_name="Название категории")

    def __str__(self):
        """Отображение категорие по ее названию"""
        return f'Категория -> {self.name}'


class Ingredient(models.Model):
    """Ингредиенты"""
    name = models.CharField(max_length=100, verbose_name="Название ингредиента")

    def __str__(self):
        return f'Название ингредиента -> {self.name}'


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


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, verbose_name="Количество")

    def __str__(self):
        return f"{self.ingredient.name} — {self.amount}"


class RecipeCategory(models.Model):
    """Модель для связи рецептов и категорий"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Рецепт")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        """Отображение связи в админке: Бульон-суп"""
        return f'Связь {self.recipe.title} -> {self.category.name} '
