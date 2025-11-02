import json
import mistune
from zope.interface import implementer

from dolmen.forms.base.errors import Error, Errors

from zopache.core import Leaf
from zopache.pages.page import PageVeryBase
from zopache.json.interfaces import IMarkdown
from zopache.core.ancestors import Ancestors
from zopache.json.jsonproperties import BasicProperties

#This should have been IJSONMarkdown. Oh well. 
@implementer(IMarkdown)
class JSONMarkdown(BasicProperties, PageVeryBase,Ancestors):
    webClass = "JSONMarkdown"
    schemaName = "JSONMarkdownSchema"    

    def getTitle(self):
        json = self.json
        if 'title' in json:
            return json['title']
        return json['data']['title']
    
    def setTitle(self,title):
        json = self.json
        json['data']['title'] = title
        self._p_changed = True
    title = property(getTitle,setTitle)
    
    @property
    def source(self):
        json = self.json
        return json['data']['content']
    
    @property
    def description(self):
        json = self.json
        return json['data']['description']

    def postProcess(self, view = None):        
        self._html = mistune.markdown(self.source)
        PageVeryBase.postProcess(self, view = view)
        
    def postAddProcess(self, view = None):                
        self.postProcess(view = view)
        
    def html(self):
        return self._html

    def partialPostProcess(self, view=None):
        pass
    
    def getDescriptionForDomain(self,view):
        return self.getDescriptionFor(view)            

    def getFieldFor(self,view,field):    
       json = self.json
       if (text:= data.get(field,None)) != None:
                   return text        
       return None

    def getTitleFor(self,view):
        return self.title       
      
    def getTitleForDomain(self,view):
        return self.title

    def getDescriptionFor(self,view):
        return self.description
    
    def getHtmlFor(self,view):
        return self.source


from zopache.zmi.interfaces import IURLSegment
import crom
@crom.adapter
@crom.sources(IMarkdown)
@crom.target(IURLSegment)
class IMarkdownAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'manage'        
