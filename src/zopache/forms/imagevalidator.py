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
        
    def logoExists(self):
        form = self.form
        context = form.context
        return 'Logo' in context

    def bannerExists(self):
        form = self.form
        context = form.context
        return 'Banner' in context
   
   
class LogoValidator(BaseValidator):             
    def validate(self, data):        
        errors = Errors()
        if self.logoExists():
           msg = "There is already a Logo in this folder.  "
           msg += "Please delete it before adding a new one. "
           msg += "Use the Manage -> Manage menu to delete it. "
           error =Error(title=msg, identifier = "logo.validator")
           error.args = [msg]
           errors.append(error)
        return errors        

class BannerValidator(BaseValidator):             
    def validate(self, data):        
        errors = Errors()
        if self.bannerExists():
           msg = "There is already a Banner in this folder.  "
           msg += "Please delete it before adding a new one. "
           msg += "Use the Manage -> Manage menu to delete it. "
           error =Error(title=msg, identifier = "Banner.validator")
           error.args = [msg]
           errors.append(error)
        return errors        


   
