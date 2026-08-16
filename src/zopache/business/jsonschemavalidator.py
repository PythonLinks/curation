from slugify import slugify
from bs4 import BeautifulSoup
from jsonschema import validate
import json
from chameleon import PageTemplate

from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zopache.application.validate import ArgsError

from zopache.pages.interfaces import IPage



class JSONSchemaValidator(object):

    def __init__(self, fields, form):
        self.form = form
        
    def validJSON(self, data):
        form = self.form
        try:
             source=data['jsonData']
             form.requestJsonString = source
             result = json.loads(source)
             form.requestJsonDict = result
             return True, result 
        except Exception as e: 
             return False, e

    def validSchema(self, data):
        form = self.form
        try:
            requestJsonDict = form.requestJsonDict           
            validate(instance=requestJsonDict, schema=form.jsonSchemaDict)     

            return True, "" 
        except Exception as e: 
             return False, e

    #FIRST VSLIDATE THE JSON    
    def validate(self, data):
        errors = Errors()
        success, result  = self.validJSON(data)
        if not success:
              msg = "That is not valid json. "
              msg += result.args[0]  #NUL RESULT
              error = ArgsError(title=msg, identifier="json.validator")
              errors.append(error)
              return errors
        success, result  = self.validSchema(data)         
        if not success:
              msg = "Your Data is invalid according to the Schema."
              msg += result.message
              error = ArgsError(title = msg, identifier = "json-schema.validator")
              errors.append(error)
              
        return errors        


   
