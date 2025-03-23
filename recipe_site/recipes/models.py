from django.db import models


class Category(models.Model):
    """Модель для хранения категорий: завтрак, обед, ужин"""
    name = models.CharField(
                            max_length=100,
                            unique=True, db_index=True,
                            verbose_name='Название категории')

    def __str__(self):
        """Отображение категорие по ее названию"""
        return f'Категория -> {self.name}'
