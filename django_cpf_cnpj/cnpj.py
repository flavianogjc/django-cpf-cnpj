from django.conf import settings
from django.core import validators

from django_cpf_cnpj.validators import is_valid_cnpj, cnpj_random_generator
import re


class CNPJ(object):
    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.number = re.sub(r'\D', '', str(raw_input)).zfill(11)

    def __str__(self):
        if self.is_valid():
            format_string = getattr(settings, 'CNPJ_MASKED', False)
            return cnpj_to_python(self.number) if format_string else self.number
        else:
            return self.raw_input

    def __len__(self):
        return len(str(self))

    def __repr__(self):
        if not self.is_valid():
            return str(
                'Invalid{}(raw_input={})'.format(type(self).__name__, self.raw_input)
            )
        else:
            return str(
                '{}(raw_input={})'.format(type(self).__name__, self.raw_input)
            )

    def __eq__(self, other):
        if other in validators.EMPTY_VALUES:
            return False
        elif isinstance(other, str):
            other = cnpj_to_python(other)
        elif isinstance(other, type(self)):
            pass
        else:
            return False

        self_str = self.number if self.is_valid() else self.raw_input
        other_str = other.number if other.is_valid() else other.raw_input

        return self_str == other_str

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(
                "'<' not supported between instances of "
                "'%s' and '%s'" % (type(self).__name__, type(other).__name__)
            )

        invalid = None
        if not self.is_valid():
            invalid = self
        elif not other.is_valid():
            invalid = other

        if invalid is not None:
            raise ValueError('Invalid cnpj: %r' % invalid)

        return self.number < other.number

    def __hash__(self):
        return hash(str(self))

    @classmethod
    def from_string(cls, cpf_number):
        cpf_number_obj = cls(cpf_number)
        return cpf_number_obj

    def format(self):
        var = self.number
        return var[:3] + '.' + var[3:6] + '.' + var[7:10] + '-' + var[-2:]

    def is_valid(self):
        return is_valid_cnpj(self.number)

    @classmethod
    def random_generator(cls):
        return cnpj_random_generator()


def cnpj_to_python(value):
    if value in [None, '']:
        cpf_number = value
    elif isinstance(value, str):
        cpf_number = CNPJ.from_string(cpf_number=value)
    elif isinstance(value, CNPJ):
        cpf_number = value
    else:
        raise TypeError("Can't convert %s to CNPJ." % type(value).__name__)

    return cpf_number


if __name__ == '__main__':
    cnpf_invalid = CNPJ('invalid')

    assert not cnpf_invalid.is_valid()
    print(cnpf_invalid)
    print(cnpf_invalid.raw_input)
    print(len(cnpf_invalid))
