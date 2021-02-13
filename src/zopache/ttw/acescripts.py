from zopache.core.scripts import Scripts
from zopache.core.getroot import getProducts

class  AceScripts(object):
    def  headerScripts(self):
        return """
<script src="https://cdn.jsdelivr.net/ace/1.2.4/min/ace.js"></script>
    """+Scripts.headerScripts(self)
    

    aceEditorFooter="""
<script>
     //var textarea = $('textarea[name= "#form-field-source" ]')[0];
     var textarea= $("#form-field-source")[0];
     //CREATE THE EDITOR
     editorDiv=$ ("#editorDiv")[0];
     var editor = ace.edit(editorDiv);
     editorDiv.style.height= " 100px ";
     editor.setOptions({maxLines: 40});
     editor.setOptions({  minLines: 3});

      //SET THE MODE AND THEME
     editor.setTheme("ace/theme/chrome");   //

      editor.getSession().setMode("ace/mode/javascript");

      //GET THE VALUE FROM THE TEXT AREA
      editor.getSession().setValue(textarea.value);

$("form").submit(function(){
          textarea.value=editor.getSession().getValue();
})
   //HIDE THE TEXT AREA IF ALL ELSE WORKS
       textarea.style.display = "none";
</script>

"""

class  AceScriptJavascript(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/javascript");
        </script>
        """
    
class  AceScriptJSON(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/json");
        </script>
        """
class  AceScriptPug(AceScripts):
        
    def  headerScripts(self):
        result = AceScripts.headerScripts(self)
        return result        
    
    def  footerScripts(self):
        result =  self.aceEditorFooter + """
        <script >editor.getSession().setMode("ace/mode/jade");</script>
 
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.9.0-beta3/beautify.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.9.0-beta3/beautify-html.min.js"></script>
        """     
        result += """
<script  src="https://pythonlinks.info/static/pug/pug.js"></script>
<script  src="/fanstatic/ttwicons/pug-runtime.js"></script>    
        """
        result += "<script>"
        products = getProducts(self.context)
        script = products['Templates']['PugScripts']
        result += script.getJavascript()
        result += "</script>"
        return result

