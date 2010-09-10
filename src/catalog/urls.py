# -*- coding: utf-8 -*-
# catalog.urls
# 

# Following few lines is an example urlmapping with an older interface.
"""
from werkzeug.routing import EndpointPrefix, Rule

def make_rules():
  return [
    EndpointPrefix('catalog/', [
      Rule('/', endpoint='index'),
    ]),
  ]

all_views = {
  'catalog/index': 'catalog.views.index',
}
"""

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='catalog.views.index'),
    Rule('/deletion_reserve_list', endpoint='deletion_reserve_list', view='catalog.views.deletion_reserve_list'),
    Rule('/detail/<key>', endpoint='detail', view='catalog.views.detail'),
    Rule('/lend/<key>', endpoint='lend', view='catalog.views.lend'),
    Rule('/lendbydroid/<key>', endpoint='lendbydroid', view='catalog.views.lendbydroid'),
    Rule('/list.xml', endpoint='listxml', view='catalog.views.listxml'),
  )
]

