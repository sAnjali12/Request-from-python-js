// declaration of function
const raw_input = require('readline-sync').question;
function firstApi(url){
    const axios = require('axios')
    return response = axios.get(url)
}
//functon calling
BASE_URL = "http://saral.navgurukul.org/api/courses"
var response=firstApi((BASE_URL))

//promises
console.log("       "+"*************@ WELLCOME TO SARAL COURSE @************"+"\n")
function coursesIdname(data){
    var allData;
    var user_choice;
    response.then((data)=>{
        let coursesId = []
        var value =  data["data"]["availableCourses"]
            for (var courses in value){
                var coursesData = value[courses]
                coursesId.push(coursesData["id"])
                console.log(courses,"..",coursesData["name"],"--id",coursesData["id"])
            }
            return coursesId
        
    })
        .then((coursesId)=>{
            var input = raw_input("Enter your id"+"\n")
            courseId = coursesId[input]
            exerciseUrl = BASE_URL+"/"+(courseId)+"/exercises"
            var exerciseResponse = firstApi((exerciseUrl))
            console.log("       "+"*************@ COURSES EXERCISES @************"+"\n")
            return exerciseResponse
    

        }) 
            .then((exerciseResponse)=>{
                // console.log(exerciseResponse)
                        let exercisesId = []
                        let dict1 = {}
                        // let child_slug = []
                        let main_slug = []
                        var exercisName = exerciseResponse["data"]["data"]
                        for(var name in exercisName){
                            let child_slug = []
                            var exercisenameData = exercisName[name]
                            exercisesId.push(exercisenameData["id"])
                            console.log(name,".",exercisenameData["name"],exercisenameData["id"])
                            var childExercise = exercisenameData["childExercises"]
                            for(var childE in childExercise){
                                var childExerciseData = childExercise[childE]
                                child_slug.push(childExerciseData["slug"])
                                console.log("       ",childE,childExerciseData["name"],"id",childExerciseData["id"])
                            }
                            main_slug.push(child_slug)
                           
                            // dict1[exercisesId] = exercisenameData
                        } 
                        dict1["id"] = exercisesId;
                        dict1["mainData"]=exercisName
                        dict1["child_slug"] = main_slug
                        allData =  dict1
                        return allData
               })
               .then((allData)=>{
                   var user_input = raw_input("Enter your exercises id")
                   var data =allData["mainData"];
                   var ids = allData["id"]
                   user_choice = user_input
                   var one_id = (ids[user_input])
                   var one_childExercises = data[user_input]["childExercises"];
                   console.log("   ","-----------USER CHOICE EXERCISES----------")
                   console.log("1. "+data[user_input]["name"]);
                   var slugId = (data[user_input]["slug"])
                   for (var names in one_childExercises){
                       var childExerciseData = one_childExercises[names]
                       console.log("  ",names,childExerciseData["name"])
                
                   }
                   var contentUrl =  BASE_URL+"/"+one_id+"/"+"exercise"+"/"+"getBySlug?slug="+(slugId)
                   var contentResponse = firstApi((contentUrl))
                   
                   

                   return contentResponse
               })
                    .then((contentResponse)=>{
                        var exerciseContent = contentResponse["data"]["content"]
                        console.log(exerciseContent)
                        var slug = allData["child_slug"]
                        var user_slug = slug[user_choice]
                        return user_slug

                    })
                    .then((user_slug)=>{
                        var main_id = allData["id"]
                        var user_child_slug = raw_input("enter your choice child_exercises slug")
                        var single_id = main_id[user_child_slug]
                        var one_slug = user_slug[user_child_slug]
                        var child_content_url =  BASE_URL+"/"+single_id+"/"+"exercise"+"/"+"getBySlug?slug="+(one_slug)
                        var child_contentResponse = firstApi((child_content_url))   
                        return child_contentResponse
            
                    })
                    .then((child_contentResponse)=>{
                                child_exercises_content = child_contentResponse["data"]["content"]
                                console.log(child_exercises_content)
    

                        
                    })
                    .catch((child_contentResponse)=>{
                        console.log("------------Here is no child_exercises-------------------")
                    })
}
coursesIdname(response)





    








