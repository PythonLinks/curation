# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError

class EmailExistsError (ValidationError):
    """ That email address already exists in the database"""
    title = "Email Exists"
class UserExistsError (ValidationError):
    """ That user name is already in use. """
    title = "User Exists"
class Validator(object):

    def __init__(self, fields, form):
        self.form = form

    def validate(self, data):
        errors = []
        people = getPrincipalFolder(self.form.context)        
        
        # MAKE SURE THE EMAIL DOES NOT EXIST
        email = data['email']
        if email in people.idByEmail:
           error = EmailExistsError("That email address is already registered "                   + email)           
           errors.append(error)

        #MAKE SURE THE HANDLE DOES NOT EXIST   
        handle = data['handle']
        if people.existsHandle (handle):
           error = UserExistsError ("That user already exists: " + handle)
           errors.append(error)
        return errors

