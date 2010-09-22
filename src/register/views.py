# -*- coding: utf-8 -*-
"""
Register.views
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
    form = BookForm()
    if request.method == "POST"  :
        if form.validate(request.form):
            book = form.save()
            book.put()
            return redirect(url_for('register/index'))
        else :
            return render_to_response('register/search_amazon.html', {'form': form.as_widget(),
                                                                        'errors': form.errors })
            
    query = Book.all().order('-created')
    books = query.fetch(ITEMS_PER_PAGE)
    return render_to_response('register/index.html', {'errors': form.errors, 
                                                      'books': books,
                                                      'form': form.as_widget()})


def search_amazon(request, isbn):
    from aws import AWS
    import xml.etree.ElementTree as ET
    import urllib2
    import logging
    from datetime import datetime, date
    
    XMLNS = "{http://webservices.amazon.com/AWSECommerceService/2010-06-01}"
    
    import myconfig
    aws = AWS()

    request_url = aws.doItemLookUp(isbn)
    logging.info(request_url)
    result = urllib2.urlopen(request_url)
    
    tree = ET.parse(result)
    root = tree.getroot()
    
    
    asin=""
    detail_page_shop_url=""
    title=""
    author=""
    publisher=""
    publication_date=""
    price=""
    image_url=""
    err_msg=""
    for node in root.getchildren():
        if node.tag == XMLNS + "Items":
            for subnode in node.getchildren():
                if subnode.tag == XMLNS + "Request":
                    for subnode2 in subnode.getchildren():
                        if subnode2.tag ==  XMLNS + "Errors":
                            for errnode in subnode2.getchildren():
                                if errnode.tag == XMLNS + "Error":
                                    for msg in errnode.getchildren():
                                        if msg.tag == XMLNS + "Message":
                                            err_msg = msg.text
                if subnode.tag == XMLNS + "Item":
                    for item in subnode.getchildren():
                        if item.tag == XMLNS + "ASIN":
                            asin = item.text
                        if item.tag == XMLNS + "DetailPageURL":
                            detail_page_shop_url = item.text
                        if item.tag == XMLNS + "MediumImage":
                            for imageurl in item.getchildren():
                                if imageurl.tag == XMLNS + "URL":
                                    image_url = imageurl.text
                        if item.tag == XMLNS + "ItemAttributes":
                            for item_attr in item.getchildren():                                
                                if item_attr.tag == XMLNS + "Title":
                                    title = item_attr.text
                                if item_attr.tag == XMLNS + "Author":
                                    author = item_attr.text
                                if item_attr.tag == XMLNS + "ListPrice":
                                    for listprice in item_attr.getchildren():
                                        if listprice.tag == XMLNS + "Amount":
                                            price = listprice.text
                                if item_attr.tag == XMLNS + "Publisher":
                                    publisher = item_attr.text
                                if item_attr.tag == XMLNS + "PublicationDate":                                    
                                    publication_date = item_attr.text

    try:
        price = int(price)
    except ValueError:
        price = 0
    try:
        st = datetime.strptime(publication_date,'%Y-%m-%d')
        pub_date = date(st.year, st.month, st.day)
    except ValueError:
        try:
            st = datetime.strptime(publication_date,'%Y-%m')
            pub_date = date(st.year, st.month, st.day)
        except ValueError:
            pub_date = None
             
    book = Book(asin=asin, isbn=isbn,detail_page_shop_url=detail_page_shop_url,title=title,author=author,
                publisher=publisher,publication_date=pub_date,price=price,image_url=image_url, 
                tags=[], deletion_reserve=False, lending=False, version=1)
    form = BookForm(instance=book)
    
    return render_to_response('register/search_result.html', {'form': form.as_widget()})



def search_rakuten(request, isbn):
    import xml.etree.ElementTree as ET
    import urllib2
    import logging
    from datetime import datetime, date
    
    XMLNS = '{http://api.rakuten.co.jp/rws/rest/BooksBookSearch/2010-03-18}'
    
    import myconfig

    request_url = 'http://api.rakuten.co.jp/rws/3.0/rest?'
    request_url += 'developerId=' + myconfig.RAKUTEN_DEV_ID + '&affiliateId=' + myconfig.RAKUTEN_AFFILIATE_ID 
    request_url += '&operation=BooksBookSearch&version=2010-03-18&isbn=' + isbn
    request_url += '&outOfStockFlag=1' #品切れ商品も対象とする
    logging.info(request_url)
    result = urllib2.urlopen(request_url)
    
    tree = ET.parse(result)
    root = tree.getroot()
    
    hit = False
    #isbn=""
    asin=""
    detail_page_shop_url=""
    title=""
    author=""
    publisher=""
    publication_date=""
    price=""
    image_url=""
    err_msg=""
    for node in root.getchildren():
        if node.tag == "Body":
            for bodynode in node.getchildren():
                if bodynode.tag == XMLNS + "BooksBookSearch":
                    for resnode in bodynode.getchildren():
                        if resnode.tag == "Items":
                            for subnode in resnode.getchildren():
                                if subnode.tag == "Item":
                                    for item in subnode.getchildren():
#                                        if item.tag == "isbn":
#                                            isbn = item.text
                                        if item.tag == "affiliateUrl":
                                            detail_page_shop_url = item.text
                                        if item.tag == "title":
                                            hit = True
                                            title = item.text
                                        if item.tag == "author":
                                            author = item.text
                                        if item.tag == "publisherName":
                                            publisher = item.text
                                        if item.tag == "salesDate":
                                            publication_date = item.text
                                        if item.tag == "itemPrice":
                                            price = item.text
                                        if item.tag == "largeImageUrl":
                                            image_url = item.text

    if not hit:
        url = url_for('register/index') + "search_rakuten_magazine/" + isbn
        return redirect(url)

    try:
        price = int(price)
    except ValueError:
        price = 0
    try:
        st = datetime.strptime(publication_date,'%Y-%m-%d')
        pub_date = date(st.year, st.month, st.day)
    except ValueError:
        try:
            st = datetime.strptime(publication_date,'%Y-%m')
            pub_date = date(st.year, st.month, st.day)
        except ValueError:
            pub_date = None
             
    book = Book(asin=asin, isbn=isbn,detail_page_shop_url=detail_page_shop_url,title=title,author=author,
                publisher=publisher,publication_date=pub_date,price=price,image_url=image_url, 
                tags=[], deletion_reserve=False, lending=False, version=1)
    form = BookForm(instance=book)
    
    return render_to_response('register/search_result.html', {'form': form.as_widget()})


def search_rakuten_magazine(request, isbn):
    import xml.etree.ElementTree as ET
    import urllib2
    import logging
    from datetime import datetime, date
    
    XMLNS = '{http://api.rakuten.co.jp/rws/rest/BooksMagazineSearch/2010-03-18}'
    
    import myconfig

    request_url = 'http://api.rakuten.co.jp/rws/3.0/rest?'
    request_url += 'developerId=' + myconfig.RAKUTEN_DEV_ID + '&affiliateId=' + myconfig.RAKUTEN_AFFILIATE_ID 
    request_url += '&operation=BooksMagazineSearch&version=2010-03-18&jan=' + isbn
    request_url += '&outOfStockFlag=1' #品切れ商品も対象とする
    logging.info(request_url)
    result = urllib2.urlopen(request_url)
    
    tree = ET.parse(result)
    root = tree.getroot()
    
    hit = False
    #isbn=""
    asin=""
    detail_page_shop_url=""
    title=""
    author=""
    publisher=""
    publication_date=""
    price=""
    image_url=""
    err_msg=""
    for node in root.getchildren():
        if node.tag == "Body":
            for bodynode in node.getchildren():
                if bodynode.tag == XMLNS + "BooksMagazineSearch":
                    for resnode in bodynode.getchildren():
                        if resnode.tag == "Items":
                            for subnode in resnode.getchildren():
                                if subnode.tag == "Item":
                                    for item in subnode.getchildren():
#                                        if item.tag == "isbn":
#                                           isbn = item.text
                                        if item.tag == "affiliateUrl":
                                            detail_page_shop_url = item.text
                                        if item.tag == "title":
                                            hit = True
                                            title = item.text
                                        if item.tag == "author":
                                            author = item.text
                                        if item.tag == "publisherName":
                                            publisher = item.text
                                        if item.tag == "salesDate":
                                            publication_date = item.text
                                        if item.tag == "itemPrice":
                                            price = item.text
                                        if item.tag == "largeImageUrl":
                                            image_url = item.text

    if not hit:
        return render_to_response('register/notfound.html', {'isbn': isbn})

    try:
        price = int(price)
    except ValueError:
        price = 0
    try:
        st = datetime.strptime(publication_date,'%Y-%m-%d')
        pub_date = date(st.year, st.month, st.day)
    except ValueError:
        try:
            st = datetime.strptime(publication_date,'%Y-%m')
            pub_date = date(st.year, st.month, st.day)
        except ValueError:
            pub_date = None
             
    book = Book(asin=asin, isbn=isbn,detail_page_shop_url=detail_page_shop_url,title=title,author=author,
                publisher=publisher,publication_date=pub_date,price=price,image_url=image_url, 
                tags=[], deletion_reserve=False, lending=False, version=1)
    form = BookForm(instance=book)
    
    return render_to_response('register/search_result.html', {'form': form.as_widget()})





def tag_relation(request, book_key):
    form = BookForm()
    book = Book.get(book_key)
    if request.method == "POST"  :
        book.tags = []
        tag_keys = request.form.getlist('tag_keys')
        for tag_key in tag_keys :
            book.tags.append(tag_key)
        book.save()
        book.put()
    
    tags = Tag.all()
    return render_to_response('register/tag_relation.html', {'errors': form.errors, 
                                                      'book': book,
                                                      'tags': tags})
    
