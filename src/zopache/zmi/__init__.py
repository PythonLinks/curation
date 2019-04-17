# this directory is a package
from zope.i18nmessageid import MessageFactory
i18n = MessageFactory("zopache.zmi")

from dolmen.template import TALTemplate
from os import path
TEMPLATE_DIR = path.dirname(__file__)
def tal_template(name):
    return TALTemplate(path.join(TEMPLATE_DIR, name))

from fanstatic import Library
library = Library('zmiicons', 'zmiiconsLibrary')
