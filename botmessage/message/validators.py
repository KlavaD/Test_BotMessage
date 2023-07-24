import re

from django.core.exceptions import ValidationError

PATTERN = r'[^\w+[A-a]'


def command_validator(value):
    incorrect = list(set(''.join(re.findall(PATTERN, value))))
    if incorrect:
        raise ValidationError('Команда может быть только на латинице')
    return value
