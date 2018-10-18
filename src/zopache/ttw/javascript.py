from jsmin import jsmin
from . import tal_template
from html import escape
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from zopache.ttw.interfaces import ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from dolmen.container import IBTreeContainer

from zope.interface import implementer
from dolmen.forms.base import action, name, context, form_component
from dolmen.container import IBTreeContainer,BTreeContainer
from crom import target, order
from cromdemo.interfaces import ITab
from cromlech.browser.directives import title
from cromlech.security import permissions
from zopache.core import Leaf
from zopache.ttw.acescripts import AceScripts
from .interfaces import ISourceContainer
from dolmen.view import name, context, view_component
from cromlech.webob.response import Response
from dolmen.view import View, make_layout_response
from zope.cachedescriptors.property import CachedProperty
from zopache.ttw.interfaces import ISourceLeaf, ISourceContainer
from zopache.ttw.interfaces import IWeb
from zopache.core.page  import  Page
from .interfaces import ITestURL

class IJavascript(ISourceLeaf,ITestURL):
    "Basic Javascript Form"

    title = schema.TextLine(
        title = u'Title',
        description = u'Describe this Javascript Object.',
        required = False,
    )

    source= schema.Text(
        title = u'Javascript Source Code',
        description = u'The Javascript code goes here.',
        required = False,
        default = u' ',
    )

class IJavascriptFolder(IJavascript,IBTreeContainer,ISourceContainer):
        "Basic Javascript Folder Form"
        pass
        

@implementer(IJavascript)      
class Javascript(Leaf):
    icon="ttwicons/Javascript.svg"    
    source =u''
    title=u''
    className='Javascript'

    def getSource(self):
        return self.source

    def getTitle(self):
        return self.__name__

    def getJavascriptObjects(self):
         return [self]

    def getLines(self):
         #NOT QUITE SURE WHAT THE FOLLOWING LINE WAS THERE.
         #result=self.source.replace(' ','mynbsp')
         result=self.source
         result=escape(result)
         #result=result.replace('mynbsp','&nbsp')
         return result.split("\n")

    def commands(self,view):
        manual=view.liHref(
            'http://www.zopache.com/baseicwebobjects/javascript',
             'Javascript Manual')
        return view.beginMenu('Javascript') + index  + edit + history + manual+ view.end 
                
    def __call__(self,view,**args):
            return self.getSource()

    def postProcess(self):
        self.createJavascriptCaches()
        
    def createJavascriptCaches(self):
        parentJavascriptFolders=self.parentsWhichImplement(IJavascriptFolder)

        # YOU MAY WANT TO IMPROVE THIS BY USING THE JSMIN LIBRARY
        for folder in parentJavascriptFolders:
             folder.sourceCache=folder.getSource()

    def parentsWhichImplement(self,interface):
           item=self
           result=[]
           while (item!=None):
             if interface.providedBy(item):
                       result.append(item)
             item=item.__parent__
           return result
                                        
@implementer(IJavascriptFolder)
class JavascriptFolder(Javascript,BTreeContainer):
    source =u''
    sourceCache=u''
    className='Javascript Folder'

    def commands(self,view):
        url=view.url(self)
        index=view.liHref(url+'/index','View')
        rawindex=view.liHref(url+'/rawindex','Raw')
        edit=view.liHref(url+'/edit','Edit')
        history=view.liHref(url+'/history','History')
        manage=view.liHref(url+'/list','Manage')
        search=view.liHref(url+'/manage','Search')
        addJavascriptFolder=view.liHref(url+'/addJavascriptFolder','Add Javascript Folder')
        addJavascript=view.liHref(url+'/addJavascript','Add Javascript')
        jsFolderCommands=(view.beginMenu('JSFolder') + 
                          index +
                          rawindex +
                          edit +
                          manage + 
                          search  + 
                          addJavascript +  
                          addJavascriptFolder +
                          view.end)
        return  jsFolderCommands

    def cacheSource(self):
        self.sourceCache=self.getSource()

    def getSource(self):
        if self.source!=None:
          result=self.source
        else:
          result=u' '  
        for item in self.values():
            result +=item.getSource()
        return result

    def getJavascriptObjects(self):
         result=[]
         for item in self.values():
             if IJavascript.providedBy(item):
                result+= item.getJavascriptObjects()
         return result

    def flatten(self,view):
         result=[]
         count=1
         class Record(object):
              pass
         objects=self.getJavascriptObjects()
         for anObject in objects:
             #JUST A LINE FOR THE FILE
             lines=anObject.getLines()
             o=Record()
             o.line=view.href(view.url(anObject)+'/aceedit', anObject.__name__)
             o.line="<h3>"+o.line+"</h3>"
             o.count=''
             result.append(o)

             for line in anObject.getLines():
                 o=Record()
                 o.line=line.replace(' ','&nbsp;')
                 o.count=view.href(view.url(anObject)+'/aceedit', str(count))
                 count=count+1
                 result.append(o)

         return result


class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/javascript");
        </script>
        """     

    def commands(self):
        manual=self.liHref('http://www.zopache.com/baseicwebobjects/javascript','Javascript Manual')
        return manual 

@form_component
@name('addJavascript')
@context(IBTreeContainer)
@target(ITab)
@title("Add Javascript")
@permissions('Manage')
@implementer(IWeb)
class AddJavascript(AceScripts,AceAddForm):
    subTitle='Add a Javascript Object'
    interface = IJavascript
    ignoreContent = True
    factory=Javascript

    def postProcess(self):
        self.new.postProcess()


    
@form_component
@name('addJavascriptFolder')
@context(IBTreeContainer)
@target(ITab)
@title("Add JavascriptFolder")
@permissions('Manage')
@implementer(IWeb)
class AddJavascriptFolder(AceScripts,AceAddForm):
    subTitle= 'Add a Javascript Folder'
    interface = IJavascriptFolder
    ignoreContent = True
    factory=JavascriptFolder    

    def postProcess(self):
        self.new.postProcess()
        
def make_javascript_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'application/javascript' 
        return response

@view_component
@name('index')
@context(IJavascript)
@title("View Javascript")
class JavascriptIndex(Page):
    responseFactory = Response
    make_response = make_javascript_response
        
    def render(self):
               source = self.context.getSource()
               return minify (source)
    def render(self ):
            if IJavascriptFolder.providedBy(self.context):
                   return self.context.sourceCache
            else: 
                   return self.context.source
               
@form_component
@context(IJavascript)
@target(ITab)
@title("AceEdit")
@name("aceedit")
@permissions('Manage')
class AceEditJavascript(AceScripts,AceEditForm):
    subTitle='Ace Edit this  Javascript'
    label=''
    def breadcrumbs(self):
        return self.breadcrumbsManage()
    
    def postProcess(self):
        self.context.postProcess()

    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    


        
@view_component
@name('search')
@title("Search")
@target(ITab)
@context(IJavascriptFolder)
class Search(Page):
    subTitle=u'Search The Javascript'
    template = tal_template('javascriptFolder.pt')
    subTitle="Search Javascript Folder"
    className='Javacript Folder'

    def breadcrumbs(self):
        return self.breadcrumbsManage()

