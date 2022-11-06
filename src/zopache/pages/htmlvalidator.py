from slugify import slugify
from bs4 import BeautifulSoup
from chameleon import PageTemplate

from dolmen.forms.base.errors import Errors
from zopache.core.getroot import getPrincipalFolder
from zopache.application.validate import ArgsError
from zopache.pages.interfaces import IPage


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
              error =ArgsError(title=msg, identifier="chameleon.validator")
              errors.append(error)              
        else:
          if self.hasJavascript(data):  
              msg = "It is a security violation to include Javascript "
              msg += "in your html."
              error =ArgsError(title=msg, identifier="javascript.validator")
              errors.append(error)
        return errors        


   
