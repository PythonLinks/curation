# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError
from slugify import slugify, SLUG_OK
from zopache.forms.urlvalidator import BaseValidator,ArgsError
from dolmen.forms.base.errors import Error,Errors

class InvalidCategoryError (ValidationError):
    """ Organization Exists. """
    title = "That category does not exists"


class Junk (object):
    pass

class ValidateDiscord(BaseValidator):
        
    def validate(self, data):
        errors = Errors()
        theItem = None
        errorMessage = ""
        categoryExists = self.categoryExists(data)
        if not categoryExists:
           categoryName = data["categoryName"] 
           errorMessage += f" No such hashtag: #{categoryName}"
           
        title = data ["title"]
        slugExists = self.slugExists(data)
        if slugExists != None:
            theItem = slugExists
            errorMessage += f""" "{title}" already exists . """
            
        urlExists = self.urlExists(data)    
        if urlExists != None:
            theItem = urlExists
            errorMessage += "That url already exists. "
            
        if (categoryExists == None or
            slugExists != None  or
            urlExists != None):
            
            errorMessage +=    f""" You can see the object at <{self.form.secureShortURL(theItem)}>
"""
            error = ArgsError(title = errorMessage,
                          identifier = "slug-or-url")
            errors.append(error)
        return errors

