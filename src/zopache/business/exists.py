# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError
from slugify import slugify, SLUG_OK


class OrganizationExistsError (ValidationError):
    """ Organization Exists. """
    title = "Organization Exists"
    
class DuplicateOrganization(object):

    def __init__(self, fields, form):
        self.form = form
    
    def validate(self, data):
        errors = []
        siteRoot = self.form.context.getSiteRoot()
        title = data ['title']
        slug = slugify(title,lower=True)
        errorMessage =    F""" Thank you for your suggesting "{title}", 
but that organization 
is already in the database at /{slug}. If it is not a duplicate, and you still 
want to submit it, then 
please change the name or spelling, resubmit, and the submission should work.
You can also add the name of the city to distinguish it from the other 
organization. """
        if slug in siteRoot:
           error = OrganizationExistsError(errorMessage)
           errors.append(error)
        return errors

