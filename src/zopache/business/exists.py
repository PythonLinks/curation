# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError
from slugify import slugify, SLUG_OK
from zopache.forms.urlvalidator import BaseValidator

class Duplicate(BaseValidator):
    def validate(self, data):
        errors = Errors()
        if self.slugExists(data):
            theItem = siteRoot[slug]
            errorMessage =    f""" 
Error: An object with that name "{title}" is already 
in the database at  {form.secureShortURL(theItem)}
"""
            error = OrganizationExistsError(errorMessage)
            errors.append(error)
        return errors

