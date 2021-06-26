#subject to the CV License Agreement

from dolmen.view import View as DolmenView
from dolmen.view import make_layout_response
from cromlech.webob.response import Response
from zopache.core.breadcrumbs import Breadcrumbs
from . import tal_template
from zopache.core.scripts import Scripts

class View(DolmenView,Breadcrumbs):
    responseFactory = Response

class LayoutView(Scripts,View):
    responseFactory = Response
    make_response = make_layout_response
    template = tal_template('form.pt')
    title = ""
    subTitle = ""
    count = 0

    
