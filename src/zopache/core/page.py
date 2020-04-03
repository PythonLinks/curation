# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from os import path
from cromlech.webob.response import Response
from dolmen.view import View, make_layout_response
from dolmen.forms.base import Form as BaseForm
from cromlech.location import get_absolute_url
from cromlech.browser.interfaces import IURL, IPublicationRoot
from zopache.core.scripts import Scripts
from dolmen.container import IBTreeContainer
from .breadcrumbs import Breadcrumbs

class Page(View,Scripts,Breadcrumbs):
    count=0
    error=''
    title=""
    subTitle=""
    responseFactory = Response
    make_response = make_layout_response


            
