# Generated by Django 3.2.16 on 2023-11-22 16:57

import django.core.validators
import django.db.models.deletion
import django.db.models.expressions
from django.db import migrations, models

import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_subscribe_subscriber'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribe',
            options={'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(help_text='Укажите e-mail', max_length=254, unique=True, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(help_text='Ваше Имя', max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(help_text='Ваша Фамилия', max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(help_text='Укажите логин', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Некорректные символы для логина', regex='^[\\w.@+-]+\\Z'), users.validators.validate_username], verbose_name='Логин'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='author',
            field=models.ForeignKey(help_text='Автор', on_delete=django.db.models.deletion.CASCADE, related_name='subscribing', to='users.customuser'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='subscriber',
            field=models.ForeignKey(help_text='Подписчик автора', on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to='users.customuser'),
        ),
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.CheckConstraint(check=models.Q(('subscriber', django.db.models.expressions.F('author')), _negated=True), name='self_follow'),
        ),
    ]
