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


@crom.component
@crom.sources(IRequest, Interface)
@crom.target(ILayout)
class LiteLayout(object):

    responseFactory = Response
    template = tal_template('layout.pt')
    title = u"Cromlech Lite"
    def bootstrap3(self):
        result = """
   <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" 
rel="stylesheet" 
integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" 
crossorigin="anonymous" />
   <script
        src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
        integrity="sha256-k2WSCIexGzOj3Euiig+TlR8gA0EmPjuc79OEeY5L45g="
        crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    """
        return result

    def headerScripts(self):
        return self.bootstrap3()

    def bootstrap4(self):
        return """
    <!-- Include Bootstrap  library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
     
"""

    
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

#@crom.component
#@name("ThinTop")
#@crom.sources(IRequest, Interface)
#@crom.target(ILayout)
#class ThinTopLayout(LiteLayout):
#    template = tal_template('thintop.pt')    
