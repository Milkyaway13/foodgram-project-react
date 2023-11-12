from django.core.exceptions import ValidationError


def validate_username(value):
    """В качестве ника запрещает использовать 'me'."""
    if value == "me":
        raise ValidationError('Запрещенное имя пользователя - "me".')
    return value
