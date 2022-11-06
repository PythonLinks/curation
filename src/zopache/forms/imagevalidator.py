from zope.schema import ValidationError
from slugify import slugify

from dolmen.forms.base.errors import Error,Errors
from zopache.application.validate import ArgsError
from zopache.core.getroot import getPrincipalFolder
from zopache.application.validate import ArgsError

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


class ImageValidator(BaseValidator):
    def validate(self, data):        
        errors = Errors()
        if data['data'] == b'' and data['imageURL'] == '':
            msg = "Please link to an image, or upload an image." 
            error =ArgsError(title=msg, identifier = "image.validator")
            errors.append(error)
        return errors        
        
class LogoValidator(BaseValidator):             
    def validate(self, data):        
        errors = Errors()
        if self.logoExists():
           msg = "There is already a Logo in this folder.  "
           msg += "Please delete it before adding a new one. "
           msg += "Use the Manage -> Manage menu to delete it. "
           error =ArgsError(title=msg, identifier = "logo.validator")
           errors.append(error)
        return errors        

class BannerValidator(BaseValidator):             
    def validate(self, data):        
        errors = Errors()
        if self.bannerExists():
           msg = "There is already a Banner in this folder.  "
           msg += "Please delete it before adding a new one. "
           msg += "Use the Manage -> Manage menu to delete it. "
           error =ArgsError(title=msg, identifier = "Banner.validator")
           errors.append(error)
        return errors        


class SocialMediaImageValidator(BaseValidator):             
    def socialMediaImageExists(self):
        form = self.form
        context = form.context
        return 'SocialMediaImage' in context
   
    def validate(self, data):        
        errors = Errors()
        if self.socialMediaImageExists():
           msg = "There is already a Social Media in this folder.  "
           msg += "Please delete it before adding a new one. "
           msg += "Use the Manage -> Manage menu to delete it. "
           error =ArgsError(title=msg, identifier = "Banner.validator")
           errors.append(error)
        return errors        


   
