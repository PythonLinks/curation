from cromlech.webob.response import Response
from dolmen.view import  make_view_response
from cromlech.security import unauthenticated_principal as anonymous

from zopache.core import View
from zopache.core.breadcrumbs import Breadcrumbs
from dolmen.forms.base import Actions
from zopache.crud import actions as formactions, i18n as _
from . import actions  as ttwactions
from .interfaces import IUntrustedHTML

from chameleon import PageTemplate
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from .interfaces import ISource,IHTML, IAceHTML,ICkHTML, ISecureHTML
from zopache.crud.forms import AddForm, BaseEditForm, EditDemoForm
from zope.interface import implementer
from dolmen.forms.base import action, name, context, form_component
from dolmen.container import IBTreeContainer, BTreeContainer
from crom import target, order
from cromlech.browser.directives import title
from cromlech.security import permissions
from zopache.core import Leaf
from zopache.ttw.acescripts import AceScripts
from zopache.ttw.interfaces import IWeb
from dolmen.view import name, context, view_component
from zopache.ttw.interfaces import IHTMLClass,IAceHTMLClass,IIndexHTML
from zopache.ttw.interfaces import IAceHTMLPage
from zopache.core.interfaces import ITreeSecurity

"""
HTML is a very important base class.  It has a field called source.  It 
can be edited witht the WYSIWYG ckEditor or the more technical Ace Editor.
So those are two different views of the class. 

The ckEditor by default strips out the <html><head> and <body> tags. 
That is great for a CMS, but for beginners might be better to leave it in. 

Historically Trusted HTML used Chameleon Page Tempaltes. 
UntrustedHTML just used html.  Now they are merging together, 
with a trusted variable. 

""" 
class HTMLRecursionError(Exception):
        pass
from zopache.zmi.interfaces import IURLSegment
from zopache.ttw.interfaces import ICkHTML



class HTMLBase(object):
    trusted = False    
    title=u'HTML Object'
    source=''

    #THIS SHOULD BE RETIRED
    #AND ONLY HTML USED. 
    def html(self):
        return self.source    

    def getTitle(self):
        if hasattr(self,'title') and self.title!= None and len(self.title)>0:
           return self.title
        else: 
           return 'Please edit the  Title'


class TrustedHTML(HTMLBase):
    trusted = True    
    icon="ttwicons/CkHTML.svg"

    def setTemplate(self):
            if self.trusted == False:
               return     
            if not hasattr(self,'_v_compiledTemplate'):
               self.compileTemplate()
            #return self._v_compiledTemplate 

    def getHTML(self):
        return self.source

    def compileTemplate(self):
                 if self.trusted == False:
                    return     
                 source=self.getHTML()
                 self._v_compiledTemplate = PageTemplate(source)
                 #return self._v_compiledTemplate

    def postProcess(self,view=None):
            principal = view.request.principal
            if principal == anonymous:
               self.trusted = False
               return
       
            if 'Python' in view.request.principal.permissions:
               self.trusted = True
               self.compileTemplate()
            else:
               self.trusted = False

    def postAddProcess(self,view=None):
            self.postProcess(view=view)
            
    #So here we pass the context into the template    
    def __call__(self,view,**args):
        if self.trusted == False:
           return self.getHTML()      
        try:
            view.count+= 1
            if view.count>50:
                raise HTMLRecursionError()
            context=view.context
            return self.callWithContext(view,context,**args)
        except AttributeError as error:
            result =  """COULD NOT DISPLAY THAT PAGE.
                      HERE IS THE ERROR MESSAGE:\n<br>"""
            result += str(error)
            return result
    
    def render(self,extraArg,**args):
            if self.trusted == False:
               return self.getHTML()     
            self.setTemplate()
            return self._v_compiledTemplate(**args)
                               
        
    def callWithContext(self,view,context,**args):
            if self.trusted == False:
               return self.getHTML()
       
            self.setTemplate()
            return self._v_compiledTemplate(
                           context=context,
                           request=view.request,
                           view=view,
                           **args)


@implementer (IUntrustedHTML)
class UntrustedHTMLBase(HTMLBase):

    def setTemplate(self):
        pass

    def compileTemplate(self):
        pass


    def __call__(self,view,**args):
            return self.getHTML()

class UntrustedHTML(UntrustedHTMLBase,Leaf):
    source = """
<html>
  <head>
  </head>
  <body>
    Hello World
  </body>
</html>
"""

    
@implementer(IHTMLClass)
class HTML(TrustedHTML,Leaf):
   pass

@implementer(IAceHTMLClass)
class AceHTML(TrustedHTML,Leaf):
    icon="ttwicons/HTML.svg"

@implementer(IAceHTMLPage)
class HTMLPage(TrustedHTML,Leaf):
    icon="ttwicons/HTML.svg"    
    webClass = "Category"
    
@implementer(ISecureHTML)
class SecureHTML(AceHTML):
    icon="ttwicons/SecureHTML.svg"


class AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/html");
        </script>
        """

class CkScripts(object):
    def  headerScripts(self):
        return """
<script src="https://cdn.ckeditor.com/4.4.4/standard/ckeditor.js"></script> 
        """ + AddForm.headerScripts(self)
    
    def  footerScripts(self):
        return """
 <script >CKEDITOR.replace('form-field-source',{disableNativeSpellChecker : false}); 
</script>
        """ 


class AddHTMLBase(object):
    interface = IHTML
    ignoreContent = True


class AddCkHTMLBase(AddHTMLBase,CkScripts):
    subTitle="Add an HTML Object"
    factory=HTML

    def footerScripts(self):
        return CkScripts.footerScripts(self)

    def headerScripts(self):
          return CkScripts.headerScripts(self)

    @property
    def actions(self):
        return Actions(
              formactions.AddAndView(_("Add and View","Add -> View"), self.factory),
              ttwactions.AddAndCkEdit(_("Add and ckEdit","Add -> ckEdit"), self.factory),
              ttwactions.AddAndAceEdit(_("Add and AceEdit","Add -> AceEdit"), self.factory),
              formactions.Cancel(_("Cancel","Cancel")))


@form_component
@name ('addChameleon')
@context(IBTreeContainer)
@permissions('Manage')
class AddCkHTML(AddCkHTMLBase,AddForm):
    pass


class AddAceHTMLBase(AddHTMLBase,AceScripts,AddForm):        
    subTitle="Add an Ace HTML Object"
    factory=AceHTML

    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)      
    @property
    def actions(self):
        return Actions(
              formactions.AddAndView(_("Add and View","Add -> View"), self.factory),
              ttwactions.AddAndAceEdit(_("Add and AceEdit","Add -> AceEdit"), self.factory),
              formactions.Cancel(_("Cancel","Cancel")))


@form_component
@name (u'addAceChameleon')
@context(IBTreeContainer)
@permissions('Manage')
class AddAceHTML (AddAceHTMLBase,AddForm):
    pass


@form_component
@name ('addHTML')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddUntrustedHTML (AddAceHTMLBase,AddForm):
    factory = UntrustedHTML 
    subTitle="Add an HTML Object"

@view_component
@name('index')
@context(IIndexHTML)
class Index(View,Breadcrumbs):
    count=0
    responseFactory = Response
    make_response = make_view_response
    def setDisplayObject(self,item):
        self.zopacheTemplate=item

        
    def render(self):
        #In the case of /index/index
        if not hasattr(self,'zopacheTemplate'):
               self.zopacheTemplate=self.context
               self.context=self.context.__parent__
        try:
               return self.zopacheTemplate(self)
        except HTMLRecursionError:
               return ('Your templates recursion exceeded 50 calls'+
                      self.zopacheTemplate.source)               

class BaseAceEdit(AceScripts,BaseEditForm):
    subTitle="Ace Edit this object"
    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    


class AceEdit(BaseAceEdit):
    @property
    def actions(self):

        action1=ttwactions.SaveAndAceEdit("Save","Save")
        action2=formactions.SaveAndView("Save  and View","Save -> View")

        action3=ttwactions.SaveAndCkEdit(
                "Save and CkEdit","Save -> ckEdit")
        
        action4=formactions.SaveAndTest(
                "Save and Test","Save -> Test")        

        action5=formactions.Cancel("Cancel","Cancel")
        if ICkHTML.providedBy(self.context):
                return Actions(action1,action2,action3,action4,action5)
        return Actions(action1,action2,action4,action5)                
        
#HERE IS THE DEVELOPER ACE EDIT FORM
@form_component
@context(IAceHTML)
@name("aceedit")
@implementer (ITreeSecurity)
class AceEditForm(AceEdit):
    pass


#AND HERE IS THE DEMO ACE EDIT FORM
@form_component
@context(IAceHTML)
@name("acedemo")
class AceDemoHTML(BaseAceEdit):
    subTitle = "Saving is disabled in this demo."            
    @property
    def actions(self):
        return Actions()


class BaseCkEdit(CkScripts,BaseEditForm):
    subTitle="CkEdit this object"        
    
    def footerScripts(self):
        return CkScripts.footerScripts(self)

    def headerScripts(self):
          return CkScripts.headerScripts(self)    


class CkEdit(BaseCkEdit):
    @property
    def actions(self):
        return Actions(
              formactions.SaveAndView(_("Save  and View","Save -> View")),
              ttwactions.SaveAndCkEdit(_("Save","Save")),
              ttwactions.SaveAndAceEdit(_("Save  and AceEdit","Save -> AceEdit")),
              formactions.SaveAndTest(_("Save  and Test","Save -> Test")),                   formactions.Cancel(_("Cancel","Cancel")))


        
        
#HERE IS THE CKEDIT FORM
@form_component
@context(ICkHTML)
@name('ckedit')
@implementer(ITreeSecurity)
class CkEditForm(CkEdit):
      pass


#AND HERE IS THE CkDemo Form
@form_component
@context(ICkHTML)
@name('ckdemo')
class CkDemoHTML(BaseCkEdit):
    subTitle = "Saving is disabled in this demo."    
    @property
    def actions(self):
        return Actions()

@view_component
@name('viewsource')
@context(IIndexHTML)
class ViewSource(Index):
    def render(self):
            top="<html><head></head><body>"
            middle=self.context.source
            bottom="</body></html>"
            return top+middle+bottom

@view_component
@name('index')
@context(IUntrustedHTML)
class ViewSource(Index):
    def render(self):
        return self.context.source


