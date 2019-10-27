from zopache.ttw.acescripts import AceScripts
class AceScripts (AceScripts):
    def update(self):
        root = self.getRoot()
        self.template = root['Products']['Templates']['TranspilerTemplate']
	
    def  footerScripts(self):
        result = self.aceEditorFooter
        result += """   <script type="text/javascript" src="https://pyodide.cdn.iodide.io/pyodide.js"></script>"""

        result += "<script> //BEGIN"
        root = self.getRoot()
        scripts = root['Products']['Templates']['PythonScripts']
        result += scripts.getJavascript()
        scripts = root['Products']['Templates']['TranspilerScripts']
        result += scripts.getJavascript()

        result = result + "//END</script>"
        return result
