Original version of merge pug.  Since changed, but useful for testing the text file.

import re

# r"" ignores python \ commands
# \s*  Any white space characters
# {}()$ are special characters, they get escaped
# \w* any number of  [a-zA-Z0-9_].
# The original string
#| ${structure: pug['about'](view=view)}
# [$]matches $  

expression = r"([|]\s*[$]\{\s*structure:\s*pug\[\s*'(\w*)'\s*\]\s*\(\s*view\s*=\s*view\s*\)\s*\})"

text = """
      -->| ${structure: pug['node'](view=view)}<---
      -->| ${structure: pug['node'](view=view)}<---
      -->| ${structure: pug['branch'](view=view)}<---
      -->|   ${  structure:   pug[  'about'  ] (  view = view )  }<---
      -->| ${structure: pug['tree'](view=view)}<---
      -->| ${structure: pug['organizations'](view=view)}<---
      -->| ${structure: pug['content'](view=view)}<---
"""

class MyClass(object):
    def replace(self,text):
        query = re.compile(expression)

        result = query.findall(text)
        for (string,arg) in result:
            new = arg
            #new = self[arg].html
            text = text.replace(string,new)
        print (text)


MyClass().replace(text)       

