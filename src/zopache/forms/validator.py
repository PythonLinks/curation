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
        people = getPrincipalFolder(self.form.context)        

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
        people = getPrincipalFolder(self.form.context)        
        anId = self.getEmail()
        principal = people.getPrincipalByUserName(anId, default = None)
        if ((principal != None )and
            (principal._password == "")):
           error = Error(title = """Please Login using Google, 
                                    not local login.""")           
           errors.append(error)
        return errors


    
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.transport.requests import Request

class AccessGoogle(object):
        
    def validateToken(self,token,form,clientId):
        try:
          idinfo = id_token.verify_oauth2_token(token,Request(),clientId)
        except Exception as err:

               raise ValueError('Trouble' + str(err))            
        legit =['accounts.google.com', 'https://accounts.google.com']
        if  not (idinfo['iss'] in legit):
               raise ValueError('Wrong issuer.')
        return idinfo

    def getClientId(self,form):
        
        root = form.getSiteRoot()
        if hasattr(root,'googleClientId'):
            return root.googleClientId
        return ''
    

    def getTokenData(self,token):

        try : 
            clientId = self.getClientId(self.form)
            if isinstance (token,list):
                token = token [0]
            tokenData = self.validateToken(token,self.form,clientId)
            self.tokenData = tokenData            
        except ValueError as err:
            # Invalid token
            return "Invalide Token"

    
class GoogleValidator (AccessGoogle,Validator):
    
    def getEmail(self):
        token = self.form.request.form['form.field.idtoken']        
        self.getTokenData (token)
        email = self.tokenData['email']
        return email
