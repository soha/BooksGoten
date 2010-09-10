# -*- coding: utf-8 -*-

from kay.utils import forms
from kay.utils.forms.modelform import ModelForm

from register.models import (
  Book,Tag
)

class BookForm(ModelForm):
    class Meta:
        model = Book
        exclude = ('user', 'created')


class TagForm(ModelForm):
    class Meta:
        model = Tag
        exclude = ('created')


