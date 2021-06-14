import setuptools


with open('README.rst', 'r') as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name='django-cpf-cnpj',
    version='1.0.0',
    long_description=long_description,
    long_description_content_type = 'text/x-rst',
    description='A django model and form field for normalised cpf and cnpj.',
    url='https://github.com/flavianogjc/django-cpf-cnpj',
    author='flavianogjc',
    author_email='flavianogjc@hotmail.com',
    platforms='OS Independent',
    license='MIT',
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    install_requires=['Django >= 2.2',],
    packages=['django_cpf_cnpj',]
)
