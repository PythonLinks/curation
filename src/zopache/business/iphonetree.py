from zopache.pages.interfaces import IPage
from zope import schema
from zope.interface import Interface


class IPhoneTree(IPage):
    leaders = schema.TextLine(
        title = "Twitter Ids of the Leaders.",
        description = """Space separated Twitter Ids of the 
(preferably 2) leaders.  Include the "@" symbolThese two people 
run this branch of the phone tree. """,
        required = False,
        max_length = 100,
        default = '',
    )

    followers = schema.TextLine(
        title = 'Twitter Ids of the followers.  ',
        description = """If they have followers, do not list them here, 
list them as leaders in the child branches. """,
        required = False,
        max_length = 200,
        default = '',
    )

    remotePages = schema.Text(
        title = 'The URL Segments for parties to include.  ',
        description = "By default include their accounts.",
        required = False,
        max_length = 400,
        default = '',
    )        
    
    remoteNodes = schema.Text(
        title = 'The URL Segments for Remote Child Nodes.  ',
        description = """This is not just a social tree, it is a graph.  This allows yyou to add remote Social Graph nodes to this branch of the tree. If you need this feature, please ask for help.   A future release will have a much easier to use tree widget.  
""",
        required = False,
        max_length = 400,
        default = '',
    )        

class ISocialNode(IPhoneTree):
    pass
