import crom
from zope import schema
from zopache.pages.interfaces import IPage
from zopache.zmi.interfaces import IURLSegment

class IIodide(IPage):

    title = schema.TextLine(
        title = u'Page Name',
        description = u'Describe this page.',
        required = True,
    )

    description= schema.Text(
        title = u'Description',
        description = """A brief introduction of this Iodide Notebook""",  
        required = False,
        default = u'',
    )
    
    source= schema.Text(
        title = u'Content',
        description = u'This is the main content for this page',
        required = False,
        default = u'',
    )


@crom.adapter
@crom.sources(IIodide)
@crom.target(IURLSegment)
class IIodideAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'manage'
