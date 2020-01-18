# -*- coding: utf-8 -*-

# Subject to ZPL and CV License agreements


from dolmen.container import BTreeContainer
from zope.interface import implementer
from .interfaces import IChat
from zopache.crud.interfaces import  IContainer
from zopache.core import Container
from zopache.ttw.html import TrustedHTML

#THIS IS BASICALLYT HE SAME THING AS A
#TTW CONTAINER, BUT THIS ONE IS FOR YOU TO
#CUSTOMIZE
@implementer(IChat)
class ContentContainer(TrustedHTML,Container):
    title = "A Chat Server"
    source=u''
    webClass="Chat"
    def __init__(self):
        Container.__init__(self)
        


