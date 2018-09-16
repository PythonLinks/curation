#This software is subject to the CV License Agreement.
from BTrees.OOBTree import OOBTree
from zope.cachedescriptors.property import CachedProperty
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from zope.interface import implementer

from dolmen.forms.base import action, name, context, form_component
from crom import target, order
from cromlech.browser.directives import title
from cromlech.security import permissions
from dolmen.view import name, context, view_component
from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response



from zopache.ttw.interfaces import IWeb
from zopache.categories.interfaces import IVote

from cromdemo.interfaces import ITab


def make_text_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'text/plain'
        return response    


def tallyVotes(principal,context):    
        upVotes =context.upVotes()
        downVotes =context.downVotes()
        principalUpVotes = len (principal._upVotes)
        principalDownVotes = len (principal._downVotes)        
        return (str(upVotes) + ' , ' +
                 str(downVotes) + ' , ' +
                 str(principalUpVotes) + ' , ' +
                str(principalDownVotes))


@view_component
@name('upVote')
@context(IVote)
@title("Vote Up")
@permissions('Vote')
class UpVote(View):
    responseFactory = Response
    make_response = make_text_response
    def render(self):
        context = self.context
        principal = self.request.principal
        principal.upVote(context)
        context.upVote(principal)
        return tallyVotes(principal,context)
        
@view_component
@name('downVote')
@context(IVote)
@permissions('Vote')
@title("Vote Down")
class DownVote(View):
    responseFactory = Response
    make_response = make_text_response
        
    def render(self):
        context = self.context
        principal = self.request.principal        
        principal.downVote(context)
        context.downVote(principal)
        return tallyVotes(principal,context)
           
