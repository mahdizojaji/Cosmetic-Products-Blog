from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from datetime import datetime


@deconstructible
class FutureDateValidator:
    message = _("Enter a Future Date value.")
    code = "invalid-date"

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if isinstance(value, datetime):
            datetime_value = value
            invalid_input = datetime_value < timezone.now()
        elif isinstance(value, int):
            datetime_value = datetime.fromtimestamp(value, tz=timezone.get_current_timezone())
            invalid_input = datetime_value < timezone.now()
        elif isinstance(value, str):
            if not value.isdecimal():
                invalid_input = True
            else:
                datetime_value = datetime.fromtimestamp(int(value), tz=timezone.get_current_timezone())
                invalid_input = datetime_value < timezone.now()
        else:
            invalid_input = True

        if invalid_input:
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        return (
            isinstance(other, FutureDateValidator) and
            (self.message == other.message) and
            (self.code == other.code)
        )
