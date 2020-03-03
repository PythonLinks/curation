
#CURRENTLY JUST TO A SINGLE PERSON
#CURRENTLY ONLY USES MAIL QUEUE

from zope import schema

from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.crud.interfaces import ILeaf
from zopache.pages.interfaces import IRootPage
from zopache.crud.forms import AddNamedForm, EditForm
from zopache.application.interfaces import IVirtualHost


#THE IDEA HERE IS THAT THE END USER
#CAN SPECIFY THE ROOT
#NO NEED TO DO IN NGINX
virtualHosts = {
                'berniesupporters.org': 'bernie-sanders',
                'climateactivists.info': 'climate-change',
                'dev.pythonlinks.info':'python',
                'desktop.rights.men':'mens-rights',
                'desktop.climatevideos.info':'climate-change',
                'desktop.forestwiki.com':'forestwiki',
                'ents.climateactivists.info': 'ents',
                'golangvideos.com':'golang',                
                'forestwiki.com':'forestwiki',
                'js.pythonlinks.info':'python',
                'mensgroups.info': 'mens-rights',
                'mqttchat.info':'mqtt',
                'rights.men':'mens-rights',
                'stopsmog.info': 'smog',                                
                'superwifi.pl':'superwifi',
                'pythonlinks.info':'python',
                'desktop.pythonlinks.info':'python'
}



def getSiteRootCore(host,root):
            if host in virtualHosts:
               path = virtualHosts [host]
               #When using Forest Wiki on Dev.PythonLinks.info,
               #There will not  be a python Rootcatgegory.
               if path in root:
                  root = root [path]
            return root

def getSiteRootFromRequest(request,root):
            host = request.domain
            return getSiteRootCore (host,root)

def getSiteRoot ( environ, root):      
            host = environ["HTTP_HOST"].lower()
            return getSiteRootCore (host,root)

@implementer (IVirtualHost)
class VirtualHost(Leaf):
    title = "Virtual Host Definitions" 
    pass

    
@form_component
@name('addVirtualHost')
@context(IRootPage)
@permissions('Manage')
class AddHost(AddNamedForm):
    subTitle='Add a Virtual Host'
    interface = IVirtualHost
    ignoreContent = True
    factory=VirtualHost
    def newName(self,data):
        return "VirtualHost"
    
#HERE IS THE  EDIT FORM
@form_component
@context(IVirtualHost)
@name("edit")
@permissions('Manage')
class EditHost(EditForm):
    subTitle='Edit the VirtualHost Object'    



