# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError
from slugify import slugify, SLUG_OK


class OrganizationExistsError (ValidationError):
    """ Organization Exists. """
    title = "That Object Exists"
    
class Duplicate(object):

    def __init__(self, fields, form):
        self.form = form
    
    def validate(self, data):
        errors = []
        form = self.form
        siteRoot = self.form.context.getSiteRoot()
        title = data ['title']
        slug = slugify(title,lower=True)
        if slug in siteRoot:
            theItem = siteRoot[slug]
            errorMessage =    f""" 
Error: An object with that name "{title}" is already 
in the database at  {form.secureShortURL(theItem)}
"""
            error = OrganizationExistsError(errorMessage)
            errors.append(error)
        return errors

