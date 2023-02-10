import random
import sqlite3
import importlib.machinery
import importlib.util
import os

directory = os.path.dirname(os.path.abspath(__file__))
exam_paper_results_path = os.path.join(directory, 'examPaperResults.py')

exam_paper_results = importlib.machinery.SourceFileLoader('examPaperResults', exam_paper_results_path)
spec = importlib.util.spec_from_loader('examPaperResults', exam_paper_results)
examPaperResults = importlib.util.module_from_spec(spec)
exam_paper_results.exec_module(examPaperResults)


# Creating a reference to the modelTraining.py file so that functions in that file can be used
def referenceToModelTrainingFile(abs_path):
    # abs_path is the absolute path
    # abs_path should be something like
    # 'E:/Apps/Python/Pycharm Projects/Learnverse/Exam Paper Generation/Model Training/modelTraining.py'
    loader = importlib.machinery.SourceFileLoader('modelTraining.py', abs_path)
    spec = importlib.util.spec_from_loader('modelTraining.py', loader)
    modelTraining = importlib.util.module_from_spec(spec)
    loader.exec_module(modelTraining)
    return modelTraining


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


def lessons_of_the_incorrect_questions(incorrectQuestions):
    # This functions will output the lessons of the incorrect questions with number of occurrence

    listOfLessons = []
    # Retrieving the questions which student answered incorrectly
    incorrect_questions = incorrectQuestions

    # Filtering out the lessons of the questions which student answered incorrectly
    for i in incorrect_questions:
        for key, value in i.items():
            if key == "RelatedLesson":
                listOfLessons.append(value)

    return countOccurrence(listOfLessons)


# Using the trained model for predictions
def use_of_model(abs_path_for_the_train_csv_file, abs_path_for_the_modelTrainingPYFile,
                 abs_path_for_the_table_to_use_in_the_model_for_predictionCSVFile, incorrectQuestions):
    # This function will use the trained model and do the predictions
    # It will take the lessons and no of occurrence as the input and will predict the no of occurrence as the output
    # no of occurrence = How many questions he got wrong in one lesson
    # no of occurrence future = How many questions he will get wrong in future
    # Output will be in dict format where the key is the lesson name and the value is the no_of_occurrence_future
    # which was predicted by the model

    modelTraining = referenceToModelTrainingFile(abs_path_for_the_modelTrainingPYFile)
    lessons_with_predicted_no_of_occurrence = lessons_of_the_incorrect_questions(incorrectQuestions)
    for key, value in lessons_with_predicted_no_of_occurrence.items():
        lessons_with_predicted_no_of_occurrence[key] = int(modelTraining.useModel(abs_path_for_the_train_csv_file,
                                                                                  abs_path_for_the_table_to_use_in_the_model_for_predictionCSVFile,
                                                                                  key, value))

    return lessons_with_predicted_no_of_occurrence


def sql_data_to_list_of_dicts_1(path_to_db, select_query, relatedLesson, noOfOccurrence):
    """Returns data from an SQL query as a list of dicts."""
    try:
        con = sqlite3.connect(path_to_db)
        con.row_factory = sqlite3.Row
        things = con.execute(select_query, (relatedLesson, noOfOccurrence,)).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
    except Exception as e:
        print(f"Failed to execute. Query: {select_query}\n with error:\n{e}")
        return []
    finally:
        con.close()


def sql_data_to_list_of_dicts_2(path_to_db, select_query, noOfOccurrence):
    """Returns data from an SQL query as a list of dicts."""
    try:
        con = sqlite3.connect(path_to_db)
        con.row_factory = sqlite3.Row
        things = con.execute(select_query, (noOfOccurrence,)).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
    except Exception as e:
        print(f"Failed to execute. Query: {select_query}\n with error:\n{e}")
        return []
    finally:
        con.close()


def retrieve_questions_based_on_prediction(abs_path_for_the_train_csv_file, abs_path_for_the_modelTrainingPYFile,
                                           abs_path_for_the_table_to_use_in_the_model_for_predictionCSVFile,
                                           pathToTheDB, incorrectQuestions):
    # This function can be used from paper 2 onwards
    # This functions will retrieve n number of questions where n is the predicted count which is given by the model
    # along with answers to be included in the exam paper which student will do next
    # It takes a dictionary which was returned by the use_of_model() function as the input

    listOfQuestionsToMakeThePaper = []
    for lesson, count in use_of_model(abs_path_for_the_train_csv_file, abs_path_for_the_modelTrainingPYFile,
                                      abs_path_for_the_table_to_use_in_the_model_for_predictionCSVFile,
                                      incorrectQuestions).items():
        Query = "Select * from Test where RelatedLesson = (?) Order By RANDOM() LIMIT (?)"

        questions_from_one_lesson = sql_data_to_list_of_dicts_1(pathToTheDB, Query, lesson, count)
        for i in questions_from_one_lesson:
            listOfQuestionsToMakeThePaper.append(i)

    return listOfQuestionsToMakeThePaper


def retrieve_remaining_questions(abs_path_for_the_train_csv_file, abs_path_for_the_modelTrainingPYFile,
                                 abs_path_for_the_table_to_use_in_the_model_for_predictionCSVFile, pathToTheDB,
                                 incorrectQuestions):
    # This function can be used from paper 2 onwards
    # This is used to retrieve the remaining questions for the exam paper after calling
    # retrieve_questions_based_on_prediction() function

    listOfQuestionsToMakeThePaper = retrieve_questions_based_on_prediction(abs_path_for_the_train_csv_file,
                                                                           abs_path_for_the_modelTrainingPYFile,
                                                                           abs_path_for_the_table_to_use_in_the_model_for_predictionCSVFile,
                                                                           pathToTheDB, incorrectQuestions)
    noOfQuestionsNeeded = 50 - len(listOfQuestionsToMakeThePaper)

    Query = "Select * from Test Order By RANDOM() LIMIT (?)"
    remainingQuestions = sql_data_to_list_of_dicts_2(pathToTheDB, Query, noOfQuestionsNeeded)
    for i in remainingQuestions:
        listOfQuestionsToMakeThePaper.append(i)

    return listOfQuestionsToMakeThePaper


def retrieve_50_questions(pathToTheDB):
    # This function is used to make the paper 1

    listOfQuestionsToMakeThePaper = []
    noOfQuestionsNeeded = 50

    Query = "Select * from Test Order By RANDOM() LIMIT (?)"
    listOfQuestions = sql_data_to_list_of_dicts_2(pathToTheDB, Query, noOfQuestionsNeeded)
    for i in listOfQuestions:
        listOfQuestionsToMakeThePaper.append(i)

    return listOfQuestionsToMakeThePaper


def retrieve_50_questions_based_on_requirement(pathToTheDB, listOfLessons):
    # This function is used to make the special paper

    listOfQuestionsToMakeThePaper = []
    listOfQuestions = []
    Query = "Select * from Test where RelatedLesson = (?) Order By RANDOM() LIMIT (?)"
    if len(listOfLessons) == 2:
        noOfQuestionsNeedForEachLesson = 25
        listOfQuestionsFromLessonOne = sql_data_to_list_of_dicts_1(pathToTheDB, Query, listOfLessons[0], noOfQuestionsNeedForEachLesson)
        for i in listOfQuestionsFromLessonOne:
            listOfQuestions.append(i)

        listOfQuestionsFromLessonTwo = sql_data_to_list_of_dicts_1(pathToTheDB, Query, listOfLessons[1], noOfQuestionsNeedForEachLesson)
        for j in listOfQuestionsFromLessonTwo:
            listOfQuestions.append(j)
    else:
        noOfQuestionsNeedForEachLesson = 50
        listOfQuestionsFromTheLesson = sql_data_to_list_of_dicts_1(pathToTheDB, Query, listOfLessons[0], noOfQuestionsNeedForEachLesson)
        for i in listOfQuestionsFromTheLesson:
            listOfQuestions.append(i)

    for i in listOfQuestions:
        listOfQuestionsToMakeThePaper.append(i)

    return listOfQuestionsToMakeThePaper


def transform_the_questions_for_the_application_paper1(pathToTheDB):
    # This function can be used to make the paper 1
    # This function is used to convert the questions in a format which can be used in the application
    listOfQuestions = retrieve_50_questions(pathToTheDB)
    listOfQuestionsInCorrectFormat = []
    for i in listOfQuestions:
        questionInCorrectFormat = {}
        listOfOptions = []
        for key, value in i.items():
            if key == "Question":
                questionInCorrectFormat['q'] = value
            if key != "RelatedLesson" and key != "Question":
                listOfOptions.append(value)

        # Answers with incorrect options were appended to the list
        correctAnswer = listOfOptions[0]

        # Shuffling the elements in the list
        shuffledListOfOptions = random.sample(listOfOptions, len(listOfOptions))

        questionInCorrectFormat['options'] = shuffledListOfOptions
        questionInCorrectFormat['answer'] = shuffledListOfOptions.index(
            correctAnswer)  # listOfQuestions.index(correctAnswer) returns the index

        # Appending the dict to the list
        listOfQuestionsInCorrectFormat.append(questionInCorrectFormat)

    return listOfQuestionsInCorrectFormat


def transform_the_questions_for_the_application_paper2(abs_path_for_the_train_csv_file,
                                                       abs_path_for_the_modelTrainingPYFile,
                                                       abs_path_for_the_table_to_use_in_the_model_for_predictionCSVFile,
                                                       pathToTheDB, incorrectQuestions):
    # This function can be used from exam paper 2 onwards
    # This function is used to convert the questions in a format which can be used in the application

    listOfQuestions = retrieve_remaining_questions(abs_path_for_the_train_csv_file,
                                                   abs_path_for_the_modelTrainingPYFile,
                                                   abs_path_for_the_table_to_use_in_the_model_for_predictionCSVFile,
                                                   pathToTheDB, incorrectQuestions)
    listOfQuestionsInCorrectFormat = []
    for i in listOfQuestions:
        questionInCorrectFormat = {}
        listOfOptions = []
        for key, value in i.items():
            if key == "Question":
                questionInCorrectFormat['q'] = value
            if key != "RelatedLesson" and key != "Question":
                listOfOptions.append(value)

        # Answers with incorrect options were appended to the list
        correctAnswer = listOfOptions[0]

        # Shuffling the elements in the list
        shuffledListOfOptions = random.sample(listOfOptions, len(listOfOptions))

        questionInCorrectFormat['options'] = shuffledListOfOptions
        questionInCorrectFormat['answer'] = shuffledListOfOptions.index(
            correctAnswer) + 1  # listOfQuestions.index(correctAnswer) returns the index

        # Appending the dict to the list
        listOfQuestionsInCorrectFormat.append(questionInCorrectFormat)

    return listOfQuestionsInCorrectFormat

def transform_the_questions_for_the_application_specialPaper(pathToTheDB, listOfLessons):
    # This function can be used to make the special paper
    # This function is used to convert the questions in a format which can be used in the application
    listOfQuestions = retrieve_50_questions_based_on_requirement(pathToTheDB, listOfLessons)
    listOfQuestionsInCorrectFormat = []
    for i in listOfQuestions:
        questionInCorrectFormat = {}
        listOfOptions = []
        for key, value in i.items():
            if key == "Question":
                questionInCorrectFormat['q'] = value
            if key != "RelatedLesson" and key != "Question":
                listOfOptions.append(value)

        # Answers with incorrect options were appended to the list
        correctAnswer = listOfOptions[0]

        # Shuffling the elements in the list
        shuffledListOfOptions = random.sample(listOfOptions, len(listOfOptions))

        questionInCorrectFormat['options'] = shuffledListOfOptions
        questionInCorrectFormat['answer'] = shuffledListOfOptions.index(
            correctAnswer)  # listOfQuestions.index(correctAnswer) returns the index

        # Appending the dict to the list
        listOfQuestionsInCorrectFormat.append(questionInCorrectFormat)

    return listOfQuestionsInCorrectFormat

# Testing
# print(lessons_of_the_incorrect_questions([{"Question": 'Who is considered as the first computer programmer?',"RelatedLesson": 'introduction to computer'},{ "Question": 'Which of the following technologies has been used in the Third Generation Computers?', "RelatedLesson": "concept of it"}]))
# print(use_of_model([{"Question": 'Who is considered as the first computer programmer?',"RelatedLesson": 'introduction to computer'},{ "Question": 'Which of the following technologies has been used in the Third Generation Computers?', "RelatedLesson": "concept of it"}]))
# print(retrieve_questions_based_on_prediction("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db"))
# print(len(retrieve_questions_based_on_prediction("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db")))
# print(retrieve_remaining_questions("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db"))
# print(len(retrieve_remaining_questions("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db")))
# print(sql_data_to_list_of_dicts_1("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db","Select * from Test where RelatedLesson = (?) Order By RANDOM() LIMIT (?)",'introduction to computer',4))
# print(transform_the_questions_for_the_application_paper2("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db"))
# print(transform_the_questions_for_the_application_paper1("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db"))
# print(retrieve_50_questions_based_on_requirement("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db", ["introduction to computer", "concept of it"]))
# print(transform_the_questions_for_the_application_specialPaper("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db", ["introduction to computer", "concept of it"]))