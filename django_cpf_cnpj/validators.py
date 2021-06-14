from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re


def last_digits_cpf(value):
    v1, v2 = 0, 0
    for i, d in enumerate(map(int, value[:-2][::-1])):
        v1 += d * (9 - (i % 10))
        v2 += d * (9 - (i + 1) % 10)

    v1 = (v1 % 11) % 10
    v2 = ((v2 + v1 * 9) % 11) % 10

    return v1, v2


def last_digits_cnpj(value):
    cnpj = tuple(map(int, value))

    v1 = 5 * cnpj[0] + 4 * cnpj[1] + 3 * cnpj[2] + 2 * cnpj[3]
    v1 += 9 * cnpj[4] + 8 * cnpj[5] + 7 * cnpj[6] + 6 * cnpj[7]
    v1 += 5 * cnpj[8] + 4 * cnpj[9] + 3 * cnpj[10] + 2 * cnpj[11]
    v1 = v1 % 11
    v1 = 0 if v1 < 2 else 11 - v1

    v2 = 6 * cnpj[0] + 5 * cnpj[1] + 4 * cnpj[2] + 3 * cnpj[3]
    v2 += 2 * cnpj[4] + 9 * cnpj[5] + 8 * cnpj[6] + 7 * cnpj[7]
    v2 += 6 * cnpj[8] + 5 * cnpj[9] + 4 * cnpj[10] + 3 * cnpj[11]
    v2 += 2 * v1

    v2 = v2 % 11
    v2 = 0 if v2 < 2 else 11 - v2

    return v1, v2


def is_valid_cpf(value):
    if not isinstance(value, str) and not isinstance(value, int):
        return False

    value = re.sub(r'\D', '', str(value)).zfill(11)
    if len(re.sub(r'([0-9])\1+', r'\1', value)) == 1 or len(value) != 11:
        return False

    v1, v2 = last_digits_cpf(value)

    if v1 != int(value[-2]) or v2 != int(value[-1]):
        return False

    return True


def is_valid_cnpj(value):
    if not isinstance(value, str) and not isinstance(value, int):
        return False

    value = re.sub(r'\D', '', str(value)).zfill(14)
    if len(re.sub(r'([0-9])\1+', r'\1', value)) == 1 or len(value) != 14:
        return False

    v1, v2 = last_digits_cnpj(value)

    if v1 != int(value[-2]) or v2 != int(value[-1]):
        return False

    return True


def cpf_generator(value):
    value = re.sub(r'\D', '', str(value)).zfill(9)[:9]

    v1, v2 = last_digits_cpf(value + 'xx')

    new = value + str(v1) + str(v2)

    if not is_valid_cpf(new):
        new = None

    return new


def cnpj_generator(value):
    value = re.sub(r'\D', '', str(value)).zfill(12)[:12]
    v1, v2 = last_digits_cnpj(value)

    new = value + str(v1) + str(v2)

    if not is_valid_cnpj(new):
        new = None

    return new


def cpf_random_generator():
    import random

    candidate = str(random.randint(1, 999999998))
    while not cpf_generator(candidate):
        candidate = str(random.randint(1, 999999998))

    return cpf_generator(candidate)


def cnpj_random_generator():
    import random

    candidate = str(random.randint(1, 999999999998))
    while not cnpj_generator(candidate):
        candidate = str(random.randint(1, 999999999998))

    return cnpj_generator(candidate)


def validate_cpf(value):
    if not is_valid_cpf(value):
        raise ValidationError(
            _(f'({value}) is not valid cpf.')
        )


def validate_cnpj(value):
    if not is_valid_cnpj(value):
        raise ValidationError(
            _(f'({value}) is not valid cnpj.')
        )


if __name__ == '__main__':
    # Cpf asserts
    assert not is_valid_cpf('00000000000')
    assert cpf_generator('000.001') == '00000000191'
    assert cpf_generator('999.999.998') == '99999999808'
    assert is_valid_cpf(cpf_random_generator())

    # Cnpj asserts
    assert not is_valid_cnpj('0' * 12)
    assert cnpj_generator('000.001') == '00000000000191'
    assert is_valid_cpf(cpf_random_generator())
    print(cnpj_random_generator())
