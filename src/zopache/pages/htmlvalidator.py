from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError
from slugify import slugify
from bs4 import BeautifulSoup
from zopache.pages.interfaces import IPage
from chameleon import PageTemplate

#NEEDED FOR SOME STRANGENESS IN DOLMEN.FORMS.BASE.VALIDATE
class ArgsError(Error):
     @property
     def args(self):
          return [self.title]

class HTMLValidator(object):

    def __init__(self, fields, form):
        self.form = form
        
    def hasJavascript(self, data):
        form = self.form
        soup = BeautifulSoup(data['source'])
        scripts = soup.find_all('script')
        return len(scripts) > 0


    def validTemplate(self, data):
        form = self.form
        source=data['source']
        try:
             result = PageTemplate(source)
             return True, result 
        except Exception as e: 
             return False, e

    def validate(self, data):
        errors = Errors()
        form = self.form        
        if form.isManager():
           success, result  = self.validTemplate(data)
           if not success:
              msg = result
              error =Error(title=msg, identifier="chameleon.validator")
              error.args = [msg]
              errors.append(error)              
        else:
          if self.hasJavascript(data):  
              msg = "It is a security violation to include Javascript "
              msg += "in your html."
              error =Error(title=msg, identifier="javascript.validator")
              error.args = [msg]
              errors.append(error)
        return errors        


   
