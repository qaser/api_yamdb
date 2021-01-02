from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MaxValueValidator(BaseValidator):
    message = _('Значение должно быть не выше %(limit_value)s.')
    code = 'max_value'

    def compare(self, a, b):
        return a > b


@deconstructible
class MinValueValidator(BaseValidator):
    message = _('Значение должно быть не ниже %(limit_value)s.')
    code = 'min_value'

    def compare(self, a, b):
        return a < b
