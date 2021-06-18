from zope.interface import implementer, Interface
from zope import schema

from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from dolmen.container import IBTreeContainer 

from zopache.core import Leaf
from zopache.ttw.htmlviews import AddAceHTML
from zopache.ttw.acescripts import AceScripts
from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *
from zopache.ttw.JSON import makeJsonResponse
from zopache.ttw.html import AceHTML
from zopache.ttw.addeditforms import AceEditForm
from  zopache.ttw.htmlviews import Index as HTMLIndex

def makeFeedResponse(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or '')
        response.content_type=u'application/rss+xml'
        return response    

class IFeed (Interface):
    title = schema.TextLine(
        title = u'Title',
        description = u'Please Describe this Feed.',
        required = False,
    )

    source= schema.Text(
        title = u'Feed Source',
        description = u'The RSS Template goes here.',
        required = False,
        default = '',
    )    

class AceScripts(AceScripts):
    aceMode = 'xml'

@implementer(IFeed)
class Feed(AceHTML):
    pass
        
@form_component
@name('addFeed')
@context(IBTreeContainer)
@permissions('Manage')
class AddFeed(AddAceHTML):
    subTitle='Add an RSS Feed'
    interface = IFeed
    ignoreContent = True
    factory=Feed

@view_component
@name('index')
@context(IFeed)
class Index(HTMLIndex):
    responseFactory = Response
    make_response = makeFeedResponse

@form_component
@context(IFeed)
@name("aceedit")
@permissions('Manage')
class AceEditFeed(AceScripts,AceEditForm):
    subTitle='Edit an RSS Feed Object'
    interface = IFeed
    
@view_component
@name('source')
@context(IFeed)
class Source(View):
    def render(self):
        return self.context.source
           
