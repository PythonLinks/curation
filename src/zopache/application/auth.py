# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from functools import wraps
from cromlech.security import Principal
from cromlech.security import unauthenticated_principal as anonymous
from cromlech.browser import getSession
from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import implementer
from zope.location import Location


#THE IDEA HERE IS THAT THE END USER
#CAN SPECIFY THE ROOT
#NO NEED TO DO IN NGINX
virtualHosts = {'dev.pythonlinks.info':'python',
                'pythonlinks.info':'python',
                'desktop.pythonlinks.info':'python',
                'rights.men':'mens-rights',
                'desktop.rights.men':'mens-rights',
                'climatevideos.info':'climate-change', 
                'desktop.climatevideos.info':'climate-change',               
                'cloud-native.pg':'golang',
                'desktop.cloud-native.pg':'golang',                
                'forestwiki.com':'forestwiki',
                'desktop.forestwiki.com':'forestwiki'                
            
}

def secured(app):

    @wraps(app)
    def secure_application(environ, start_response, default=anonymous):
        session = getSession()
        principal = default
        if session is not None and 'user' in session:
            environ['REMOTE_USER'] = userName = session['user']
            conn = environ["zodb.connection"]
            root=conn.root()
            realRoot=root["applicationRoot"]

            host = environ["HTTP_HOST"].lower()
            if host in virtualHosts:
               path = virtualHosts [host] 
               root = realRoot [path]
            try:              
                principalFolder = root["person"]
                principal = principalFolder.getPrincipalByUserName(userName)
            except:
                principalFolder = realRoot["person"]
                principal = principalFolder.getPrincipalByUserName(userName)                
        return app(environ, start_response, principal)

    return secure_application
