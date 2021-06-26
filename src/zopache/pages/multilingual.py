import json
from zope.interface import implementer

from dolmen.forms.base.errors import Error, Errors

from zopache.pages.page import PageVeryBase
from zopache.pages.interfaces import IMultilingual


from zopache.core.viewdecorators import *
from zopache.business.editjsonschema import AddJson, EditJson
from zopache.core.interfaces import ITreeSecurity

@implementer(IMultilingual)
class Multilingual(PageVeryBase):
    webClass = "Multilingual"    
    
    def getTitleFor(self,view):
       if len(self.json) > 0: 
          return self.json[0]["title"]
       else:
           return "Error: Please define at least one language."
       
    def getDescriptionFor(self,view):
       if len(self.json) > 0: 
          return self.json[0]["description"]
       else:
           return "Error: Please define at least one language."

    def getHtmlFor(self,view):
       if len(self.json) > 0: 
          return self.json[0]["content"]
       else:
           return "Error: Please define at least one language."              
            
    def partialPostProcess(self, view=None):
        for item in self.json:
            item["description"]=item["description"].replace ('"' , "&ldquo;", 1)
            item["description"]=item["description"].replace ('"' , "&rdquo;", 1)
            item["description"]=item["description"].replace ('"' , "&ldquo;")
            item["description"]=item["description"].replace ('\n' , " ")
            item["description"]=item["description"].replace ('\r' , " ")           
            item["title"]=item["title"].replace ('"' , "&ldquo;", 1)
            item["title"]=item["title"].replace ('"' , "&rdquo;", 1)
            item["title"]=item["title"].replace ('"' , "&ldquo;")
            item["title"]=item["title"].replace ('\n' , " ")
            item["title"]=item["title"].replace ('\r' , " ")                

@form_component
@name ('ckedit')
@context(IMultilingual)
@implementer(ITreeSecurity)
class EditMultilingual (EditJson):
    title = 'Edit this Multilingual Page.'
    subTitle = ''
    schemaName = "MultilingualSchema"  


from zopache.pages.interfaces import IPageBase
@view_component
@name('addMultilingual')
@target(IView)
@context(IPageBase)
class AddMultilingual(AddJson):
    title = "Add a MultiLingual Page"
    subTitle = "You can add as many language versions as you need."
    factory = Multilingual
    schemaName = "MultilingualSchema"

    def newName(self,data):
        newName =  self.requestJsonDict[0]['title']
        return newName
        
    def dataModel(self):   
        contextJsonDict =  self.template['newMultilingualJson'].getAsDict()
        result = json.dumps(contextJsonDict)
        return result
    
