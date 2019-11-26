from zope.interface import implementer

from zopache.core import Container
from zopache.crud.interfaces import IRootContainer
from zopache.ttw.principalfolder import PrincipalFolder
from zopache.pages.interfaces import IContent


@implementer(IRootContainer)
class RootContainer(Container):
    icon="ttwicons/Container.svg"
    webClass = "Container"
    __name__ = "applicationRoot"
    branchSize = 0
    def __init__(self):
        Container.__init__(self)
        self['person'] = PrincipalFolder()

    def valuesAsList(self):
        result = []
        for item in self.values():
            if IContent.providedBy(item):            
               result.append (item)
        return result
