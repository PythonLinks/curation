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

def makeXMLResponse(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or '')
        response.content_type=u'application/rss+xml'
        return response    

class IXML (Interface):
    title = schema.TextLine(
        title = u'Title',
        description = u'Please Describe this XML Document.',
        required = False,
    )

    source= schema.Text(
        title = u'Feed Source',
        description = u'The XML Template goes here.',
        required = False,
        default = '',
    )    

class AceScripts(AceScripts):
    aceMode = 'xml'

@implementer(IXML)
class XML(AceHTML):
    pass
        
@form_component
@name('addXML')
@context(IBTreeContainer)
@permissions('Manage')
class AddXML(AddAceHTML):
    subTitle='Add an XML Object'
    interface = IXML
    ignoreContent = True
    factory=XML

@view_component
@name('index')
@context(IXML)
class Index(HTMLIndex):
    responseFactory = Response
    make_response = makeXMLResponse

@form_component
@context(IFeed)
@name("aceedit")
@permissions('Manage')
class AceEditXML(AceScripts,AceEditForm):
    subTitle='Edit an XML Object'
    interface = IFeed
    
@view_component
@name('source')
@context(IXML)
class Source(View):
    def render(self):
        return self.context.source
           
