from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.


class Profile(models.Model):
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True, verbose_name="Аватар")
    gitprofile = models.URLField(null=True, blank=True, verbose_name='Профиль на GitHub', max_length=50)
    about_me = models.TextField(null=True, blank=True, verbose_name="О себе", max_length=500)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь", related_name="profile")
