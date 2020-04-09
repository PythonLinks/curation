#THERE IS A COPY OF THIS IN zopache.core  as well       
from cromlech.browser.interfaces import IPublicationRoot
from BTrees.OOBTree import OOBTree
from zopache.crud.interfaces import IZodbRoot


def getDBRoot(self):
           return (self.request.environ['zodb.connection'].root()
                   ['applicationRoot'])

def getRoot(object,anInterface):
        max = 9999
        context=object
        while context is not None:
            if anInterface.providedBy(context):
                return context
            #IF YOU GET TO ZODB ROOT AND STILL NO STIE ROOT,
            #RETURN NONE
            if ((IZodbRoot.providedBy(context)) and
               (anInterface == IPublicationRoot)):
               return None
            context = context.__parent__
            max -= 1
            if max < 1:
                raise TypeError("Maximum location depth exceeded, "                                "probably due to a a location cycle.")
        raise TypeError("Parents needed to  determine location root")

def getSiteRoot(item):
    root = getRoot(item, IPublicationRoot)
    return root

def getZodbRoot(item):
    return  getRoot(item, IZodbRoot)

def getPrincipalFolder(item):
    root = getSiteRoot(item)
    if ((root != None) and
       ("person" in root)):
        return root["person"]
    else:
        return root['python']["person"]

def getProducts(item):
    root = getZodbRoot(item)
    return root["Products"]

#Here is the old version which was in this file.
"""
def getRoot(object):
        max = 9999
        context=object
        while context is not None:
            if IPublicationRoot.providedBy(context):
                return context
            context = context.__parent__
            max -= 1
            if max < 1:
                raise TypeError("Maximum location depth exceeded, "                                "probably due to a a location cycle.")
        raise TypeError("Parents needed to  determine location root")
"""


class Root(object):

    def getSiteRoot(self):
        return getSiteRoot(self.context)

    def getZodbRoot(self):
        return getZodbRoot(self.context)

    def getPrincipalFolder(self):
        return getPrincipalFolder(self.context)               

    def getProducts(self):
        return getProducts(self.context)       

    def getTemplates(self):
        products = self.getProducts()
        templates = products['Templates']
        return templates

    def getArticles (self):
       siteRoot = self.getSiteRoot()
       if not hasattr(siteRoot,'articles'):
          siteRoot.articles = OOBTree()
       return siteRoot.articles   
