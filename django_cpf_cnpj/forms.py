from django.forms.fields import CharField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from django.core import validators

from django_cpf_cnpj.validators import validate_cpf, validate_cnpj
from django_cpf_cnpj.widgets import CPFWidget, CNPJWidget
from django_cpf_cnpj.cpf import cpf_to_python
from django_cpf_cnpj.cnpj import cnpj_to_python


__all__ = ['CPFForm', 'CNPJForm']


class CPFForm(CharField):
    default_validators = [validate_cpf]

    def __init__(self, *args, masked=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = CPFWidget()
        self.masked = getattr(settings, 'CPF_MASKED', None) or masked

        if 'invalid' not in self.error_messages:
            if masked:
                example_number = '012.345.678-90'
                error_message = _(f'Enter a valid cpf number (e.g. {example_number})')
            else:
                example_number = '01234567890'
                error_message = _(f'Enter a valid cpf number (e.g. {example_number}).')

            self.error_messages['invalid'] = format_lazy(
                error_message, example_number=example_number
            )

    def to_python(self, value):
        cpf = cpf_to_python(value)

        if cpf in validators.EMPTY_VALUES:
            return self.empty_value

        if cpf and not cpf.is_valid():
            raise ValidationError(self.error_messages['invalid'])

        return cpf


class CNPJForm(CharField):
    default_validators = [validate_cnpj]

    def __init__(self, *args, masked=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = CNPJWidget()
        self.masked = getattr(settings, 'CNPJ_MASKED', None) or masked

        if 'invalid' not in self.error_messages:
            if masked:
                example_number = '00.123.456/7890-01'
                error_message = _(
                    'Enter a valid cnpj number (e.g. {example_number})'
                )
            else:
                example_number = '00123456789001'
                error_message = _('Enter a valid cnpj number (e.g. {example_number}).')

            self.error_messages['invalid'] = format_lazy(
                error_message, example_number=example_number
            )

    def to_python(self, value):
        cnpj = cnpj_to_python(value)

        if cnpj in validators.EMPTY_VALUES:
            return self.empty_value

        if cnpj and not cnpj.is_valid():
            raise ValidationError(self.error_messages['invalid'])

        return cnpj
