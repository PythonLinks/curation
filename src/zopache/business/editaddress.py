import googlemaps

from zope.interface import Interface
from zope.schema._field import Choice
from zope.schema import Text, TextLine, Bool

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.business.interfaces import ICompanyBase
from cromlech.browser.exceptions import HTTPFound
from zopache.forms.interfaces import IApprove

class IAddress(IApprove):    
    address= Text(
        title = u'Address (For the map).',
        description = u'Where is this office located?',
        required = True,
        default = u'',
    )         

@form_component
@name ('editAddress')
@context(ICompanyBase)
class EditAddress (EditForm):
    title = 'Edit the company office address.'
    subTitle = 'This is used to geocode lattitude and longitude.'
    interface = IAddress 
    fields = Fields(IAddress)
    
    def postProcess (self):
        if self.context.address=='':
           raise HTTPFound(self.url(self.context))            
           return 
        gmaps = googlemaps.Client(key='AIzaSyDcxk6rq4CA3dFsUzIwYde5K3fIfCMq8y4')
        # Geocoding an address
        geocode_result = gmaps.geocode(self.context.address)
        result=geocode_result[0][u'geometry'] [u'location']
        self.context.lattitude=float(result [u'lat'])
        self.context.longitude=float(result [u'lng'])
        raise HTTPFound(self.url(self.context))

    
    def acquireTitle(self):
        return 'Edit' + self.context.title + "'s Address "


