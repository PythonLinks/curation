from zope.interface import implementer

from zopache.core import Container
from zopache.crud.interfaces import IRootContainer
from zopache.ttw.principalfolder import PrincipalFolder

@implementer(IRootContainer)
class RootContainer(Container):
    icon="ttwicons/Container.svg"
    webClass = "Container"

    def __init__(self):
        Container.__init__(self)
        self['person'] = PrincipalFolder()

