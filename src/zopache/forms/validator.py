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

class NoPasswordError(ValidationError):
    """ You need to login with Google Login """
    title = "Please do a Google Login"
    
class Validator(object):

    def __init__(self, fields, form):
        self.form = form

    def getEmail(self):
        email = self.data['email']
        return email
    
    def validate(self, data):
        self.data = data
        errors = []
        people = getPrincipalFolder(self.form.context)        

        # MAKE SURE THE EMAIL DOES NOT EXIST
        email = self.getEmail()
        if email in people.idByEmail:
           error = EmailExistsError("That email address is already registered "                   + email)           
           errors.append(error)

        #MAKE SURE THE HANDLE DOES NOT EXIST   
        handle = data['handle']
        if people.existsHandle (handle):
           error = UserExistsError ("That user already exists: " + handle)
           errors.append(error)
        return errors

class LoginValidator(Validator):
    def validate(self, data):
        self.data = data
        errors = []
        people = getPrincipalFolder(self.form.context)        
        anId = self.getEmail()
        principal = people.getPrincipalByUserName(anId, default = None)
        if ((principal != None )and
            (principal._password == "")):
           error = NoPasswordError("""Please Login using Google, 
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
        except:
               raise ValueError('Trouble')            
        legit =['accounts.google.com', 'https://accounts.google.com']
        if  not (idinfo['iss'] in legit):
               raise ValueError('Wrong issuer.')
        return idinfo
        
    def getClientId(self,form):
        domain = form.getDomain()
        if (domain == 'pythonlinks.info'):
            clientId= '901181416018-8c8n8knds3b6koqkottchj7ivpncf409.apps.googleusercontent.com'
        elif (domain == 'dev.pythonlinks.info'):
            clientId = '901181416018-npba3s080378saoc1umjkn5jo7lipa1q.apps.googleusercontent.com'
        elif (domain == 'forestwiki.com'):
            clientId = '901181416018-8sh20u10e5tltf00jc4o8qfpq1jhmvh0.apps.googleusercontent.com'
        elif (domain == 'rights.men'):
            clientId = '901181416018-il4qps4qiqafom0uhmrppvcf9ao7ve07.apps.googleusercontent.com'
        elif (domain == 'golangvideos.com'):
            clientId = '901181416018-f6c7p85thdp79l9c6c3joccj9ffb5jug.apps.googleusercontent.com'
        elif (domain == 'stopsmog.info'):
            clientId = '901181416018-gmg5itiqs6f4cp5j5eot1corta0gd558.apps.googleusercontent.com'
        elif (domain == 'mensgroups.info'):
            clientId = '950419722294-r5peocg874brshvn5kk2bdi71iuhrlc5.apps.googleusercontent.com'
        elif (domain == 'climateactivists.info'):
            clientId = '832774817535-0e4d586gd3us7oq6pak88u0djtl8punn.apps.googleusercontent.com'            
        else:
            raise ValueError('Bad Domain')
        return clientId

    def getTokenData(self,token):

        try : 
            clientId = self.getClientId(self.form)
            if isinstance (token,list):
                token = token [0]
            tokenData = self.validateToken(token,self.form,clientId)
            self.tokenData = tokenData            
        except ValueError:
            # Invalid token
            return "Invalide Token"

    
class GoogleValidator (AccessGoogle,Validator):
    
    def getEmail(self):

        token = self.form.request.form['form.field.idtoken']        
        self.getTokenData (token)
        email = self.tokenData['email']
        return email
