from django.contrib.auth.models import User
from django.forms import forms

from recipes.models import Recipe


class RecipeForm(forms.Form):
    """Форма для создания и редактирования рецептов"""
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'cook_time', 'image', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        """
        Расширяем конструктор для настройки полей формы.
        Можно добавить классы CSS, плейсхолдеры и т.п.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class RegisterForm(forms.Form):
    """
    Форма для регистрации нового пользователя.
    Расширяет встроенную форму UserCreationForm.
    """
    email = forms.EmailField(required=True, help_text="Укажите действительный email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Поля формы регистрации

    def __init__(self, *args, **kwargs):
        """
        Расширяем конструктор для добавления классов к полям.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'