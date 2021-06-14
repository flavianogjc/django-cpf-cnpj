DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

SECRET_KEY = 'SECRET_KEY'

INSTALLED_APPS = [
    'django_cpf_cnpj',
    'tests'
]
