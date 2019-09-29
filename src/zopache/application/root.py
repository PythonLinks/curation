from zope.interface import implementer

from zopache.core import Container
from zopache.application.interfaces2 import IRootContainer

@implementer(IRootContainer)
class RootContainer(Container):
    icon="ttwicons/Container.svg"
    webClass = "Container"


