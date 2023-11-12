from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators

from .validators import validate_username


class CustomUser(AbstractUser):
    """Кастомная модель юзера."""

    username = models.CharField(
        validators=(
            validators.RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Некорректные символы для логина',
            ),
            validate_username
        ),
        max_length=150,
        verbose_name='Логин',
        help_text='Укажите логин',
        unique=True,
        null=False,
        blank=True,
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='E-mail',
        help_text='Укажите e-mail',
        null=False,
        blank=True,
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Ваше Имя',
        blank=True,
        null=False,
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Ваша Фамилия',
        blank=True,
        null=False,
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        help_text='Введите пароль',
        blank=False,
        null=False,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    '''Модель подписок. '''
    subscriber = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriber',
        null=True,
        help_text="Подписчик автора",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribing',
        null=True,
        help_text="Автор",
    )

    class Meta:
        verbose_name = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('subscriber', 'author'), name='unique_follow')
        ]

    def __str__(self):
        return f'{self.subscriber} подписался на  {self.author}'
