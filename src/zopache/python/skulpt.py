import json
from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from dolmen.forms.base import Actions
from dolmen.forms.base.errors import Error
from dolmen.container import IBTreeContainer ,OrderedBTreeContainer
from dolmen.forms.base import DISPLAY

from zopache.pages.page import Page
from zopache.core import Leaf
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.core.transactionnote import TransactionNote
from zopache.ttw.interfaces import IJSON, IJSONContainer
from zopache.ttw.acescripts import AceScripts
from zopache.ttw.javascript import JavascriptBase
from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *
from zopache.core import Container
from zopache.pages.interfaces import IPage
from zopache.crud.update import Edit
from zopache.crud.forms import AddByTitle, EditForm
from zopache.python.iskulpt import ISolution, ISkulptAssignment

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
           return self._code or self.parent.problemCode

    @property
    def solutionText(self):
        return self.parent.solutionText

    @property
    def showSolution(self):
        return self.parent.showSolution
    
    def getProblemCode(self):
       return self._code or self.parent.problemCode
 
    def setProblemCode(self,value):
        self._code = value

    problemCode = property (getProblemCode, setProblemCode)

@implementer(ISkulptAssignment)
class SkulptAssignment(Page):
    webClass = "Skulpt"
    icon="ttwicons/Python.svg"
    title = ""
    description = ""
    problemText = ""
    timeIsUp = False
    showSolution = False
    problemCode ="""#Please complete this program to solve the problem.
def run():
"""
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
            new._code = context.problemCode
            msg = handle +" Answered: " + self.title
            TransactionNote.describeTransactionWithText(msg)
            transaction.commit()
        return context[handle]

from zopache.crud.forms import AddByTitleForm
from dolmen.forms.base import Fields
from zopache.ttw.htmlviews import CkScripts

def skulptScripts():
         return """
         <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js" type="text/javascript"></script> 
<script src="/root/Products/Templates/Skulpt/skulpt.min.js" type="text/javascript"></script> 
<script src="/root/Products/Templates/Skulpt/skulpt-stdlib.js" type="text/javascript"></script> 
<script src="/root/Products/Templates/Skulpt/fiddle.js" type="text/javascript"></script> 

<script src="/root/Products/Templates/Skulpt/addButtons" type="text/javascript"></script> 

"""

class AssignmentForm(TransactionNote,AceScripts,CkScripts):
    actions = Actions()
    fields = Fields(ISkulptAssignment)

    @property
    def title(self):
        if self.isTeacher():
           return "Edit a Python (Skulpt) Assignment"
        else:
           return self.context.title
       
    def isStudent(self):
        if self.isAuthenticated() and not self.isManager():
           return True
        return False
    
    def isTeacherOrShowSolution(self):
        return self.isTeacher() or self.showSolution
    
    def isTeacher(self):
        return self.isManager()

    def isAnonymousVisitor(self):
        return not self.isAuthenticated()    

    def update(self):
        self.template = self.getTemplates()['Skulpt']
        isAnonymous = self.isAnonymousVisitor()
        isTeacher = self.isTeacher()
        isStudent = self.isStudent()

        if not isTeacher:
            self.fields["title"].mode = DISPLAY
           
        if not isTeacher:
            self.fields["problemText"].mode = DISPLAY

        if isTeacher or isAnonymous:
            self.fields = self.fields.omit('comments')

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

@view_component
@name('addAssignment')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddAssignment(AssignmentForm,AddByTitle):
    title = 'Create a Python (Skulpt) Assignment'
    subTitle= ""
    ignoreContent = True
    factory = SkulptAssignment
    schemaName = "AssignmentSchema"
    interface = ISkulptAssignment
    aceMode = "python"
    def update(self):
        AssignmentForm.update(self)        
        AddByTitleForm.updateWidgets(self)    

@form_component
@context(ISkulptAssignment)
@name("index")
class AceEditSkulpt(AssignmentForm,EditForm):
    aceMode = "python"
    schemaName = "AssignmentSchema"
    title = "class assignment"
    subTitle = "class assignment2"
    interface = ISkulptAssignment
    
    def update(self):
        AssignmentForm.update(self)          
        EditForm.update(self)
        isAnonymous = self.isAnonymousVisitor()
        isTeacher = self.isTeacher()
        isStudent = self.isStudent()

        if not self.context.showSolution and not isTeacher:
             self.fields = self.fields.omit('solutionText')
             self.fields = self.fields.omit('solutionCode')             
   
        if not isTeacher:
            self.fields = self.fields.omit('showSolution')
           
        if self.context.showSolution:
           if not isTeacher:
               self.fields['solutionText'].mode = DISPLAY
               self.fields['solutionCode'].mode = DISPLAY                      
        else:
           if not isTeacher:           
               self.fields = self.fields.omit('solutionText')
               self.fields = self.fields.omit('solutionCode')           
        #AceEditForm.updateWidgets(self)              
        
    def addUnauthorizedActions(self):
        self.actions = Actions()
        
    def addAuthorizedActions(self):
        if self.isTeacher() or self.isStudent():
           self.actions = Actions(
               Edit("Save","Save"))
           
    def extractData(self):
        data, errors = AceEditForm.extractData(self)
        if self.context.timeIsUp and not self.isTeacher():
            errors += Error("Time is up, no more submissions.")
        return data, errors

    def applyData(self,data):
        context = self.context
        if self.isTeacher():
           context.title = data['title'] 
           context.problemText = data['problemText']
           context.problemCode = data['problemCode']           
           context.solutionText = data['solutionText']
           context.showSoltion=data['showSolution']
           context.timeIsUp=data['timeIsUp']           
           msg = "Teacher edited: " + self.title
           self.describeTransactionWithText(msg)
           
        else:
           answer = self.solution() 
           answer.comments = data['comments']
           answer.problemCode = data['problemCode']

           
@form_component
@context(ISkulptAssignment)
@name("asStudent")
@implementer(ITreeSecurity)
class AsStudent(AceEditSkulpt):           
    def isTeacher(self):
       return False
    def isStudent(self):
       return True

@form_component
@context(ISkulptAssignment)
@name("asAnonymous")
@implementer(ITreeSecurity)
class AsAnonymous(AceEditSkulpt):           
    def isTeacher(self):
       return False
    def isAnonymousVisitor(self):
       return True
