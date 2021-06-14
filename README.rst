========================
django-cpf-cnpf
========================

A Django library for working with `cpf`_ and `cnpj`_ fields.

.. _`cpf`: https://pt.wikipedia.org/wiki/Cadastro_de_pessoas_f%C3%ADsicas
.. _`cnpj`: https://pt.wikipedia.org/wiki/Cadastro_Nacional_da_Pessoa_Jur%C3%ADdica

Installation
============

Install from pypi::

    pip install django-cpf-cnpj


Install from git::

    pip install git+https://github.com/flavianogjc/django-cpf-cnpj.git


Basic usage
===========

Add the ``django_cpf_cnpj`` app between your apps and django apps::

    INSTALLED_APPS = [
        ...
        'django_cpf_cnpj',
        ...
    ]


Then, you can use it like any regular model field::

    from django_cpf_cnpj.fields import CPFField, CNPJField
    from django.db import models

    class MyModel(models.Model):
        cpf = CPFField(masked=True)  # To enable auto-mask xxx.xxx.xxx-xx
        cnpj = CNPJField(masked=False)  # To disable auto-mask xx.xxx.xxx/xxxx-xx

Running tests
=============

Check tests with tox::

    tox

Check a specific combination::

    tox -e py38-django22

