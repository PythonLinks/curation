import os
import transaction
import tempfile
from ZODB.ExportImport import ExportImport

from dolmen.view import View
from cromlech.webob.response import Response

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.core.interfaces import ITreeSecurity

def make_file_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or '')
        response.content_type = "application/zodb-export"
        return response

class Base(object):
    def update(self):
        Form.update(self)
        self.renderFile()    
        
    def renderFile(self):
            context = self.context
            parent = context.__parent__

            #IT bACKUPS from the DATA
            #SO FIREST wE HAVE TO COMMIT
            context.__parent__ = None
            transaction.commit()
            
            try:
                return self.doit()
                
            except Exception as error:
                self.status = str( error)
            finally:
                #NOW UNDO THE COMMIT
                context.__parent__ = parent
                transaction.commit()
    
@view_component
@name('forest-wiki-backup')
@context(Interface)
@permissions('Manage')
class Index(View):
    responseFactory = Response
    make_response = make_file_response
    def doit(self):
        with  tempfile.TemporaryFile(prefix="DUP")  as f:
            f = self.context._p_jar.exportFile(context._p_oid, f)
            f.seek (0)
            return f.read()
            
    def render(self):
            return self.renderFile()

from here import HERE


@form_component
@context(Interface)
@target(IView)
@context(Interface)
@name('backup')
@implementer(ITreeSecurity)
class LocalBackup(Base, Form):
        
    def doit(self):
        path = os.path.join(HERE,'data', self.context.name + '.export')
        with  open (path,'wb') as f:
            self.context._p_jar.exportFile(context._p_oid, f)
        self.status='The branch was backed up on the server.'


