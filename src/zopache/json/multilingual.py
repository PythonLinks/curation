import json
from zope.interface import implementer

from dolmen.forms.base.errors import Error, Errors

from zopache.pages.page import PageVeryBase
from zopache.pages.interfaces import IMultilingual


from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson, EditJson
from zopache.core.interfaces import ITreeSecurity
from zopache.core.ancestors import Ancestors

@implementer(IMultilingual)
class Multilingual(PageVeryBase,Ancestors):
    webClass = "Multilingual"    

    def getLanguages(self,view):
        if getattr(view,'languages', False):
           return view.languages 
        try:
          header = view.request.headers["Accept-Language"]
        except:
          header = ['en']
        #header is "en,fr;0.3,de;0.5,en-uk"  
        languages = header.split(',')
        languages = [language.split(';')[0][:2] for language in languages]
        #Default Language
        languages.append ('en')
        view.languages = languages
        return languages
        
    def getFieldFor(self,view,field):    
       languages = self.getLanguages(view)
       json = self.json
       for lang in languages:
           if (data:= json.get(lang,None)) != None:
               if (text:= data.get(field,None)) != None:
                   return text        
       return None

    def getTitleFor(self,view):
        if (text := self.getFieldFor(view,'title'))!=None:               
            return text
        else:
           return "Error: No title, not even an blank title,  is available."
    @property
    def title(self):
        json = self.json
        if 'en' in json:
          return json['en']['title']
        else:
          return "No English title available"  
      
    def getTitleForDomain(self,view):
        return self.getTitleFor(view)

    def getDescriptionFor(self,view):
        if (text := self.getFieldFor(view,'description'))!=None:               
            return text
        else:
           return "Error: No description, not even a blank  description,  is available."

    def getDescriptionForDomain(self,view):
        return self.getDescriptionFor(view)            
            
    def getHtmlFor(self,view):

        if (text := self.getFieldFor(view,'content'))!=None:               
            return text
        else:
           return "Error: No content is available."            
            
    def partialPostProcess(self, view=None):
        pass

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
        newName =  self.requestJsonDict['en']['title']
        return newName
        
    def dataModel(self):   
        contextJsonDict =  self.template['newMultilingualJson'].getAsDict()
        result = json.dumps(contextJsonDict)
        return result
    
