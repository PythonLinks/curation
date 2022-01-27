from zopache.forms.validator import LoginValidator

    
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
