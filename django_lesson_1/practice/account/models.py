from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    """Определяем кастомную таблицу для юзера"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('/')


class Author(User):
    """Пример работы со стандартной таблицей Джанго"""
    class Meta:
        proxy = True

    def __str__(self):
        return self.username


