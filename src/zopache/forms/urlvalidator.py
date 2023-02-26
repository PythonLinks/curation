from zope.schema import ValidationError
from slugify import slugify
from json import loads
import json

from dolmen.forms.base.errors import Error,Errors

from zopache.application.validate import ArgsError
from zopache.core.getroot import getPrincipalFolder



class BaseValidator(object):

    def __init__(self, fields, form):
        self.form = form

    def getTitle(self,data):
        if "title" in data:
           return  data ['title'].strip()
        return None
  
    def slugExists(self, data):
        form = self.form
        siteRoot = self.form.getSiteRoot()
        title = self.getTitle(data)
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
            result  = json.loads(data['jsonData'])
            return result['connect']['remoteURL']
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
        if ((theItem != None) and (
                theItem != self.form.context)):
           form = self.form
           msg = "That url is already in the database at: "
           url=  form.secureShortURL(theItem)
           url = form.shortenURL(url)
           msg +=  url
           error =ArgsError(title=msg, identifier="url.validator")
           errors.append(error)
        return errors        

