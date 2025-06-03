from zope import schema
from zope.interface import Interface
from z3c.schema.email import RFC822MailAddress as Email

from dolmen.container import IBTreeContainer

from zopache.ttw.interfaces import IUntrustedHTML, ICanonical
from zopache.pages.interfaces import (ILocation,
                                      IPage,
                                      IPageBase)

from zopache.json.interfaces import IClass

class IPostalCode(ILocation, IPage):
    title = schema.TextLine(
        title = 'Zip/Postal Code',
        required = True,
    )

class IVoter (IPageBase):
    pass    
