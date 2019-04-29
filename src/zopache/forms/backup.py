from dolmen.view import View
from zopache.core.viewdecorators import *
from ZODB.ExportImport import ExportImport
from cromlech.webob.response import Response

def make_file_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or '')
        response.content_type = "application/zodb-export"
        return response

@view_component
@name('forest-wiki-backup')
@context(Interface)
@title("Backup To Your Computer")
class Index(View):
    responseFactory = Response
    make_response = make_file_response
            
    def render(self):

            import tempfile
            context = self.context
            parent = context.__parent__
            context.__parent__ = None
            with tempfile.TemporaryFile(prefix="DUP") as f:
                f = context._p_jar.exportFile(context._p_oid, f)
                f.seek (0)
                return f.read()
            context.__parent__ = parent
            assert(context.__parent__)            

