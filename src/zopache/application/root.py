import json

    
from zope.interface import implementer

from zopache.core import Container
from zopache.application.interfaces import IRootContainer
from zopache.ttw.principalfolder import PrincipalFolder
from zopache.pages.interfaces import IContent
from zopache.application.allblogobjects import ProcessTree

@implementer(IRootContainer)
class RootContainer(Container,ProcessTree):
    basePath = "/"
    private = False
    icon="ttwicons/Container.svg"
    webClass = "Container"
    __name__ = "applicationRoot"
    branchSize = 0
    
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
                'mensgroups.info': 'mens-groups',
                'mqttchat.info':'mqtt',
                'rights.men':'mens-rights',
                'stopsmog.info': 'smog',                                
                'superwifi.pl':'superwifi',
                'pythonlinks.info':'python',
                'usgreens.info':'us-greens',            
                'desktop.pythonlinks.info':'python'
                }
    
    def __init__(self):
        Container.__init__(self)
        self['person'] = PrincipalFolder()

    def valuesAsList(self):
        result = []
        for item in self.values():
            if IContent.providedBy(item):            
               result.append (item)
        return result

    def getSiteRootFor(self, hostName):
            root = self
            virtualHosts = self.virtualHosts
            if hostName in virtualHosts:
               path = virtualHosts [hostName]
               if path in self:
                  root = self [path]
            return root                  

    def setVirtualHosts(self,value):
        value = json.loads(value)
        self.virtualHosts = value
        self._p_changed = True

    def getVirtualHosts(self):
        return json.dumps(self.virtualHosts, indent=2)
    
    source = property(getVirtualHosts,setVirtualHosts)



    
