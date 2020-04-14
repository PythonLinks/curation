from slugify import slugify
from zopache.categories.category import ConferenceVideo
from zopache.pages.uniquename import UniquePageName

def isTime(aString):
    if (
       (len (aString) > 5) and  
       isdigit(aString[0]) and
       isdigit(aString[1]) and
       (aString [2]== ':')  and      
       isdigit(aString[3]) and
       isdigit(aString[4])):
           return True
    return False

def startPositions (aString):
    result = []
    for index, character  in enumerate(aString):
        if isTime(aString [index:]):       
           result.append (index)
    return result


def getSections (aString):
    starts = startPositions (aString)
    ends = []
    #figure out the end positions

    for index, item in enumerate(starts):
        if (index == (len(starts) -1)):
           lastPosition= len(aString) -1
        else:
           lastPositin = starts [index + 1] -1
        ends.append (lastPosition)
        for index in range (len(starts) -1):           
               theString = aString[starts[index:ends[index]]]
               sections.append (theString)


def getDate(video):
    pass


def processVideos(container): 
    for video in container.valuesList():
        theString = video.source
        sections = getSections (theString)
        date = getDate(video)
        print (theString)
        for section in sections:
               print (section)
               minutes = theString [0:1]
               seconds = theString [3:4]
               title = theString [6:]
               new = ConferenceVideo()
               new.title = title + ' ' + date
               newName = slugify (new.title)
               newName = UniquePageName().uniqueName(container, newName, '-')
               new.youTubeId = video.youTubeId 
               new.minutes = minutes
               new.seconds = minutes
               new.conference =video.conference
               video.conference.talks [newName] = new
               video.__parent__ [newName]= new
               new.postProcess()
        IObjectDeleter(item).delete()       
