import requests
import json, pprint
import pathlib
# variable region


BASE_URL = "http://saral.navgurukul.org/api/courses"
coursesJsonData={}
exercisData = {}
def printText(text):
    print ("\n\n\t"+"*"*20+text+"*"*20+"\t\n\n")

printText("WELCOME TO SARAL")    

# calling API by get in function.
def getResp(api):
    getData = requests.get(api)                                                     
    coursesJsonData = getData.json()
    return coursesJsonData


# Write json_data in courses.json file. 
def writeData(data,fileName):
    with open(fileName, "w") as writeIt: 
	    writeIt.write(json.dumps(data))
    writeIt.close()


# Read the json_data from courses.json file.
def readData(fileName):
    with open(fileName, "r") as readIt: 
        readJson = json.load(readIt)
    return readJson

# Chacking the file exists or not.
def getData(fileName,url):
    file = pathlib.Path(fileName)
    if file.exists ():
        readJsonData = readData(fileName)
        coursesJsonData=readJsonData

    else:
        coursesJsonData=getResp(url)
        writeData(coursesJsonData,fileName)

    return coursesJsonData
coursesJsonData = getData("courses.json",BASE_URL)

# Using while loop for print courses Names.
def getCourses(jsonData):
    index = 0
    while index<len(jsonData["availableCourses"]):
        id = (jsonData["availableCourses"][index]["id"])
        print  (str(index+1)+"."+jsonData["availableCourses"][index]["name"]),id
        index = index+1
getCourses(coursesJsonData)

printText("*"*10)

# I created a function to take users from the user.
users = input("Enter your course number :- ")
courseId = (coursesJsonData["availableCourses"][int(users)]["id"])
courseName=(coursesJsonData["availableCourses"][int(users)]["name"])
print (courseId)

# Calling  API for print the exercises of the courses.

printText("EXERCISES OF COURSES")  
print (courseName)
exerciseUrl = BASE_URL+"/"+str(courseId)+"/exercises"
exercisData = getData("exercisesFolder/exercises_"+str(courseId)+".json",exerciseUrl)
exercisesIdList = []
sluglist = []
def getExercises(exercisesData):
    
    index1 = 1
    while index1<len(exercisesData["data"]):
        useExercisesId = exercisesData["data"][index1]["id"]
        print  str(index1)+"."+exercisesData["data"][index1]["name"],useExercisesId
        slug=exercisesData["data"][index1]["slug"]
        sluglist.append(slug)
        
        exercisesIdList.append(exercisesData["data"][index1]["id"])

        index2 = 0
        while index2<len(exercisesData["data"][index1]["childExercises"]):
            print ("\t"+str(index2+1)+":"+exercisesData["data"][index1]["childExercises"][index2]["name"])
            index2 += 1
        index1 = index1+1  
    return sluglist
        
exercisesId = getExercises(exercisData)

userWant = raw_input("IF YOU WANT TO GO UP SIDE SO ENTER (up) IF YOU WANT NO SO ENTER (no)")
if userWant == "up":
    print getCourses(coursesJsonData)
elif userWant == "no":

    #USING 3TH API FOR PRINT PERENTEXERCISE SLUG

    users = input("Enter Your  Choice Exercises ID")
    inputId  = exercisesId[users-1]

    printText("CONTENT OF EXERCISES")
    useExercisesId = exercisData["data"][users]["id"]
    contentUrl = BASE_URL+"/"+str(users)+"/"+"exercise"+"/"+"getBySlug?slug="+str(inputId)
    contentJsonData = getData("parentContentFolder/content_"+str(users)+".json",contentUrl)
    content = contentJsonData["content"]
    print "\n YOUR CHOICE ID CONTENT\n"
    print content
    printText("*"*10)

    # FOR CHILDEXERCISES SLUG USING 3TH API.
    chidExerciseData = exercisData["data"][users]["childExercises"]
    childSlug=[]
    index3 = 0
    while index3<len(chidExerciseData):
        print ("\t"+str(index3+1)+":"+chidExerciseData[index3]["name"])
        childSlug.append(chidExerciseData[index3]["slug"])
        index3+=1

    user1 = input("CHOICE YOUR LASSON")
    input1Id = childSlug[user1-1]

    printText("CONTENT OF CHILDEXERCIS :)")
    child_ID = exercisData["data"][users]["childExercises"][user1-1]["id"]
    print child_ID
    cContentURl = BASE_URL+"/"+str(child_ID)+"/"+"exercise"+"/"+"getBySlug?slug="+str(input1Id)
    def childData(child_ID,cContentURl):
        childJson = getData("childContentFolder/childContent_"+str(child_ID)+".json",cContentURl)
        childContent = childJson["content"]
        return childContent


    slugData = childData(child_ID,cContentURl)
    print slugData

    #USING WHILE LOOP FOR NEXT AND PREVIOUS CONTENT. 

    index4  = 0
    while index4<len(childSlug):
        userNextP = raw_input("IF YOU WANT NEXT CONTENT SO ENTER (n) AND IF YOU WANT PREVIOUS CONTENT SO ENTER (P) :)")
        if userNextP == "n":
            user1 = user1+1
            input2Id = (childSlug[user1-1])
            print input2Id
            nextSlugId = exercisData["data"][users]["childExercises"][user1-1]["id"]
            nextcontentURL = BASE_URL+"/"+str(nextSlugId)+"/"+"exercise"+"/"+"getBySlug?slug="+str(input2Id)
            print nextcontentURL
            nextcontent = childData(nextSlugId,nextcontentURL)
            print nextcontent
        elif userNextP == "p":
            users3 = user1-1
            if users3 == 0:
                break
    
            else:
                input3Id = (childSlug[users3])
                previouSlugId = exercisData["data"][users]["childExercises"][users3-1]["id"]
                preContentURL = BASE_URL+"/"+str(previouSlugId)+"/"+"exercise"+"/"+"getBySlug?slug="+str(input3Id)
                previouscontent = childData(previouSlugId,preContentURL)
                print previouscontent
                print users3
        index4 += 1

    print "THERE IS NO CONTENT"



    