from BTrees.OOBTree import OOBTree
from zope.interface import implementer
from zopache.business.region import RegionBase
from zopache.business.company import Organization
from zopache.business.interfaces import IJSONMapOrganization
from zopache.pages.location import LocationContainer
from zopache.json.jsonproperties import LocalOrganizationProperties

@implementer(IJSONMapOrganization)
class JSONMapOrganization(LocalOrganizationProperties,RegionBase):
    webClass = 'SmallParty'
    zoom = 3.0
    schemaName = "OrganizationSchema"    
    def __init__(self):
       RegionBase.__init__(self)

