# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError
from slugify import slugify, SLUG_OK
from zopache.forms.urlvalidator import BaseValidator,ArgsError

class Duplicate(BaseValidator):
    def validate(self, data):
        siteRoot = self.form.getSiteRoot()
        errors = Errors()

        theItem = self.slugExists(data)
        if theItem != None:
            title = theItem.title
            errorMessage =    "Error: An object with that name "
            errorMessage += title
            errorMessage += " is already in the database at  "
            form = self.form
            url = form.secureShortURL(theItem)
            url = form.shortenURL (url)
            errorMessage += "<" + url +   ">"
            error = ArgsError(errorMessage)
            errors.append(error)
        return errors

