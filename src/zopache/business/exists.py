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
            errorMessage += """ This software is organized as a taxonomy, a tree, but every page
also gets a unique short canonical url.  So this error message
prevents duplicates.  If you still want to add this page, just give it
a slightly different title.  After it has been created, you can edit
the page title back to whatever you want.  The page titles can be duplicates, 
it is the URL's which have to be unique. """
            error = ArgsError(errorMessage)
            errors.append(error)
        return errors

class DuplicatePerson(Duplicate):
    def slugExists(self, data):
        principalFolder = self.form.getPrincipalFolder()
        title = data ['title']
        return principalFolder.getIdByHandle(self, title) != None            



    
