from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from datetime import datetime
from rest_framework import serializers


class TimestampField(serializers.Field):
    default_error_messages = {
        'invalid-date': _('Timestamp is not valid.'),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            data = int(data)
            if data <= 0:
                raise ValueError
        except (ValueError, TypeError):
            self.fail('invalid-date')
        return datetime.fromtimestamp(int(data), tz=timezone.get_current_timezone())

    def to_representation(self, value):
        return int(value.strftime("%s"))
