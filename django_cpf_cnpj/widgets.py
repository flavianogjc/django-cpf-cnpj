from django.forms import TextInput


class CPFWidget(TextInput):
    def __init__(self, attrs=None):
        if not isinstance(attrs, dict):
            attrs = dict()

        if attrs is not None and hasattr(attrs, 'setdefault'):
            attrs.setdefault('max_length', 14)
            attrs.setdefault('size', 14)
            attrs.setdefault('type', 'text')

        super(CPFWidget, self).__init__(attrs)


class CNPJWidget(TextInput):
    def __init__(self, attrs=None):
        if not isinstance(attrs, dict):
            attrs = {}

        if attrs is not None and hasattr(attrs, 'setdefault'):
            attrs.setdefault('max_length', 18)
            attrs.setdefault('size', 18)
            attrs.setdefault('type', 'text')

        super(CNPJWidget, self).__init__(attrs)
