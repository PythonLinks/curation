from zopache.ttw.acescripts import AceScripts
from zopache.core.getroot import getProducts

class AceScripts (AceScripts):
    def update(self):
        products = getProducts(self.context)
        self.template = products['Templates']['TranspilerTemplate']
	
    def  footerScripts(self):
        result = self.aceEditorFooter
        result += """   <script type="text/javascript" src="https://pyodide.cdn.iodide.io/pyodide.js"></script>"""

        result += "<script> //BEGIN"
        products = getProducts(self.context)        
        scripts = products['Templates']['PythonScripts']
        result += scripts.getJavascript()
        scripts = products['Templates']['TranspilerScripts']
        result += scripts.getJavascript()

        result = result + "//END</script>"
        return result
