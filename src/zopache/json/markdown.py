import json
from zope.interface import implementer

from dolmen.forms.base.errors import Error, Errors

from zopache.core import Leaf
from zopache.pages.page import PageVeryBase
from zopache.json.interfaces import IMarkdown
from zopache.core.ancestors import Ancestors
from zopache.json.jsonproperties import JSONProperties

@implementer(IMarkdown)
class JSONMarkdown(JSONProperties, Base,PageVeryBase,Ancestors):
    webClass = "Multilingual"    
    @property
    def title(self):
        json = self.json
          return json['title']

    @property
    def source(self):
        json = self.json
        json['en']['content']
    
    @property
    def description(self):
        json = self.json
        return json['description']

    def postAddProcess(self, view = None):
        pass

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
@crom.sources(IMultilingualLeaf)
@crom.target(IURLSegment)
class IMarkdownAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'ckedit'        
