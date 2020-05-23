from zope import schema
from zope.interface import Interface
from cromlech.webob.response import Response

from dolmen.view import View, make_view_response

from dolmen.container import IBTreeContainer

from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.ttw.interfaces import ISourceLeaf
from zopache.ttw.interfaces import ITestSource as ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.crud.forms import EditDemoForm
from zopache.ttw.acescripts import AceScripts

from zopache.core.interfaces import ITreeSecurity
from dolmen.container import IBTreeContainer

class IEmail(Interface):

    title = schema.TextLine(
        title = 'Subject',
        description = u'Please Email Subject Line.',
        required = True
    )

    source= schema.Text(
        title = u'Email Body',
        description = u'The body of the Email.',
        required = True
    )


@implementer(IEmail)
class Email(Leaf):
      pass
  
class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/text");
        </script>
        """
    

@form_component
@name('addEmail')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddEmail(AceScripts,AceAddForm):
    subTitle='Create an Email'
    interface = IEmail
    ignoreContent = True
    factory=Email
    

def make_css_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'text'
        return response    

@view_component
@name('index')
@context(IEmail)
class Index(View):
    responseFactory = Response
    make_response = make_css_response
        
    def render(self):
               body = view.context.source
               return F"""
<html>
<body>
<b>Subject:<b> {self.context.title}<br>

<b>Message:</b><br>
{body}
</body>
</html>
"""



#AND HERE IS THE ACE DEMO FORM

#HERE IS THE ACE EDIT FORM
@form_component
@context(IEmail)
@name('acedemo')
class AceDemoCSS(AceScripts,EditDemoForm):
    subTitle='Edit an Email, sending disabled'



#HERE IS THE ACE EDIT FORM
@form_component
@context(IEmail)
@name('aceedit')
@implementer(ITreeSecurity)
class AceEditCSS(AceScripts,AceEditForm):
    subTitle='Edit an Email'

        
