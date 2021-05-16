from zopache.ttw.acescripts import AceScripts
from zopache.core.getroot import getProducts

#JUST FOR Transcrypt
class AceScripts (AceScripts):
    def update(self):
        products = getProducts(self.context)
        self.template = products['Templates']['TranspilerTemplate']
        if self.isPython():
           self.addAuthorizedActions()
           
    def  footerScripts(self):
        result = super().footerScripts()
        result += "<script> //BEGIN"
        products = getProducts(self.context)        
        scripts = products['Templates']['PythonScripts']
        result += scripts.getJavascript()
        scripts = products['Templates']['TranspilerScripts']
        result += scripts.getJavascript()

        result = result + "//END</script>"
        return result
