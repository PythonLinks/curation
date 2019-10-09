#THERE IS A COPY OF THIS IN zopache.core  as well       
from cromlech.browser.interfaces import IPublicationRoot
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
            context = context.__parent__
            max -= 1
            if max < 1:
                raise TypeError("Maximum location depth exceeded, "                                "probably due to a a location cycle.")
        raise TypeError("Parents needed to  determine location root")

def getSiteRoot(object):
    return getRoot(object, IPublicationRoot)

def getZodbRoot(object):
    return getRoot(object, IZodbRoot)


def getPrincipalFolder(item):
    root = getSiteRoot(item)
    if "person" in root:
        return root["person"]
    else:
        return root.__parent__["person"]

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
