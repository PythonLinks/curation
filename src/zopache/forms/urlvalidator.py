from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError
from slugify import slugify

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
        siteRoot = self.form.context.getSiteRoot()
        title = data ['title']
        slug = slugify(title,lower=True)
        return siteRoot.get(slug,None)

    def urlExists(self, data):
        self.data = data
        if not 'remoteURL' in data:
             return None
        
        remoteURL = data['remoteURL']
        if remoteURL == "":
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
   
class DuplicateURLValidator(object):             
    def validate(self, data):        
        errors = Errors()
        if self.urlExists(data) != None:
           msg = "That url is already in the database "
           msg +=  form.secureShortURL(urlObject)
           error =ArgsError(title=msg, identifirer="url.validator")
           error.title = msg
           errors.append(error)
        return errors        


   
