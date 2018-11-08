#just to make sure this is included
from dolmen.template import TALTemplate
from os import path
TEMPLATE_DIR = path.dirname(__file__)
def tal_template(name):
    name =  TALTemplate(path.join(TEMPLATE_DIR, name))    
    print ("TEMPLATE = ", path)
    return path
