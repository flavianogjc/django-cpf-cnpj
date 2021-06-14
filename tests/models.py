from django.db import models

from django_cpf_cnpj.fields import CPFField, CNPJField


class DefaultCPF(models.Model):
    cpf = CPFField()
    objects = models.Manager()


class OptionalCPF(models.Model):
    cpf = CPFField(blank=True, default='')
    objects = models.Manager()


class NullableCPF(models.Model):
    cpf = CPFField(blank=True, null=True)
    objects = models.Manager()


class UniqueCPF(models.Model):
    cpf = CPFField(null=True, unique=True)
    objects = models.Manager()


class TestCPFModel(models.Model):
    cpf = CPFField(blank=True, null=True)
    objects = models.Manager()


class TestToCPFForm(models.Model):
    cpf = CPFField(blank=True, null=True)
    objects = models.Manager()


class CustomCPFField(CPFField):
    def formfield(self, **kwargs):
        from .forms import CustomCPFForm

        return super().formfield(form_class=CustomCPFForm)


class CustomCPFModel(models.Model):
    cpf = CustomCPFField()


class DefaultCNPJ(models.Model):
    cnpj = CNPJField()
    objects = models.Manager()


class OptionalCNPJ(models.Model):
    cnpj = CNPJField(blank=True, default='')
    objects = models.Manager()


class NullableCNPJ(models.Model):
    cnpj = CNPJField(blank=True, null=True)
    objects = models.Manager()


class UniqueCNPJ(models.Model):
    cnpj = CNPJField(null=True, unique=True)
    objects = models.Manager()


class TestCNPJModel(models.Model):
    cnpj = CNPJField(blank=True, null=True)
    objects = models.Manager()


class TestToCNPJForm(models.Model):
    cnpj = CNPJField(blank=True, null=True)
    objects = models.Manager()


class CustomCNPJField(CNPJField):
    def formfield(self, **kwargs):
        from .forms import CustomCNPJForm

        return super().formfield(form_class=CustomCNPJForm)


class CustomCNPJModel(models.Model):
    cnpj = CustomCNPJField()
