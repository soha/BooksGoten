# -*- coding: utf-8 -*-
# Register.models

from google.appengine.ext import db
from kay.auth.models import User
import kay.db
from kay.i18n import lazy_gettext as _


# Create your models here.
class MyUser(User):
    pass


class Book(db.Model):
    user = kay.db.OwnerProperty()
    asin = db.StringProperty(required=False, verbose_name=_(u'asin'))
    isbn = db.StringProperty(required=True, verbose_name=_(u'isbn'))
    title = db.StringProperty(required=True, verbose_name=_(u'title'))
    author = db.StringProperty(required=False, verbose_name=_(u'author'))
    publisher = db.StringProperty(required=True, verbose_name=_(u'publisher'))
    publication_date = db.DateProperty(verbose_name=_(u'publication_date'))
    price = db.IntegerProperty(required=True, verbose_name=_(u'price'))
    image_url = db.StringProperty(required=True, verbose_name=_(u'image_url'))
    detail_page_shop_url = db.StringProperty(required=False, verbose_name=_(u'detail_page_shop_url'))
    #not from Amazon
    tags = db.StringListProperty(default=[''])
    memo = db.TextProperty(required=False, verbose_name=_(u'memo'))
    deletion_reserve = db.BooleanProperty(required=False, verbose_name=_(u'deletion_reserve'))
    lending = db.BooleanProperty(required=False, verbose_name=_(u'lending'))
    updated = db.DateTimeProperty(auto_now=True, verbose_name=_(u'updated'))
    created = db.DateTimeProperty(auto_now_add=True, verbose_name=_(u'created'))
    version = db.IntegerProperty(required=False, verbose_name=_(u'version'), default=1)
    
    def __unicode__(self):
        return self.title


class Tag(db.Model):
    title = db.StringProperty(required=True, verbose_name=_(u'tag_title'))
    created = db.DateTimeProperty(auto_now_add=True, verbose_name=_(u'created'))
    version = db.IntegerProperty(required=False, verbose_name=_(u'version'), default=1)
    
    def __unicode__(self):
        return self.title

