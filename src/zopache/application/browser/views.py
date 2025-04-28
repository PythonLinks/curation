# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.


from cromlech.browser.exceptions import HTTPFound
from cromlech.security import Unauthorized
from crom import target, order
from dolmen.view import name, context, view_component
from cromlech.browser.directives import title

#FROM INTERFACES
from zope.interface import Interface
from dolmen.container import IBTreeContainer
from cromlech.browser.interfaces import IURL, IPublicationRoot
from zopache.application.interfaces import IRootContainer



from zopache.core.page  import  Page


from . import tal_template
from cromlech.security import unauthenticated_principal as anonymous
    
@view_component
@name('logout')
@title("Logout")
@context(Interface)
class Logout(Page):
    title="You are logged out"
    subTitle="Please come back soon!"    
    layoutName = "UserMenu"
    submissionError = ""
    def update(self):
         principal = self.request.principal
         if principal != anonymous:
            principal.logout()
            self.request.principal = anonymous
    
    def render(self):
         return    """ 

<p>
We hope that you enjoyed your visit. 
</p>

<h3>         Click <a href =".."> here </a> to go back.
</h3>
"""
junk = """    
 <script src="https://apis.google.com/js/platform.js" async defer></script>
 <script>
gapi.auth2.getAuthInstance().signOut();
</script>
         """


@view_component
@name('logout2')
@title("Logout")
@context(Interface)
class Logout2(Page):

    def update(self):
        self.request.principal.logout()

    def render(self):
        newURL ='.'
        raise HTTPFound(location=newURL)    

@view_component
@name('')
@context(Unauthorized)
class NoAcces(Page):

    def render(self):
        return "You do not have permission to access that view on that object !"
