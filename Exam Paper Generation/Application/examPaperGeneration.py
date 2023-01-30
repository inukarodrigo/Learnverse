from examPaperResults import examPaperResults
import importlib.machinery
import importlib.util

# Creating an instance of the examPaperResults class
results = examPaperResults()

# Creating a reference to the modelTraining.py file so that functions in that file can be used
loader = importlib.machinery.SourceFileLoader('modelTraining.py',
                                              'E:/Apps/Python/Pycharm Projects/Learnverse/Exam Paper Generation/Model Training/modelTraining.py')
spec = importlib.util.spec_from_loader('modelTraining.py', loader)
modelTraining = importlib.util.module_from_spec(spec)
loader.exec_module(modelTraining)


# modelTraining is the reference to that file, we can use that variable to access specific functions


def countOccurrence(listOfLessons):
    # This will take list as in input and create a dict and iterate over the list
    # Later, check if the element present in the list is available in the dictionary or not.
    # If yes, then increase its value by one; otherwise, introduce a new element in the dictionary and assign 1 to it.
    # Repeat the same process until all the elements in the lists are visited.
    k = {}
    for j in listOfLessons:
        if j in k:
            k[j] += 1
        else:
            k[j] = 1
    return k


def lessons_of_the_incorrect_questions():
    # This functions will output the lessons of the incorrect questions with number of occurrence

    listOfLessons = []
    # Retrieving the questions which student answered incorrectly
    incorrect_questions = results.incorrect_questions()

    # Filtering out the lessons of the questions which student answered incorrectly
    for i in incorrect_questions:
        for key, value in i.items():
            if key == "RelatedLesson":
                listOfLessons.append(value)

    return countOccurrence(listOfLessons)


# Using the trained model for predictions
def use_of_model():
    # This function will use the trained model and do the predictions
    # It will take the lessons and no of occurrence as the input and will predict the no of occurrence as the output
    # no of occurrence = How many questions he got wrong in one lesson
    # no of occurrence future = How many questions he will get wrong in future
    # Output will be in dict format where the key is the lesson name and the value is the no_of_occurrence_future
    # which was predicted by the model

    lessons_with_predicted_no_of_occurrence = lessons_of_the_incorrect_questions()
    for key, value in lessons_with_predicted_no_of_occurrence.items():
        lessons_with_predicted_no_of_occurrence[key] = int(modelTraining.useModel(key, value))

    return lessons_with_predicted_no_of_occurrence

# Testing
print(lessons_of_the_incorrect_questions())
print(use_of_model())
