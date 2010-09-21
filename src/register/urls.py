# -*- coding: utf-8 -*-
# Register.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('register/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'register/index': 'register.views.index',
}
"""
from kay.generics import admin_required
from kay.generics import crud
from kay.routing import (
  ViewGroup, Rule
)

class BookCRUDViewGroup(crud.CRUDViewGroup):
  model = 'register.models.Book'
  form = 'register.forms.BookForm'

class TagCRUDViewGroup(crud.CRUDViewGroup):
  model = 'register.models.Tag'
  form = 'register.forms.TagForm'


view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='register.views.index'),
    Rule('/search_amazon/<isbn>', endpoint='search_amazon', view='register.views.search_amazon'),
    Rule('/search_rakuten/<isbn>', endpoint='search_rakuten', view='register.views.search_rakuten'),
    Rule('/search_rakuten_magazine/<isbn>', endpoint='search_rakuten_magazine', view='register.views.search_rakuten_magazine'),
    Rule('/tag_relation/<book_key>', endpoint='tag_relation', view='register.views.tag_relation'),
  ),
  BookCRUDViewGroup(),
  TagCRUDViewGroup(),
]

