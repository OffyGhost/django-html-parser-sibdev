from django.core.exceptions import ValidationError
from django.utils import timezone


def only_future_time(date):
    if date < timezone.now():
        raise ValidationError("Можно указывать только будующее время!")
