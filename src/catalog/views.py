# -*- coding: utf-8 -*-
"""
catalog.views
"""

"""
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""


from werkzeug import redirect
from kay.utils import render_to_response
from kay.utils import (
 render_to_response, url_for, forms
)

from kay.auth.decorators import login_required

from register.models import Book, Tag
from register.forms import BookForm


# Create your views here.
ITEMS_PER_PAGE = 100


def index(request):
    tag = request.args.get('tags')
    query = Book.all()
    if tag :
        tag_id = ""
        tag_model = Tag.all().filter("title =", tag).get()
        if tag_model :
            tag_id = str(tag_model.key())
        query.filter("tags =", tag_id)
            
    query.order('-created')
    books = query.fetch(ITEMS_PER_PAGE)
    
    tags = Tag.all()
    return render_to_response('catalog/index.html', {'books': books,
                                                     'tags': tags})
                                                      
def deletion_reserve_list(request):
    query = Book.all().filter("deletion_reserve = ", True).order('-created')
    books = query.fetch(ITEMS_PER_PAGE)
    return render_to_response('catalog/index.html', {'books': books,
                                                     'deletion_reserve_flg': True})

def detail(request, key):
    book = Book.get(key)
    tag_key_list = book.tags #tags is always not None
    tag_title_list = []
    for tag_key in tag_key_list :
        try :
            tag_title = Tag.get(tag_key)
            if tag_title :
                tag_title_list.append(tag_title)
        except :
            pass
    
    return render_to_response('catalog/detail.html', {'book': book,
                                                      'tag_title_list': tag_title_list})

def lend(request, key):
    if request.method == "POST" :
        book = Book.get(key)
        lending_str = request.form['lending']
        if(lending_str == 'True'):
            book.lending = True
        else:
            book.lending = False
        book.put()
    detail_url = '/catalog/detail/' + key
    return redirect(detail_url) 

#Androidからの貸出更新用 XMLを返す
def lendbydroid(request, key):
    books = []
    if request.method == "POST" :
        book = Book.get(key)
        lending_str = request.form['lending']
        if(lending_str.lower() == 'true'):
            book.lending = True
        else:
            book.lending = False
        book.put()
        #book = Book.get(key)
        books.append(book)
    #return render_to_response('catalog/detail.html', {'book': book})
    return render_to_response('catalog/listxml.html', {'books': books})
    

def listxml(request):
    query = Book.all().order('-created')
    books = query.fetch(ITEMS_PER_PAGE)
    return render_to_response('catalog/listxml.html', {'books': books})


    