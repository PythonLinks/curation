from BTrees.OOBTree import OOBTree
from zope.interface import implementer
from zopache.business.region import RegionBase
from zopache.business.company import Organization
from zopache.business.interfaces import IJSONMapOrganization

class JSONMapOrganization(Organization,RegionBase):
    webClass = 'SmallParty'
    zoom = 3.0
    schemaName = "OrganizationSchema"    
    def __init__(self):
       self.mapPoints =  OOBTree()
       Organization.__init__(self)
       RegionBase.__init__(self)
