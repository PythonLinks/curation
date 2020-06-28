# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError
from slugify import slugify, SLUG_OK


class InvalidCategoryError (ValidationError):
    """ Organization Exists. """
    title = "That category does not exists"
    
class MissingCategory(object):

    def __init__(self, fields, form):
        self.form = form
    
    def validate(self, data):
        errors = []
        form = self.form
        siteRoot = self.form.context.getSiteRoot()
        categoryName = data ['categoryName']
        if not categoryName  in siteRoot:
            errorMessage =    f""" 
There is no category called #"{categoryName}" in {form.secureShortURL()}.
"""
            error = InvalidCategoryError(errorMessage)
            errors.append(error)
        return errors

