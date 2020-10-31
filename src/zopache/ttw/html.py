
from zope.interface import implements
from cromlech.security import unauthenticated_principal as anonymous
from dolmen.container import IBTreeContainer, BTreeContainer
from chameleon import PageTemplate
from zopache.core import Leaf
from zope.interface import implementer
from zopache.ttw.interfaces import (ISource,
                                    IHTML,
                                    IAceHTML,
                                    ICkHTML,
                                    ISecureHTML,
                                    IHTMLClass,
                                    IAceHTMLClass,
                                    IUntrustedHTML,
                                    IIndexHTML,
                                    IAceCMSClass,
                                    IAceIFrameClass,
                                    IAceHTMLPage)




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

    def getHTML(self):
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
            if view.count>500:
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
    
@implementer(IAceCMSClass)
class AceCMSHTML(TrustedHTML,Leaf):
    icon="ttwicons/HTML.svg"

@implementer(IAceIFrameClass)
class AceIFrameHTML(TrustedHTML,Leaf):
    icon="ttwicons/HTML.svg"        


@implementer(IAceHTMLPage)
class HTMLPage(TrustedHTML,Leaf):
    icon="ttwicons/HTML.svg"    
    webClass = "Category"
    
@implementer(ISecureHTML)
class SecureHTML(AceHTML):
    icon="ttwicons/SecureHTML.svg"

