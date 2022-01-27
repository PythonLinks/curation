# -*- coding: utf-8 -*-
from dolmen.forms.base.errors import Error,Errors
from zopache.core.getroot import getPrincipalFolder
from zope.schema import ValidationError

class Validator(object):

    def __init__(self, fields, form):
        self.form = form

    def getEmail(self):
        email = self.data['email']
        return email
    
    def validate(self, data):
        self.data = data
        errors = Errors()
        people = getPrincipalFolder(self.form.context,self.form)        

        # MAKE SURE THE EMAIL DOES NOT EXIST
        email = self.getEmail()
        if email in people.idByEmail:
           msg = title="That email address is already registered " + email
           identifier = "Email.Exists.Error" 
           error = Error(msg,identifier)
           error.args = [msg]           
           errors.append(error)

        #MAKE SURE THE HANDLE DOES NOT EXIST   
        handle = data['handle']
        if people.existsHandle (handle):
           error = Error (title= "That user already exists: " + handle,
                          identifier = "User.Exists.Error")
           errors.append(error)
        return errors

class LoginValidator(Validator):
    def validate(self, data):
        self.data = data
        errors = Errors()
        people = getPrincipalFolder(self.form.context,self.form)        
        anId = self.getEmail()
        principal = people.getPrincipalByUserName(anId, default = None)
        #WARNING
        #if principal.email =="calozinski@gmail.com":
        #    return errors
        
        if ((principal != None )and
            (principal._password == "")):
           error = Error(title = """Please Login using Google, 
                                    not local login.""")           
           errors.append(error)
        return errors




