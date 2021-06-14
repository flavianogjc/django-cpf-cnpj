from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from django.utils.version import get_version as django_version

from django_cpf_cnpj.cpf import CPF, cpf_to_python as cpf_to_python
from django_cpf_cnpj.cnpj import CNPJ, cnpj_to_python as cnpj_to_python
from django_cpf_cnpj.validators import is_valid_cpf, is_valid_cnpj
from .models import DefaultCPF, OptionalCPF, NullableCPF, UniqueCPF, TestCPFModel, CustomCPFModel, DefaultCNPJ, OptionalCNPJ, NullableCNPJ, UniqueCNPJ, TestCNPJModel, CustomCNPJModel
from .forms import TestCPFForm, CustomCPFForm, TestCNPJForm, CustomCNPJForm


def cpf_transform(obj):
    return obj.pk, obj.cpf


def cnpj_transform(obj):
    return obj.pk, obj.cnpj


class CPFFieldTestCase(TestCase):
    invalid_string_cpf = 'invalid'
    valid_string_cpf = '00000000191'
    list_invalid_string = ['12312312312', '123.123.123-12', '123456789012345', invalid_string_cpf]
    list_valid_string = ['000.000.001-91', valid_string_cpf]
    equal_valid_cpfs = ['01234567890', '012.345.678-90']

    def test_random_cpf(self):
        self.assertTrue(is_valid_cpf(CPF.random_generator()))

    def test_str_for_valid_string(self):
        self.assertEqual(
            str(cpf_to_python(self.valid_string_cpf)),
            self.valid_string_cpf,
        )

    def test_str_for_invalid_string(self):
        self.assertEqual(
            str(cpf_to_python(self.invalid_string_cpf)),
            self.invalid_string_cpf,
        )

    def test_repr_for_valid_string(self):
        self.assertEqual(
            repr(cpf_to_python(self.valid_string_cpf)),
            f'CPF(raw_input={self.valid_string_cpf})',
        )

    def test_repr_for_invalid_string(self):
        self.assertEqual(
            repr(cpf_to_python(self.invalid_string_cpf)),
            f'InvalidCPF(raw_input={self.invalid_string_cpf})',
        )

    def test_list_valid_string_are_valid(self):
        cpfs = [
            CPF.from_string(cpf_string)
            for cpf_string in self.list_valid_string
        ]
        self.assertTrue(all(cpf.is_valid() for cpf in cpfs))

    def test_list_invalid_string_are_invalid(self):
        cpfs = [
            CPF.from_string(cpf_string)
            for cpf_string in self.list_invalid_string
        ]
        self.assertTrue(all(not cpf.is_valid() for cpf in cpfs))

    def test_same_cpf_valid_has_same_hash(self):
        cps = [
            CPF.from_string(cpf)
            for cpf in self.equal_valid_cpfs
        ]

        cpfs_set = set(cps)
        self.assertEqual(len(cpfs_set), 1)
        for cpf in cps:
            self.assertIn(cpf, cpfs_set)

        self.assertNotIn(self.valid_string_cpf, cpfs_set)

    def test_eq_and_ne(self):
        cpf_string_1 = '99999999808'
        cpf_string_2 = '55555555474'
        cpf_1 = CPF.from_string('99999999808')
        cpf_2 = CPF.from_string('55555555474')

        self.assertNotEqual(cpf_1, cpf_2)
        self.assertNotEqual(cpf_1, cpf_string_2)
        self.assertNotEqual(cpf_string_2, cpf_1)
        self.assertEqual(cpf_1, cpf_string_1)
        self.assertEqual(cpf_string_1, cpf_1)
        self.assertEqual(cpf_1, cpf_1)

    def test_raise_on_invalid_values(self):
        msg = "Can't convert int to CPF."
        with self.assertRaisesMessage(TypeError, msg):
            cpf_to_python(42)


class CPFFieldAppTest(TestCase):
    invalid_string_cpf = 'invalid'
    valid_string_cpf = '00000000191'
    list_invalid_string = ['12312312312', '123.123.123-12', '123456789012345', invalid_string_cpf]
    equal_valid_cpfs = ['01234567890', '012.345.678-90']

    def test_create_with_int(self):
        msg = "Can't convert int to CPF."
        with self.assertRaisesMessage(TypeError, msg):
            DefaultCPF.objects.create(
                cpf=int(self.valid_string_cpf)
            )

    def test_filter_by_invalid_type_int_raises_value_error(self):
        msg = "Can't convert int to CPF."
        with self.assertRaisesMessage(TypeError, msg):
            DefaultCPF.objects.filter(cpf=123).exists()

    def test_create_with_invalid_string_cpf(self):
        obj = TestCPFModel.objects.create(cpf=self.invalid_string_cpf)
        if django_version() > '3.0':
            self.assertEqual(obj.cpf.raw_input, self.invalid_string_cpf)

        obj = TestCPFModel.objects.get(id=obj.id)
        if django_version() > '3.0':
            self.assertEqual(obj.cpf.raw_input, self.invalid_string_cpf)

    def test_save_field_to_database(self):
        """Basic Field Test"""
        random_cpf = CPF.random_generator()

        tm = TestCPFModel()
        tm.cpf = random_cpf
        tm.full_clean()
        tm.save()
        pk = tm.pk

        tm = TestCPFModel.objects.get(pk=pk)

        if django_version() > '3.0':
            self.assertIsInstance(tm.cpf, CPF)
        else:
            self.assertIsInstance(tm.cpf, str)
        self.assertQuerysetEqual(
            TestCPFModel.objects.all(),
            [(tm.pk, random_cpf)],
            transform=cpf_transform,
        )

    def test_save_field_with_invalid_cpf(self):
        for invalid_cpf in self.list_invalid_string:
            with self.assertRaises(ValidationError):
                tm = TestCPFModel()
                tm.cpf = invalid_cpf
                tm.full_clean()
                tm.save()
                pk = tm.pk

                tm = TestCPFModel.objects.get(pk=pk)
                if django_version() > '3.0':
                    self.assertIsInstance(tm.cpf, CPF)
                else:
                    self.assertIsInstance(tm.cpf, str)
                self.assertQuerysetEqual(
                    TestCPFModel.objects.all(),
                    [(tm.pk, invalid_cpf)],
                    transform=cpf_transform,
                )

    def test_filter_by_partial_digits_of_valid_cpf(self):
        DefaultCPF.objects.create(cpf='15496107911')
        DefaultCPF.objects.create(cpf='99768383445')
        self.assertEqual(
            DefaultCPF.objects.filter(
                cpf__contains='154961079'
            ).count(),
            1,
        )
        self.assertEqual(
            DefaultCPF.objects.filter(
                cpf__contains='997683834'
            ).count(),
            1,
        )

    def test_defer_cpf_field(self):
        u = DefaultCPF.objects.create(cpf=self.valid_string_cpf)
        v = DefaultCPF.objects.defer('cpf').get(pk=u.pk)
        self.assertEqual(v.cpf, self.valid_string_cpf)

    def test_filtering_by_invalid_cpf_does_not_raise_value_error(self):
        DefaultCPF.objects.filter(cpf='0' * 11)

    def test_blank_field_returns_empty_string(self):
        model = OptionalCPF()
        self.assertEqual(model.cpf, '')

        model.cpf = self.valid_string_cpf
        if django_version() > '3.0':
            self.assertIsInstance(model.cpf, CPF)
        else:
            self.assertIsInstance(model.cpf, str)

    def test_null_field_returns_none(self):
        model = NullableCPF()
        self.assertIsNone(model.cpf)

        model.cpf = self.valid_string_cpf
        if django_version() > '3.0':
            self.assertIsInstance(model.cpf, CPF)
        else:
            self.assertIsInstance(model.cpf, str)

    def test_can_assign_stringcpf(self):
        model = OptionalCPF()
        model.cpf = self.valid_string_cpf
        if django_version() > '3.0':
            self.assertIsInstance(model.cpf, CPF)
        else:
            self.assertIsInstance(model.cpf, str)
        model.full_clean()
        model.save()

    def test_objects_with_same_cpf_are_equal(self):
        cpfs = [
            DefaultCPF.objects.create(
                cpf=cpf
            ).cpf
            for cpf in self.equal_valid_cpfs
        ]

        for cpf in cpfs:
            if django_version() > '3.0':
                self.assertEqual(cpf, cpfs[0])
            for vcpf in self.equal_valid_cpfs:
                if django_version() > '3.0':
                    self.assertEqual(cpf, vcpf)

    def test_nullable_field(self):
        cpf1 = UniqueCPF()
        cpf1.save()

        cpf2 = UniqueCPF()
        cpf2.save()

        pk1 = cpf1.pk
        pk2 = cpf2.pk
        tmp1 = UniqueCPF.objects.get(pk=pk1)
        tmp2 = UniqueCPF.objects.get(pk=pk2)
        self.assertIsNone(tmp1.cpf)
        self.assertIsNone(tmp2.cpf)
        self.assertQuerysetEqual(
            list(UniqueCPF.objects.all()), [(tmp1.pk, None), (tmp2.pk, None)], transform=cpf_transform
        )

        # Ensure that null values do not cause uniqueness conflicts
        TestCPFModel.objects.create()
        self.assertEqual(UniqueCPF.objects.count(), 2)


class CPFFormFieldTest(TestCase):
    invalid_string_cpf = 'invalid'
    list_invalid_string = ['12312312312', '123.123.123-12', invalid_string_cpf]

    def test_invalid(self):
        for invalid_cpf in self.list_invalid_string:
            form = TestCPFForm({'cpf': invalid_cpf})
            self.assertIs(form.is_valid(), False)

            self.assertEqual(
                form.errors,
                {
                    'cpf': [
                        f'({invalid_cpf}) is not valid cpf.'
                    ]
                },
            )

    def test_invalid_size(self):
        form = TestCPFForm({'cpf': '123456789012345'})
        self.assertIs(form.is_valid(), False)

        self.assertEqual(
            form.errors,
            {
                'cpf': [
                    f'Ensure this value has at most 14 characters (it has 15).'
                ]
            },
        )

    def test_override_form_field(self):
        cpf = CustomCPFModel()
        model_field = cpf._meta.get_field('cpf')
        self.assertIsInstance(model_field.formfield(), CustomCPFForm)


class CNPJFieldTestCase(TestCase):
    invalid_string_cnpj = 'invalid'
    valid_string_cnpj = '00000000000191'
    list_invalid_string = ['12345678901234', '12.345.678/9012-34', '1234567890123456789', invalid_string_cnpj]
    list_valid_string = ['00.000.000/0001-91', valid_string_cnpj]
    equal_valid_cnpjs = ['89765309115838', '89.765.309/1158-38']

    def test_random_cnpj(self):
        self.assertTrue(is_valid_cnpj(CNPJ.random_generator()))

    def test_str_for_valid_string(self):
        self.assertEqual(
            str(cnpj_to_python(self.valid_string_cnpj)),
            self.valid_string_cnpj,
        )

    def test_str_for_invalid_string(self):
        self.assertEqual(
            str(cnpj_to_python(self.invalid_string_cnpj)),
            self.invalid_string_cnpj,
        )

    def test_repr_for_valid_string(self):
        self.assertEqual(
            repr(cnpj_to_python(self.valid_string_cnpj)),
            f'CNPJ(raw_input={self.valid_string_cnpj})',
        )

    def test_repr_for_invalid_string(self):
        self.assertEqual(
            repr(cnpj_to_python(self.invalid_string_cnpj)),
            f'InvalidCNPJ(raw_input={self.invalid_string_cnpj})',
        )

    def test_list_valid_string_are_valid(self):
        cnpjs = [
            CNPJ.from_string(cnpj_string)
            for cnpj_string in self.list_valid_string
        ]
        self.assertTrue(all(cnpj.is_valid() for cnpj in cnpjs))

    def test_list_invalid_string_are_invalid(self):
        cnpjs = [
            CNPJ.from_string(cnpj_string)
            for cnpj_string in self.list_invalid_string
        ]
        self.assertTrue(all(not cnpj.is_valid() for cnpj in cnpjs))

    def test_same_cnpj_valid_has_same_hash(self):
        cps = [
            CNPJ.from_string(cnpj)
            for cnpj in self.equal_valid_cnpjs
        ]

        cnpjs_set = set(cps)
        self.assertEqual(len(cnpjs_set), 1)
        for cnpj in cps:
            self.assertIn(cnpj, cnpjs_set)

        self.assertNotIn(self.valid_string_cnpj, cnpjs_set)

    def test_eq_and_ne(self):
        cnpj_string_1 = '99999999808'
        cnpj_string_2 = '55555555474'
        cnpj_1 = CNPJ.from_string('99999999808')
        cnpj_2 = CNPJ.from_string('55555555474')

        self.assertNotEqual(cnpj_1, cnpj_2)
        self.assertNotEqual(cnpj_1, cnpj_string_2)
        self.assertNotEqual(cnpj_string_2, cnpj_1)
        self.assertEqual(cnpj_1, cnpj_string_1)
        self.assertEqual(cnpj_string_1, cnpj_1)
        self.assertEqual(cnpj_1, cnpj_1)

    def test_raise_on_invalid_values(self):
        msg = "Can't convert int to CNPJ."
        with self.assertRaisesMessage(TypeError, msg):
            cnpj_to_python(42)


class CNPJFieldAppTest(TestCase):
    invalid_string_cnpj = 'invalid'
    valid_string_cnpj = '00000000000191'
    list_invalid_string = ['12345678901234', '12.345.678/9012-34', '1234567890123456789', invalid_string_cnpj]
    list_valid_string = ['00.000.000/0001-91', valid_string_cnpj]
    equal_valid_cnpjs = ['89765309115838', '89.765.309/1158-38']

    def test_create_with_int(self):
        msg = "Can't convert int to CNPJ."
        with self.assertRaisesMessage(TypeError, msg):
            DefaultCNPJ.objects.create(
                cnpj=int(self.valid_string_cnpj)
            )

    def test_filter_by_invalid_type_int_raises_value_error(self):
        msg = "Can't convert int to CNPJ."
        with self.assertRaisesMessage(TypeError, msg):
            DefaultCNPJ.objects.filter(cnpj=123).exists()

    def test_create_with_invalid_string_cnpj(self):
        obj = TestCNPJModel.objects.create(cnpj=self.invalid_string_cnpj)
        if django_version() > '3.0':
            self.assertEqual(obj.cnpj.raw_input, self.invalid_string_cnpj)

        obj = TestCNPJModel.objects.get(id=obj.id)
        if django_version() > '3.0':
            self.assertEqual(obj.cnpj.raw_input, self.invalid_string_cnpj)

    def test_save_field_to_database(self):
        """Basic Field Test"""
        random_cnpj = CNPJ.random_generator()

        tm = TestCNPJModel()
        tm.cnpj = random_cnpj
        tm.full_clean()
        tm.save()
        pk = tm.pk

        tm = TestCNPJModel.objects.get(pk=pk)
        if django_version() > '3.0':
            self.assertIsInstance(tm.cnpj, CNPJ)
        else:
            self.assertIsInstance(tm.cnpj, str)
        self.assertQuerysetEqual(
            TestCNPJModel.objects.all(),
            [(tm.pk, random_cnpj)],
            transform=cnpj_transform,
        )

    def test_save_field_with_invalid_cnpj(self):
        for invalid_cnpj in self.list_invalid_string:
            with self.assertRaises(ValidationError):
                tm = TestCNPJModel()
                tm.cnpj = invalid_cnpj
                tm.full_clean()
                tm.save()
                pk = tm.pk

                tm = TestCNPJModel.objects.get(pk=pk)
                if django_version() > '3.0':
                    self.assertIsInstance(tm.cnpj, CNPJ)
                else:
                    self.assertIsInstance(tm.cpf, str)
                self.assertQuerysetEqual(
                    TestCNPJModel.objects.all(),
                    [(tm.pk, invalid_cnpj)],
                    transform=cnpj_transform,
                )

    def test_filter_by_partial_digits_of_valid_cnpj(self):
        DefaultCNPJ.objects.create(cnpj='15496107911')
        DefaultCNPJ.objects.create(cnpj='99768383445')
        self.assertEqual(
            DefaultCNPJ.objects.filter(
                cnpj__contains='154961079'
            ).count(),
            1,
        )
        self.assertEqual(
            DefaultCNPJ.objects.filter(
                cnpj__contains='997683834'
            ).count(),
            1,
        )

    def test_defer_cnpj_field(self):
        u = DefaultCNPJ.objects.create(cnpj=self.valid_string_cnpj)
        v = DefaultCNPJ.objects.defer('cnpj').get(pk=u.pk)
        self.assertEqual(v.cnpj, self.valid_string_cnpj)

    def test_filtering_by_invalid_cnpj_does_not_raise_value_error(self):
        DefaultCNPJ.objects.filter(cnpj='0' * 11)

    def test_blank_field_returns_empty_string(self):
        model = OptionalCNPJ()
        self.assertEqual(model.cnpj, '')

        model.cnpj = self.valid_string_cnpj
        if django_version() > '3.0':
            self.assertIsInstance(model.cnpj, CNPJ)
        else:
            self.assertIsInstance(model.cnpj, str)

    def test_null_field_returns_none(self):
        model = NullableCNPJ()
        self.assertIsNone(model.cnpj)

        model.cnpj = self.valid_string_cnpj
        if django_version() > '3.0':
            self.assertIsInstance(model.cnpj, CNPJ)
        else:
            self.assertIsInstance(model.cnpj, str)

    def test_can_assign_stringCNPJ(self):
        model = OptionalCNPJ()
        model.cnpj = self.valid_string_cnpj
        if django_version() > '3.0':
            self.assertIsInstance(model.cnpj, CNPJ)
        else:
            self.assertIsInstance(model.cnpj, str)
        model.full_clean()
        model.save()

    def test_objects_with_same_cnpj_are_equal(self):
        cnpjs = [
            DefaultCNPJ.objects.create(
                cnpj=cnpj
            ).cnpj
            for cnpj in self.equal_valid_cnpjs
        ]

        for cnpj in cnpjs:
            if django_version() > '3.0':
                self.assertEqual(cnpj, cnpjs[0])
            for vcnpj in self.equal_valid_cnpjs:
                if django_version() > '3.0':
                    self.assertEqual(cnpj, vcnpj)

    def test_nullable_field(self):
        cnpj1 = UniqueCNPJ()
        cnpj1.save()

        cnpj2 = UniqueCNPJ()
        cnpj2.save()

        pk1 = cnpj1.pk
        pk2 = cnpj2.pk
        tmp1 = UniqueCNPJ.objects.get(pk=pk1)
        tmp2 = UniqueCNPJ.objects.get(pk=pk2)
        self.assertIsNone(tmp1.cnpj)
        self.assertIsNone(tmp2.cnpj)
        self.assertQuerysetEqual(
            list(UniqueCNPJ.objects.all()), [(tmp1.pk, None), (tmp2.pk, None)], transform=cnpj_transform
        )

        # Ensure that null values do not cause uniqueness conflicts
        TestCNPJModel.objects.create()
        self.assertEqual(UniqueCNPJ.objects.count(), 2)


class CNPJFormFieldTest(TestCase):
    invalid_string_cnpj = 'invalid'
    list_invalid_string = ['12345678901234', '12.345.678/9012-34', invalid_string_cnpj]

    def test_invalid(self):
        for invalid_cnpj in self.list_invalid_string:
            form = TestCNPJForm({'cnpj': invalid_cnpj})
            self.assertIs(form.is_valid(), False)

            self.assertEqual(
                form.errors,
                {
                    'cnpj': [
                        f'({invalid_cnpj}) is not valid cnpj.'
                    ]
                },
            )

    def test_invalid_size(self):
        form = TestCNPJForm({'cnpj': '1234567890123456789'})
        self.assertIs(form.is_valid(), False)

        self.assertEqual(
            form.errors,
            {
                'cnpj': [
                    f'Ensure this value has at most 18 characters (it has 19).'
                ]
            },
        )

    def test_override_form_field(self):
        cnpj = CustomCNPJModel()
        model_field = cnpj._meta.get_field('cnpj')
        self.assertIsInstance(model_field.formfield(), CustomCNPJForm)
