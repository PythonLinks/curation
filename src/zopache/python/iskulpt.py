from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zopache.ttw.interfaces import ICanonical
from zopache.ttw.interfaces import ISourceLeaf
from zopache.zmi.interfaces import IZMI
from zopache.crud.interfaces import IDeletable

class ISkulptSolution(ISourceLeaf,IZMI,IDeletable):
    """Student solution data. """

    comments= schema.Text(
        title = 'Comments',
        description = "Teacher <-> Student comments",
        required = False,
        default = u'',
    )
    
    problemCode= schema.Text(
        title = u'Solution Source Code',
        description = "The student's answer.",
        required = False,
        default = u'',
    )
    

class ISkulptAssignment(ICanonical):

    title = schema.TextLine(
        title = u'Title',
        description = 'The Name of this assignment.',
        default='',            
        required = True,
    )

    #description= schema.Text(
    #    title = 'Description',
    #    description = """A brief description of this problem.""",  
    #    required = False,
    #    default = u'',
    #)
    
    problemText= schema.Text(
        title = 'The problem statement.',
        description = 'Please explain the problem.',
        required = False,
        default = u'',
    )
    
    problemCode= schema.Text(
        title = u'Starting Source Code',
        description = 'Here is the code you give to the students.',
        required = False,
        default = u'',
    )
    
    comments= schema.Text(
        title = 'Comments',
        description = "Notes between the student and teacher."  ,
        required = False,
        default = u'',
    )
    
    solutionText= schema.Text(
        title = u'Explanation of the solution.',
        description = u'An English language explanation of the solution.',
        required = False,
        default = u'',
    )
    
    solutionCode= schema.Text(
        title = 'Solution Code',
        description = 'A correct program which answers the problem.',
        required = False,
        default =
        '',
    )        

#    correctAnswer= schema.Text(
#        title = 'Correct Result',
#        description = 'What the program should return, if left empty, not checked.',
#        required = False,
#        default =
#        '',
#    )    
    
    showSolution = schema.Bool(
        title = 'Show Solution?',
        description = "Show the solution already?",
        required = False,
        default = False,
    )

    timeIsUp = schema.Bool(
        title = 'Time is up?',
        description = "Prevent further answers when the time has run out.",
        required = False,
        default = False,
    )    
