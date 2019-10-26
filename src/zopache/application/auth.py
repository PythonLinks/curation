# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from functools import wraps
from cromlech.security import Principal
from cromlech.security import unauthenticated_principal as anonymous
from cromlech.browser import getSession
from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import implementer
from zope.location import Location
from zopache.application.virtualhost import getSiteRoot



def secured(app):

    @wraps(app)
    def secure_application(environ, start_response, default=anonymous):
        session = getSession()
        principal = default
        if session is not None and 'user' in session:
            environ['REMOTE_USER'] = userName = session['user']
            conn = environ["zodb.connection"]
            connRoot=conn.root()
            zodbRoot= connRoot ["applicationRoot"]
            siteRoot = getSiteRoot (environ, zodbRoot)
            principalFolder = siteRoot["person"]
            principal = principalFolder.getPrincipalByUserName(userName)

        return app(environ, start_response, principal)

    return secure_application
