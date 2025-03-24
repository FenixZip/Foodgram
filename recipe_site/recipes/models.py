from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Расширяет модель пользователя полями: описание и аватар."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, verbose_name="О себе")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")

    def __str__(self):
        return f"Профиль: {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаёт профиль пользователя после регистрации."""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()


class Category(models.Model):
    """Категория рецепта: Завтрак, Обед, Ужин."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингредиент для рецепта."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название ингредиента")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Основная модель рецепта."""
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    steps = models.TextField(verbose_name="Шаги приготовления")
    cook_time = models.PositiveIntegerField(verbose_name="Время приготовления (мин)")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="Изображение")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    categories = models.ManyToManyField(Category, through='RecipeCategory', verbose_name="Категории")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """Связь между рецептом и ингредиентами с указанием количества и единицы."""
    UNIT_CHOICES = [
        ('г', 'грамм'),
        ('мл', 'миллилитр'),
        ('шт', 'штука'),
        ('ч.л.', 'ч.л.'),
        ('ст.л.', 'ст.л.'),
    ]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ингредиент")
    amount = models.FloatField(verbose_name="Количество")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='г', verbose_name="Ед. изм.")

    def __str__(self):
        return f"{self.ingredient.name} — {self.amount} {self.unit}"


class RecipeCategory(models.Model):
    """Связующая таблица для рецептов и категорий."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'category')

    def __str__(self):
        return f"{self.recipe.title} → {self.category.name}"
