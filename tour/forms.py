from django import forms
from django.utils.translation import gettext as _


class Participate(forms.Form):
    e_mail = forms.EmailField(label=_('Email'))

    def __str__(self):
        return self.e_mail
