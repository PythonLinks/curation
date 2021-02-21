from zope import schema
from zope.interface import implementer
from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response

from dolmen.container import IBTreeContainer ,OrderedBTreeContainer

from zopache.pages.page import Page
from zopache.core import Leaf
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.ttw.acescripts import AceScripts
from zopache.core.transactionnote import TransactionNote
from zopache.ttw.interfaces import IJSON, IJSONContainer
from zopache.ttw.javascript import JavascriptBase
from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *
from zopache.core import Container
from zopache.pages.interfaces import IPage
from zopache.crud.update import Edit
from zopache.ttw.interfaces import ISourceLeaf
from zopache.zmi.interfaces import IZMI
from zopache.crud.interfaces import IDeletable

class ISolution(ISourceLeaf,IZMI,IDeletable):
    """Student solution data. """

    comments= schema.Text(
        title = 'Comments',
        description = """A brief introduction of this page.  
                        This is used by the search functions.""",
        required = False,
        default = u'',
    )
    
    code= schema.Text(
        title = u'Solution Source Code',
        description = "The student's answer.",
        required = False,
        default = u'',
    )
    
    result= schema.Text(
        title = 'Result',
        description = """My Solution to the Problem.  """,
        required = False,
        default = u'',
    )    
class ISkulptBase(Interface):
    

    title = schema.TextLine(
        title = u'Title',
        description = 'The Name of this assignment.',
        default='',            
        required = False,
    )

    description = schema.Text(
        title = u'Description',
        description = u'A short optional introductory description.',
        default='',            
        required = False,
    )    
    
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

    correctAnswer= schema.Text(
        title = 'Correct Result',
        description = 'What the program should return, if left empty, not checked.',
        required = False,
        default =
        '',
    )    
    
    showSolution = schema.Bool(
        title = 'Show Solution?',
        description = "Show the solution already?",
        required = False,
        default = False,
    )
from zopache.ttw.interfaces import ICanonical

class ISkulptAssignment(ISkulptBase,ICanonical):
   pass

@implementer(ISolution)
class Solution(Leaf):
    icon="ttwicons/Python.svg"
    _solutionCode = ""
    comments = ""
    result = ""

    @property
    def title (self):
        return  self.parent.title

    @property
    def description(self):
        return self.parent.description

    @property
    def problemText(self):
        return self.parent.problemText
    
    @property
    def problemCode(self):
        return self.parent.problemCode    

    @property
    def solutionText(self):
        return self.parent.solutionText

    @property
    def showSolution(self):
        return self.parent.showSolution
    
    def getSourceCode(self):
       return self._solutionCode or self.parent.problemCode
    def setSourceCode(self,value):
        self._solutionCode = value
    solutionCode = property (getSourceCode, setSourceCode)

    
@implementer(ISkulptAssignment)
class SkupltAssignment(Page):
    icon="ttwicons/Python.svg"
    title = ""
    description = ""
    problemText = ""
    problemCode = ""
    solutionText = ""
    solutionCode = ""
    showSolution = False
    answer = ""
    
    def getContentData(self):
        if self.isStudent():
            return self.studentsWork()
        else:
            return self.context
        
    def studentsWork(self,view):
        principal = view.request.principal
        handle = principal.title
        context = self.context
        if not handle in context:
            context[handle]= new = Skupt()
            new._solutionCode = context.problemCode
            msg = handle +" Answered: " + self.title
            TransactionNote.describeTransactionWithText(msg)
            transaction.commit()
        return context[handle]

from zopache.crud.forms import AddByTitleForm
from dolmen.forms.base import Fields
from zopache.ttw.htmlviews import CkScripts

class AllScripts(AceScripts, CkScripts):
    fields =  Fields(ISkulptAssignment)    
    def isStudent(self):
        if self.isAuthenticated() and not self.isManager():
           return True
        return False
    
    def isTeacher(self):
        return self.isManager()
    
    def isAnonymousVisitor(self):
        return not self.isAuthenticated()
    
    def headerScripts(self):
        return CkScripts.headerScripts(self) + AceScripts.headerScripts(self)
    
    def footerScripts(self):
         result = """ <script>
           createAce("form-field-problemCode","python");
           """

         if self.isTeacher():
           result +="""  
        CKEDITOR.replace('form-field-problemText',
       {disableNativeSpellChecker : false}); 
        CKEDITOR.replace('form-field-solutionText',
       {disableNativeSpellChecker : false}); 
         """

         if self.isTeacher() or self.context.showSolution == True:
             result += """ 
           createAce("form-field-solutionCode","python");
           """
         result += """    
         const form = document.getElementById('form');
         form.addEventListener('submit', saveThenSubmit);    
         </script>"""
         return result
    interface = ISkulptAssignment
    aceMode = "python"
    @property
    def title(self):
        if self.isTeacher():
           return "Edit a Python (Skulpt) Assignment"
        else:
           return self.context.title

    @property
    def subTitle(self):
        if self.isTeacher():
           return ""
        else:
           return self.context.description
    
    def update(self):
        isAnonymous = self.isAnonymousVisitor()
        isTeacher = self.isTeacher()
        isStudent = self.isStudent()

        if not isTeacher:
            self.fields = self.fields.omit("title")
            self.fields = self.fields.omit("description")
           
        if not isTeacher:
            self.fields["problemText"].mode = DISPLAY

        if isTeacher or isAnonymous:
            self.fields = self.fields.omit('comments')
            
         
@form_component
@name('addSkulpt')
@context(IPage)
@implementer(ITreeSecurity)
class AddSkulptProblem(AllScripts,AddByTitleForm):
    aceMode = "python"
    title = 'Create a Python (Skulpt) Assignment'
    subTitle= "Don't make it too hard"
    interface = ISkulptAssignment
    ignoreContent = True
    factory=SkupltAssignment
    def update(self):
        AllScripts.update(self)        
        #AddByTitleForm.updateWidgets(self)

@form_component
@context(ISkulptAssignment)
@name("index")
class AceEditSkulpt(AceScripts,AceEditForm):
    def update(self):
        AllScripts.update(self)
        isAnonymous = self.isAnonymousVisitor()
        isTeacher = self.isTeacher()
        isStudent = self.isStudent()        
        if not self.context.showAnswer and not isTeacher:
             self.fields = self.fields.omit('answer')
   
        if not isTeacher:
            self.fields = self.fields.omit('showAnswer')
           
        if self.context.showAnswer:
           if not isTeacher:
               self.fields['solutionText'].mode = DISPLAY
               self.fields['solutionCode'].mode = DISPLAY                      
        else:
           if not isTeacher:           
               self.fields = self.fields.omit('solutionText')
               self.fields = self.fields.omit('solutionCode')           
        #AceEditForm.updateWidgets(self)            

    def addUnauthorizedActions(self):
        self.actions = DoNothing()
        
    def addAuthorizedActions(self):
        if self.isTeacher() or self.isStudent():
           self.actions = Actions(
               Edit("Save","Save")),
        #Do nothing if anonymous visitor.
           
    def applyData(self,data):
        context = self.context
        if self.isTeacher():
           context.title = data['title'] 
           context.description = data['description']
           context.source = data['source']
           context.solution = data['solution']
           context.showSoltion= True if 'showSolution' in data else False
           msg = "Teacher edited: " + self.title
           TransactionNote.describeTransactionWithText(msg)
           
        else:
           answer = self.solution() 
           answer.comments = data['comments']
           answer.source = data['source']
           answer.solution = data['solution']

@form_component
@context(ISkulptAssignment)
@name("asStudent")
@implementer(ITreeSecurity)
class AsStudent(AceEditSkulpt):           
    aceMode = "python"
    def isTeacher(self):
       return False
    def isStudent(self):
       return True


@form_component
@context(ISkulptAssignment)
@name("asAnonymous")
@implementer(ITreeSecurity)
class AsStudent(AceEditSkulpt):           
    aceMode = "python"
    def isTeacher(self):
       return False
    def isAnonymousVisitor(self):
       return True
   
