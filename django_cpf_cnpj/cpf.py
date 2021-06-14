from django.conf import settings
from django.core import validators

from django_cpf_cnpj.validators import is_valid_cpf, cpf_random_generator
import re


class CPF(object):
    fiscal_region_map = {
        '1': {
            'name': '1.ª Região Fiscal',
            'thirst': 'Brasília',
            'shorted': 'RF1',
            'jurisdiction': ['DF', 'GO', 'MT', 'MS',  'TO']
        },
        '2': {
            'name': '2.ª Região Fiscal',
            'thirst': 'Belém',
            'shorted': 'RF2',
            'jurisdiction': ['AC', 'AP', 'AM', 'PA', 'RO',  'RR']
        },
        '3': {
            'name': '3.ª Região Fiscal',
            'thirst': 'Fortaleza',
            'shorted': 'RF3',
            'jurisdiction': ['CE', 'MA',  'PI']
        },
        '4': {
            'name': '4.ª Região Fiscal',
            'thirst': 'Recife',
            'shorted': 'RF4',
            'jurisdiction': ['AL', 'PB', 'PE', 'RN']
        },
        '5': {
            'name': '5.ª Região Fiscal',
            'thirst': 'Salvador',
            'shorted': 'RF5',
            'jurisdiction': ['BA', 'SE']
        },
        '6': {
            'name': '6.ª Região Fiscal',
            'thirst': 'Belo Horizonte',
            'shorted': 'RF6',
            'jurisdiction': ['MG']
        },
        '7': {
            'name': '7.ª Região Fiscal',
            'thirst': 'Rio de Janeiro',
            'shorted': 'RF7',
            'jurisdiction': ['ES', 'RJ']
        },
        '8': {
            'name': '8.ª Região Fiscal',
            'thirst': 'São Paulo',
            'shorted': 'RF8',
            'jurisdiction': ['SP']
        },
        '9': {
            'name': '9.ª Região Fiscal',
            'thirst': 'Curitiba',
            'shorted': 'RF9',
            'jurisdiction': ['PR', 'SC']
        },
        '0': {
            'name': '10.ª Região Fiscal',
            'thirst': 'Porto Alegre',
            'shorted': 'RF10',
            'jurisdiction': ['RS']
        },
    }

    def __init__(self, raw_input):
        self.raw_input = raw_input
        self.number = re.sub(r'\D', '', str(raw_input)).zfill(11)

    def __str__(self):
        if self.is_valid():
            format_string = getattr(settings, 'CPF_MASKED', False)
            return cpf_to_python(self.number) if format_string else self.number
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
            other = cpf_to_python(other)
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
            raise ValueError('Invalid cpf: %r' % invalid)

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
        return is_valid_cpf(self.number)

    def get_fiscal_region(self):
        if self.is_valid():
            return self.fiscal_region_map[self.number[8]]
        else:
            return None

    @classmethod
    def random_generator(cls):
        return cpf_random_generator()


def cpf_to_python(value):
    if value in [None, '']:
        cpf_number = value
    elif isinstance(value, str):
        cpf_number = CPF.from_string(cpf_number=value)
    elif isinstance(value, CPF):
        cpf_number = value
    else:
        raise TypeError("Can't convert %s to CPF." % type(value).__name__)

    return cpf_number


if __name__ == '__main__':
    cpf_invalid = CPF('invalid')

    assert not cpf_invalid.is_valid()
    print(cpf_invalid)
    print(cpf_invalid.raw_input)
    print(len(cpf_invalid))

    cpf_valid = CPF('00000000868')
    assert cpf_valid.is_valid()
    print(cpf_valid.get_fiscal_region())
