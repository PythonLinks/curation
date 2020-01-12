# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from crom import subscription, sources, target
from cromlech.browser.interfaces import IView
from cromlech.security import Unauthorized
from cromlech.security import getSecurityGuards
from cromlech.security.interfaces import ISecurityPredicate
from cromlech.security.meta import permissions
from zope.interface import Interface
from zopache.core.interfaces import ITreeSecurity, IUserSecurity
from zopache.application.treesecurity import TreeSecurity
from zopache.application.usersecurity import UserSecurity

def getPermissions(principal):
          if principal.id == 'user.unauthenticated':
               return []
          return principal.permissions
                

def check_permissions(component, interaction):
    perms = permissions.get(component) or tuple()
    if not perms:
        return
    for principal in interaction.principals:
        access = getPermissions(principal)
        for item in perms:
            if not item  in access:
               return Unauthorized
    return


@subscription
@sources(Interface)
@target(ISecurityPredicate)
def security_predicate(component, interaction):    
    return check_permissions(component, interaction)


def secure_query_view(request, context, name=""):
    check, predict = getSecurityGuards()
    factory = IView.component(context, request, name=name)
    # TEMPORARY TWO LJNES
    #view = factory(context, request)
    #return view
    if predict is not None:
        factory = predict(factory)  # raises if security fails.
    view = factory(context, request)
    check (view)

    if ITreeSecurity.providedBy(view):
        TreeSecurity(view).check()  

    if IUserSecurity.providedBy(view):
        UserSecurity(view).check()          

    return view
