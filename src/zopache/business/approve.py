
from zopache.core.viewdecorators import *
from zopache.business.interfaces import ICompanyBase
from cromlech.browser.exceptions import HTTPFound
from zopache.forms.interfaces import IApprove
from zopache.business.interfaces import IAddress
from zopache.business.geocoding import GeoCode
from zope.schema import Text
from zopache.business.geocoding import Address
from zopache.business.interfaces import ICompanyOrOrganization
from zopache.ttw.html import CkEditForm


class IApproveCompany(IApprove):
    address= Address(
        title = u'Company Address',
        description = """This is used to 
                 locate the organization on the map.  You need at least a street name.  If you only give the city, multiple organizations will share the same pin, and only one will be visible. """,
        required = False
    )    


@form_component
@name ('ckEdit')
@context(IAddress)
class EditAddress (CkEditForm,GeoCode):
    title = 'CkEdit this object.'
    subTitle = """This form is used to geocode lattitude and longitude.
"""

@form_component
@name ('approve')
@context(ICompanyOrOrganization)
class Approve (CkEditForm):
    title = 'Edit the company address.'
    subTitle = """This is used to geocode lattitude and longitude.
"""
    interface = IApproveCompany
    fields = Fields(IApproveCompany)
    

    

