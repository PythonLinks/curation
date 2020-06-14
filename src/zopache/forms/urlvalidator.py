from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError

class DuplicateURLError(ValidationError):
      pass

class DuplicateURLValidator(object):

    def __init__(self, fields, form):
        self.form = form

    def validate(self, data):
        self.data = data
        errors = Errors()
        remoteURL = data['remoteURL']        
        if self.form.remoteURLExists(remoteURL):
           error =DuplicateURLError("That url is already in the database "
                                    + remoteURL)           
           errors.append(error)

        return errors        
