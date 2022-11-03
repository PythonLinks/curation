from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError
from slugify import slugify
from json import loads
import json

#NEEDED FOR SOME STRANGENESS IN DOLMEN.FORMS.BASE.VALIDATE
class ArgsError(Error):
     @property
     def args(self):
          return [self.title]

class BaseValidator(object):

    def __init__(self, fields, form):
        self.form = form
        
    def slugExists(self, data):
        form = self.form
        siteRoot = self.form.getSiteRoot()
        if "title" in data:
           title = data ['title']
        else:
           try:
              json = loads(data["json"])
              baseTab = self.jsonSchemaDict["baseTab"]
              title = json[baseTab]["title"]
           except:
                return None
             
        slug = slugify(title,lower=True)
        return siteRoot.get(slug,None)

    def getURL(self,data):
       if 'remoteURL' in data:
             return data['remoteURL']
       if 'rssURL' in data:
             return data['rssURL']        
       if 'articleURL' in data:
             return data['articleURL']        
       try:
            data  = json.loads(data['json'])
            return data['connect']['remoteURL']
       except:
            pass
       return None

    def urlExists(self, data):
        self.data = data
        remoteURL = self.getURL(data)
        if not remoteURL:
           return None  
        form = self.form
        siteRoot = form.getSiteRoot()
        urlObject = siteRoot.existsRemoteURL(remoteURL)
        return urlObject
   
    def categoryExists(self, data):
        form = self.form
        siteRoot = self.form.context.getSiteRoot()
        categoryName = data ['categoryName']
        return siteRoot.get(categoryName,None)
   
class DuplicateURLValidator(BaseValidator):             
    def validate(self, data):
        errors = Errors()
        
        theItem = self.urlExists(data) 
        if theItem != None:
           form = self.form
           msg = "That url is already in the database "
           url=  form.secureShortURL(theItem)
           url = form.shortenURL(url)
           msg +=  url
           error =Error(title=msg, identifier="url.validator")
           error.args = [msg]
                
           errors.append(error)
        return errors        


   
