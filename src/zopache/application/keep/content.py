

tomRusselsBlurb = """
<h3>Zopache: The World&#39;s Only:</h3>

<ul>
<li>
<p>graph-based&nbsp;</p>
</li>
<li>
<p>user-friendly&nbsp;</p>
</li>
<li>
<p>web-development platform&nbsp;</p>
</li>
</ul>

"""

appRootSource="""

<h2>Welcome to the ZODB Demo.&nbsp;</h2>

<p>ZODB is an Object Oriented database written in Python.&nbsp; Just subclass off of class Persistent, and your application becomes persistent.</p>

<p>This demo showcases what is possible with the ZODB. &nbsp;In your browser,&nbsp; you can build a sophisticated&nbsp; web application just by adding&nbsp; HTML, CSS, Javascript, Python&nbsp; and Folder (Container) objects.&nbsp; They all have gorgeous editors, HTML objects have both a technical Ace Editor and a WYSIWYG ckEditor.&nbsp;</p>

<p>But this is not just a tool for end users.&nbsp; We invite you jump into file system development.&nbsp; See how easy it is to customize the existing TreeLeaf and TreeBranch objects, to build your own advanced applications.&nbsp;&nbsp;These web tools work well for both beginners and advanced users.&nbsp; Indeed there are hundreds of man years of excellent software engineering hiding under this pretty user interface.&nbsp;</p>

<p>I invite you to get started by <a href="./ckedit">editing this page</a>.&nbsp;</p>

 """

indexSource=""" 
 
 <!DOCTYPE html>
<html lang="en">
  <head>

   <script
        src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
        integrity="sha256-k2WSCIexGzOj3Euiig+TlR8gA0EmPjuc79OEeY5L45g="
        crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    
    <meta content="IE=edge" http-equiv="X-UA-Compatible">
    <meta charset="utf-8" />
    <title> ${view.acquireTitle()}</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="" />
    <meta name="author" content="" />
       <link rel="stylesheet" href="/css" />

    </head>
    <body>
        <center>
            <h1> ${view.acquireTitle()}</h1>
        </center>
    
   <div  class="container"> 
        <div>${structure: view.acquire('Menu')(view)}</div>
        <div> ${structure: view.breadcrumbs()}</div>

        <div> ${structure:context(view)}</div>
          </div>
        <div id="footer">
            <div class="container">
           ${structure: view.acquire('footerSource').source}
           </div>
        </div>
  
    </body>
</html>





"""
cssSource="""
      #siteheader a {
         color: white;
         text-decoration: none;
      }
      
      
      #footer {
          color: white;
  background-color: #464c4a;
  margin-top: 2em
      }

      #footer a {
        color: white;
  font-weight: bold;
      }

      #siteheader {
        width: auto;
  background-color: #004a96;
          margin-bottom: 0em;
          color: white;
      }

      .header-action {
          margin-top: -2em;
      }

      .form-group.required label:after {
          content: "•";
          color: red;
  padding-left: 0.3em;
  font-weight: bold;
      }

"""

footerSource="""

<h3>Credits</h3>

<p><a href="https:PythonLinks.info">PythonLinks.info</a>&nbsp;is built with the&nbsp;<a href="https://ace.c9.io/">Ace Editor</a>,&nbsp;<a href="https://ckeditor.com/">ckEditor</a>, the&nbsp;<a href="https://github.com/PythonLinks/ZodbDemo#zodb--cromlech--introduction-and-demo">Cromlech Toolkit</a>,&nbsp;<a href="https://www.docker.com/">Docker,</a>&nbsp;&nbsp;the&nbsp;<a href="http://https:python.org">Python</a>&nbsp;language,&nbsp; <a href="http://restrictedpython.readthedocs.io/en/latest/">Restricted Python</a> the object-oriented&nbsp;<a href="http://www.zodb.org/en/latest/">ZODB</a>&nbsp;database,&nbsp;&nbsp;<a href="http://uwsgi-docs.readthedocs.io/en/latest/">uwsgi</a>,&nbsp;<a href="https://readthedocs.org/projects/zopeinterface/">Zope.Interface</a>&nbsp;and many other libraries.&nbsp; Thanks to the innumerable open source volunteers who made this project possible.&nbsp;&copy; Christopher Lozinski 2018.&nbsp; Provided to you by <a href="http://PythonLinks.info">PythonLinks.info</a></p>

"""

menuSource= """
<nav class="navbar navbar-default">
<div class="container-fluid">
<div class="navbar-header">
<a class="navbar-brand" href="#">ZODB Demo</a>
</div>
<ul class="nav navbar-nav">
<li><a href="/">Home</a></li>


<li class="dropdown" tal:condition="view">
<a class="dropdown-toggle" data-toggle="dropdown" href="#">
Add  <span class="caret"></span></a>

<ul class="dropdown-menu">
<li><a href="./addContent">Add Content</a></li>
<li><a href="./addContentContainer">Add Container</a></li>
</ul>
</li>
<li><a href="./manage">Manage</a></li>




<li><a href="./logout">Logout</a></li>
</ul>
</div>
</nav>
"""

headerSource="""

"""

from cromdemo.models import TreeRoot
from zopache.ttw.html import HTML,  AceHTML
from zopache.ttw.css import CSS
from zopache.ttw.python import PythonScript
from zopache.ttw.javascript import Javascript, JavascriptFolder
from zopache.ttw.container import HTMLContainer
import transaction
from zopache.ttw.products import Products
from zopache.ttw.webclass import WebClass
from zopache.ttw.webclass import ImutableWebClass

def initialize(root):
            appRoot = root['applicationRoot'] = TreeRoot()
            appRoot.source=appRootSource
            appRoot.title= 'Zopache IDE'
            transaction.manager.commit()

            appRoot.source = 'Version 1'
            appRoot.title= "Version 1"
            transaction.manager.commit()

            appRoot.source = 'Version 2'
            appRoot.title= "Version 2"
            transaction.manager.commit()

            appRoot.source = 'Version 3'
            appRoot.title= "Version 3"
            transaction.manager.commit()


            appRoot.source = tomRusselsBlurb
            appRoot.title= "Zopache IDE"
            transaction.manager.commit()
            
            products=Products()
            appRoot['Products']=products
            
            rootWebClass = ImutableWebClass()
            rootWebClass.title = "Root Web Class"
            products ["Root"] = rootWebClass
            rootWebClass.webClass = None

            containerWebClass = ImutableWebClass()
            containerWebClass.title = "Container Web Class"
            products ["Container"]=containerWebClass
            products.title = "Web Classes"
            containerWebClass.webClass = rootWebClass
            
            homePageWebClass = ImutableWebClass()
            homePageWebClass.title = "Home Page Web Class"
            products ["HomePage"]=homePageWebClass
            homePageWebClass.webClass = containerWebClass
            
            contentWebClass = WebClass()
            contentWebClass.title = "Content Web Class"
            products ["Content"] = contentWebClass
            contentWebClass.webClass = rootWebClass

            folder=HTMLContainer()
            appRoot['Folder']=folder
            
            index=AceHTML()
            index.title='The page layout'
            index.source=indexSource
            rootWebClass['index']=index

            footer=HTML()
            footer.title='The footer html'
            footer.source=footerSource
            rootWebClass['footerSource']=footer


            header=HTML()
            header.title='The header html'
            header.source=headerSource
            rootWebClass['headerSource']=header
            
            css=CSS()
            css.title='Home Page CSS'
            css.source=cssSource
            rootWebClass['css']=css    

            menu=AceHTML()
            menu.title='HTML For the User Menu'
            menu.source=menuSource
            rootWebClass['Menu'] = menu

            helloWorld=PythonScript()
            helloWorld.arguments=''
            helloWorld.source='return \"Hello World\"'
            helloWorld.testURL='/test'
            helloWorld.title='Print Hello World'
            rootWebClass['PythonScript']=helloWorld

            test=AceHTML()
            test.source="${view.acquire('PythonScript')()}"
            test.title="Test the PythonScript"
            rootWebClass['test']=test

            javascriptFolder=JavascriptFolder()
            javascriptFolder.source="function Foo(){} \n"
            javascriptFolder.title="Javascript Folder"
            rootWebClass['JavascriptFolder']=javascriptFolder

            javascript=Javascript()
            javascript.source="function Bar(){} \n"
            javascript.title="Javascript Function Bar"
            javascriptFolder['Bar Function']=javascript            

            javascript2=Javascript()
            javascript2.source="function Zip(){} \n"
            javascript2.title="Javascript Function Zip"
            javascriptFolder['ZipFunction']=javascript2            
            javascriptFolder.createJavascriptCaches()            
