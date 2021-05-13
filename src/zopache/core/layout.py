# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.
#It has been modifeid frm the Cromlech version

import crom
from cromlech.browser import IRequest, ILayout
from cromlech.i18n import getLocale
from cromlech.security import permissions
from cromlech.webob.response import Response
from dolmen.viewlet import ViewletManager, viewlet_manager
from zope.interface import Interface
from dolmen.forms.base import name
from . import tal_template


@viewlet_manager
class SiteHeader(ViewletManager):
    pass

@viewlet_manager
class Breadcrumbs(ViewletManager):
    pass


@viewlet_manager
@permissions('Manage')
class AdminHeader(ViewletManager):
    """Authorized user only
    """
    pass


@viewlet_manager
class ContextualActions(ViewletManager):
    pass


@viewlet_manager
class Footer(ViewletManager):
    pass
from zopache.core.scripts import Scripts

@crom.component
@crom.sources(IRequest, Interface)
@crom.target(ILayout)
class LiteLayout(Scripts):

    responseFactory = Response
    template = tal_template('layout.pt')
    title = u"Cromlech Lite"

    def __init__(self, request, context):
        self.context = context
        self.request = request
        self.target_language = getLocale()

    def namespace(self, **extra):
        namespace = {
            'context': self.context,
            'layout': self,
            'request': self.request,
            }
        namespace.update(extra)
        return namespace

    def __call__(self, content, **namespace):

        environ = self.namespace(**namespace)
        environ['content'] = content
        if self.template is None:
            raise NotImplementedError("Template is not defined.")
        return self.template.render(
            self, target_language=self.target_language, **environ)


@crom.component
@name("UserMenu")
@crom.sources(IRequest, Interface)
@crom.target(ILayout)
class UserMenuLayout(LiteLayout):
    template = tal_template('UserMenuLayout.pt')

#@crom.component
#@name("NoMenu")
#@crom.sources(IRequest, Interface)
#@crom.target(ILayout)
#class NoMenuLayout(LiteLayout):
#    template = tal_template('NoMenuLayout2.pt')    

@crom.component
@name("ThinTop")
@crom.sources(IRequest, Interface)
@crom.target(ILayout)
class ThinTopLayout(LiteLayout):
    template = tal_template('thintop.pt')    
