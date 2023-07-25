import re

from django.core.exceptions import ValidationError

PATTERN = r'[a-z]+'


def command_validator(value):
    if not re.match(PATTERN, value):
        raise ValidationError('Команда может быть только на латинице')
    return value
