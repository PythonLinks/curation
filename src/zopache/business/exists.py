# -*- coding: utf-8 -*-
from json import loads
from slugify import slugify, SLUG_OK

from zope.schema import ValidationError
from dolmen.forms.base.errors import Error,Errors

from zopache.core.getroot import getPrincipalFolder
from zopache.forms.urlvalidator import BaseValidator
from zopache.application.validate import ArgsError

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
            errorMessage += """ 
            If you still want to add this page,
            just give it a slightly different title and a different
            unique url slug will be generated.
            """
            error = ArgsError(title=errorMessage, identifier ="In Duplicat")
            errors.append(error)
        return errors

class DuplicatePerson(Duplicate):
    def slugExists(self, data):
        principalFolder = self.form.getPrincipalFolder()
        title = data ['title'].strip()
        return  principalFolder.getIdByHandle(self, title)

import json    
class DuplicatePolitician(Duplicate):
    def getTitle(self,data):
      try:
            requestJsonDict = self.form.requestJsonDict
            return requestJsonDict ["content"]['english']["title"].strip()
      except:
         return None
             
class DuplicateOrganization(Duplicate):
    def getTitle(self,data):
        try:
            requestJsonDict = self.form.requestJsonDict
            return requestJsonDict ["content"][0]["title"].strip()
        except:
            return None
             



    
