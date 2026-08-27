"""
This form just checks if the user entered a valid domain name,
and if so, redirects them to /person/moauth/<mastodon_server>
which does the real work of the mastodon oauth process flow.
"""

from zope.interface import Interface
from zope.schema import DottedName

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.ttw.interfaces import IPrincipalFolder
from dolmen.forms.base import Actions, Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE


class IDomain(Interface):

    domain = DottedName(
        title = u'Domain Name',
        description = ("the domain name of your "
                       " Mastodon/Fediverse oauth "
                       "server which you wish to use to login here."),
        required = True,
    )

    gdprPermission = schema.Bool(
        title = ("To run this web site, including cookie-based "
                 "authentication."),
        required = True,
        default = False)

    gdprPermission.text = """
    <p> I give permission 
to process my personal information for the following  
purposes:</p>"""
    
class CreateAndUse(Action):

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        domain = data['domain']
        newURL = "/person/moauth/" + domain
        cookieValue = str(data["gdprPermission"])
        form.request.response.set_cookie(
            "gdprPermission",
            cookieValue,
            max_age=(3600),     #one hour
            path="/",
            domain=None,
            secure=True,        # only send over HTTPS
            httponly=True,      # not accessible via JS
            samesite="Strict",  # "Strict", "Lax", or "None"
            )
        return SuccessMarker('Logging In', True, url=newURL)

@form_component
@name ('oauth')
@context(IPrincipalFolder)
class OtherServer (Form):
    title = "Mastodon or Fediverse Oauth Login"
    subTitle = 'Please enter the domain name of your home server.'
    allowAnonymous = True
    interface = IDomain
    fields = Fields(IDomain)
    actions = Actions(CreateAndUse("Login"))
    fields["domain"].htmlAttributes = {"placeholder":
               "e.g. example.social"}
    def acquireTitle(self):
        return "Oauth Login"

