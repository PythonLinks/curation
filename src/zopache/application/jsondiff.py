import json
from zopache.core.breadcrumbs import Breadcrumbs
from dolmen.container import IBTreeContainer
from dolmen.view import View
from dolmen.view import name, context, view_component
from cromlech.webob.response import Response

from zopache.core.viewdecorators import *
from zopache.application.diff import hashTime, hash
from zopache.ttw.interfaces import IAceEdit
from zopache.ttw.interfaces import  IInternalPrincipal

def makeJsonCorsResponse(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or '')
        response.content_type=u'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response    

class Base(object):
    def getData(self,item):
        data = dict()
        data ['name'] = item.__name__
        data ['hash'], data ['modificationTime'] = hashTime (item)
        if IInternalPrincipal.providedBy(self.context):
            data ['title'] = "That is privae information"
        else:         
           data ['title'] = getattr(item,'title','')
        data ['url'] = self.getSecureLongURL(context=item)
        if hasattr(item,'description'):
            data ['description'] = getattr(item,'description','')
        data ['aceEdit'] = IAceEdit.providedBy(item) 
        data ['bTree'] =  IBTreeContainer.providedBy(item) 
        if hasattr(item,'source'):    
            data ['source'] = getattr(item,'source','')
        return data

@view_component            
@name('diff.json')
@target(IView)
@context(Interface)
class DiffJson(View, Breadcrumbs,Base):
    responseFactory = Response
    make_response = makeJsonCorsResponse
    
    def render(self):
        result = {}
        for item in self.context.values():
            data = self.getData(item)
            result[item.__name__]= data
        return json.dumps(result)    

@view_component
@name('ace.json')
@target(IView)
@context(IAceEdit)
class AceJson(View, Breadcrumbs, Base):
    responseFactory = Response
    make_response = makeJsonCorsResponse
           
    def render(self):
        context = self.context    
        data = self.getData(context)
        data ['hashSource'] = hash(context.source)
        data ['hashTitle'] = hash(context.title)
        if hasattr(context,'description'): 
           data ['hashDescription'] = hash(context.description)                
        return json.dumps(data)    

 
