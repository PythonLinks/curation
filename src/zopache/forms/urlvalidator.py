from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError

class DuplicateURLError(ValidationError):
     """ Two urls exist"""
     title="That URL already is in the database"

class DuplicateURLValidator(object):

    def __init__(self, fields, form):
        self.form = form

    def validate(self, data):
        self.data = data
        #errors = Errors()
        errors = []
        if not 'remoteURL' in data:
             return errors
        remoteURL = data['remoteURL']        
        if self.form.getSiteRoot().existsRemoteURL(remoteURL)!= None:
           error =DuplicateURLError("That url is already in the database "
                                    + remoteURL)           
           errors.append(error)

        return errors        
