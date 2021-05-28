#My version of the Jinja Sandbox


class LoadTemplate(object):
    def __call__(self,name):
        grandParent = self.parent.parent 
        if name in grandParent:
            return grandParent[name].source
        else:
            return f"""Please create a Jinja template called {name} either in 
a parent principal folder or in /Products/Layouts"""


from jinja2.sandbox import SandboxedEnvironment, SecurityError
from zope.interface import Interface

class MyEnvironment(SandboxedEnvironment):
    def is_safe_attribute(self,obj, attr, value):
       if Interface.providedBy(obj):  
           if attr in [
             "name",
             "__name__",
             "title",
             "description",
             "values",
             "items",
             "keys",
             "source",
             "asDict",
             "asString",
             "secureParent"
              ]:
              return True
           else:
              raise SecurityError('You are not allowed to access %r ' % (attr,))

       return SandboxedEnvironment.is_safe_attribute(obj, attr, value)

