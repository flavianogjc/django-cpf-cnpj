from django import forms

from django_cpf_cnpj.forms import CPFForm, CNPJForm
from .models import TestToCPFForm, TestToCNPJForm


class TestCPFForm(forms.ModelForm):
    class Meta:
        model = TestToCPFForm
        fields = ['cpf']


class CustomCPFForm(CPFForm):
    pass


class TestCNPJForm(forms.ModelForm):
    class Meta:
        model = TestToCNPJForm
        fields = ['cnpj']


class CustomCNPJForm(CNPJForm):
    pass
