

begin ="""
<style>
    .navbar {
        background-color: #00b563;
    }
</style>
<nav class="navbar navbar-expand-md navbar-dark default-color"><button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExample04" aria-controls="navbarsExample04" aria-expanded="false" aria-label="Toggle navigation" style="background-color: green;"><span class="navbar-toggler-icon"> </span></button>
    <div class="collapse navbar-collapse" id="navbarsExample04">
      <ul class="navbar-nav mr-auto">
"""  

end = """
        </ul>
    </div>
</nav>
"""

from zope.interface import implementer
from zopache.core import Leaf
from zopache.application.interfaces import IMenuBar

@implementer (IMenuBar)
class MenuBar(Leaf):

    def render(self,view):
        result = begin

        for item in self.json:
            link = "/about"
            text = "Hello"
            
            result  += F"""
            <li class="nav-item"><a class="nav-link" href="{{url}}">
             {{text}}
            </a></li>"""

            result += end
            return result

import json
from dolmen.forms.base.errors import Error, Errors
from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson, EditJson
from zopache.core.interfaces import ITreeSecurity
class MultilingualBase(object):
    def applyData(self,data):
        context = self.target()
        jsonSchemaDict =self.jsonSchemaDict
        requestJsonDict = self.requestJsonDict                
        context.json = json.loads(data["json"])        
        self.context._p_changed = True
        return Errors()    

@form_component
@name ('ckedit')
@context(IMenuBar)
@implementer(ITreeSecurity)
class EditMultilingual (MultilingualBase,EditJson):
    title = 'Edit this MenuBar.'
    subTitle = 'Supports multiple languages.'
    schemaName = "MenuBarSchema"  
    def contextJsonDict(self):
        return self.context.json

from zopache.pages.interfaces import IPageBase
@view_component
@name('addMenuBar')
@target(IView)
@context(IPageBase)
class AddMultilingual(MultilingualBase,AddJson):
    title = "Add a Menu Bar"
    subTitle = "Supports multiple languages"
    factory = MenuBar
    schemaName = "MenuBarSchema"

    def newName(self,data):
        newName =  self.requestJsonDict['title']
        return newName
        
    def dataModel(self):   
        return   self.template['newMenuBar'].getAsString()
    
        
