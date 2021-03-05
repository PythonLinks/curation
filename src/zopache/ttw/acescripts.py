from zopache.core.getroot import getProducts
from zopache.core.scripts import Scripts



def createEditorDiv():
        return """
<script>
function createEditorDiv(fieldName){
  var textarea= document.getElementById(fieldName);
  var editorDiv = document.createElement('div');
  editorDiv.id = fieldName+ '-editor'; 
  editorDiv.style.height= " 100px ";
  textarea.after(editorDiv);
  return editorDiv;
}
</script>
       """
    
class  AceScripts(object):    
    def  headerScripts(self):
        result =  Scripts.headerScripts(self) 
        result += createEditorDiv() +   f"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.min.js"></script>
<script  src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/mode-{self.aceMode}.js" type="text/javascript" charset="utf-8"></script>"""
        result += """
<script >
var aceEditors = {};
ace.config.set('basePath','https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/' ); 

//USED BY Coffeescript and SaSS Key Up events. 
var editorDiv;
function createAce(fieldName,mode){
  var textarea= document.getElementById(fieldName);
  editorDiv = createEditorDiv(fieldName);
  var Mode = ace.require("ace/mode/" + mode).Mode;
  var editor = ace.edit(editorDiv);
  aceEditors[fieldName] = editor;
  editor.setOptions({maxLines: 40});
  editor.setOptions({minLines: 3});

      //SET THE MODE AND THEME
     //editor.setTheme("ace/theme/chrome");   
    editor.session.setMode(new Mode());

      //editor.getSession().setMode("ace/mode" + mode);

      //GET THE VALUE FROM THE TEXT AREA
      editor.getSession().setValue(textarea.value);
      
      //HIDE THE TEXT AREA IF ALL ELSE WORKS
      textarea.style.display = "none";
  return editor;
 }

  function saveThenSubmit(event){
  
    for (const [key, editor] of Object.entries(aceEditors)) {
    var textarea= document.getElementById(key);
    textarea.value=editor.getSession().getValue();
     
    }
     
  }  
 
 function createAndSave(fieldName,mode){
     editor = createAce(fieldName,mode);
     const form = document.getElementById('form');
     form.addEventListener('submit', saveThenSubmit);
 }
</script>

    """ 
        return result

    def  footerScripts(self):
      return f"""
<script > createAndSave('form-field-source',"{self.aceMode}");
                </script> """

class  AceScriptPug(AceScripts):
    aceMode = 'jade'        
    
    def  footerScripts(self):
        result = """
<script >
     var  editor = createAce("form-field-source","jade");
</script> """
        
        result += """
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.9.0-beta3/beautify.min.js" ></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.9.0-beta3/beautify-html.min.js"></script>
        """     
        result += """
<script  src="https://pythonlinks.info/static/pug/pug.js" ></script>
<script  src="/fanstatic/ttwicons/pug-runtime.js"></script>    
        """
        result += "<script>"
        products = getProducts(self.context)
        script = products['Templates']['PugScripts']
        result += script.getJavascript()
        result += "</script>"
        return result

