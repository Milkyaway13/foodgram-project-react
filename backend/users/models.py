from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

from .validators import validate_username


class CustomUser(AbstractUser):
    """Кастомная модель юзера."""

    username = models.CharField(
        validators=(
            validators.RegexValidator(
                regex=r"^[\w.@+-]+\Z",
                message="Некорректные символы для логина",
            ),
            validate_username,
        ),
        max_length=150,
        verbose_name="Логин",
        help_text="Укажите логин",
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        verbose_name="E-mail",
        help_text="Укажите e-mail",
        unique=True,
    )
    first_name = models.CharField(
        max_length=150, verbose_name="Имя", help_text="Ваше Имя"
    )
    last_name = models.CharField(
        max_length=150, verbose_name="Фамилия", help_text="Ваша Фамилия"
    )

    REQUIRED_FIELDS = ("username", "first_name", "last_name")
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Модель подписок."""

    subscriber = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="subscriber",
        help_text="Подписчик автора",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="subscribing",
        help_text="Автор",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=("subscriber", "author"), name="unique_follow"
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F("author")),
                name="self_follow",
            ),
        ]

    def __str__(self):
        return f"{self.subscriber} подписался на  {self.author}"
