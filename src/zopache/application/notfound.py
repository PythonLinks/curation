from zope.interface import Interface
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from cromlech.browser import IView
from cromlech.browser.exceptions import HTTPFound
from dolmen.view import View, view_component

from zopache.core.viewdecorators import *

@view_component
@context(Interface)
@name("not-found")
@target(IView)
class NotFound(View):
    responseFactory = Response
    make_response = make_view_response    
    def update(self):
           raise HTTPFound("/categories")

