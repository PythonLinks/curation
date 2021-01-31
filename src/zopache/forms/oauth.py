from cromlech.security import permissions
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage
from zopache.core.baseform import Form

class Base(Form):
    count = 0
    def update(self):
            Form.update(self)
            self.template = self.getTemplates()['OauthGoogle']               

@form_component
@context(IPage)
@target(IView)
@name("login")
class GLogin(Base):
    registerURL = "gregister"
    loginURL = ""

@form_component
@context(IPage)
@target(IView)
@name("loginToSubscribe")
class LoginToSubscribe(Base):
    registerURL = "gsubscribe"
    loginURL = "subscribe"

@form_component
@context(IPage)
@target(IView)
@name("loginToDonate")
class LoginToDonate(Base):
    registerURL = "gdonate"
    loginURL = "donate"

@form_component
@context(IPage)
@target(IView)
@name("loginToVolunteer")
class LoginToVolunteer(Base):
    registerURL = "gvolunteer"
    loginURL = "volunteer"            


@form_component
@context(IPage)
@target(IView)
@name("loginToEndorse")
class LoginToEbdorse(Base):
    registerURL = "gendorse"
    loginURL = "endorse"            
    


