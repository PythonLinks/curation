from zopache.core.scripts import Scripts

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

