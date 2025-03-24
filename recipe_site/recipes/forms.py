from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import Recipe, RecipeIngredient, UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar')
        labels = {
            'bio': 'О себе',
            'avatar': 'Аватар',
        }


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'cook_time', 'image', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'steps': 'Шаги приготовления',
            'cook_time': 'Время приготовления (мин)',
            'image': 'Изображение',
            'categories': 'Категории',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RegisterForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя.
    """
    username = forms.CharField(label="Имя пользователя",
                               help_text="До 150 символов. Только буквы, цифры и символы @/./+/-/_")
    email = forms.EmailField(label="Email", help_text="Укажите действительный email")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput, help_text="""
            Пароль должен содержать не менее 8 символов, не быть слишком простым или полностью цифровым.
        """)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput,
                                help_text="Введите пароль ещё раз.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'amount', 'unit']
        labels = {
            'ingredient': 'Ингредиент',
            'amount': 'Количество',
            'unit': 'Единица',
        }


RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True
)
