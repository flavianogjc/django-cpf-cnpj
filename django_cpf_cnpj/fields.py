from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_cpf_cnpj.validators import validate_cpf, validate_cnpj
from django_cpf_cnpj.cpf import cpf_to_python, CPF
from django_cpf_cnpj.cnpj import cnpj_to_python, CNPJ

__all__ = ['CPFField', 'CNPJField']


class CPFDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.field.name in instance.__dict__:
            value = instance.__dict__[self.field.name]
        else:
            instance.refresh_from_db(fields=[self.field.name])
            value = getattr(instance, self.field.name)
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = cpf_to_python(value)


class CPFField(models.CharField):
    default_validators = [validate_cpf]
    description = _('CPF number')
    descriptor_class = CPFDescriptor

    def __init__(self, masked=False, *args, **kwargs):
        kwargs.setdefault('max_length', 14)
        super().__init__(*args, **kwargs)
        self._masked = getattr(settings, 'CPF_MASKED', None) or masked
        self.empty_values = [None, '']

    @property
    def is_masked(self):
        return self._masked or getattr(settings, 'CPF_MASKED', False)

    def get_prep_value(self, value):
        """
        Perform preliminary non-db specific value checks and conversions.
        """
        if not value:
            return super().get_prep_value(value)

        if isinstance(value, CPF):
            parsed_value = value
        else:
            # Convert the string to a CPF object.
            parsed_value = cpf_to_python(value)

        if parsed_value.is_valid():
            # A valid cpf. Normalize it for storage.
            value = parsed_value.__str__()
        else:
            # Not a valid cpf. Store the raw string.
            value = parsed_value.raw_input

        return super().get_prep_value(value)


class CNPJDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.field.name in instance.__dict__:
            value = instance.__dict__[self.field.name]
        else:
            instance.refresh_from_db(fields=[self.field.name])
            value = getattr(instance, self.field.name)
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = cnpj_to_python(value)


class CNPJField(models.CharField):
    default_validators = [validate_cnpj]
    description = _('CNPJ number')
    descriptor_class = CNPJDescriptor

    def __init__(self, masked=False, *args, **kwargs):
        kwargs.setdefault('max_length', 18)
        super().__init__(*args, **kwargs)
        self._masked = getattr(settings, 'CNPJ_MASKED', None) or masked
        self.empty_values = [None, '']

    @property
    def is_masked(self):
        return self._masked or getattr(settings, 'CNPJ_MASKED', False)

    def get_prep_value(self, value):
        """
        Perform preliminary non-db specific value checks and conversions.
        """
        if not value:
            return super().get_prep_value(value)

        if isinstance(value, CNPJ):
            parsed_value = value
        else:
            # Convert the string to a CPF object.
            parsed_value = cnpj_to_python(value)

        if parsed_value.is_valid():
            # A valid cpf. Normalize it for storage.
            value = parsed_value.__str__()
        else:
            # Not a valid cpf. Store the raw string.
            value = parsed_value.raw_input

        return super().get_prep_value(value)
