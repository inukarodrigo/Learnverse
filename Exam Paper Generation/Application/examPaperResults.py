import os
import sqlite3


# Retrieving the questions with answers from the DB
# This function is to retrieve relevant questions from the DB as a list of dict
def sql_data_to_list_of_dicts(path_to_db, select_query, specific_question):
    """Returns data from an SQL query as a list of dicts."""
    try:
        con = sqlite3.connect(path_to_db)
        con.row_factory = sqlite3.Row
        things = con.execute(select_query, (specific_question,)).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
    except Exception as e:
        print(f"Failed to execute. Query: {select_query}\n with error:\n{e}")
        return []
    finally:
        con.close()


# This is to retrieve the questions which student answered incorrectly from the DB
def get_list_of_Questions_from_the_DB(pathToTheDataBase, listOfIncorrectlyAnsweredQuestions):
    # Same list of questions given in the paper including the correct answer and the related lesson
    listOfQuestionsInTheDB = []
    for question in listOfIncorrectlyAnsweredQuestions:
        Query = "SELECT Question,CorrectAnswer, RelatedLesson from Test where Question = (?)"
        # Changing the format of the question
        # No need to do that
        # if str(question).find("\n") != -1:
        #     modifiedQuestion = str(question).replace("\n", "\r\n")
        # else:
        #     modifiedQuestion = str(question)
        questionInTheDB = sql_data_to_list_of_dicts(pathToTheDataBase, Query, question)
        listOfQuestionsInTheDB.append(questionInTheDB[0])

    # Removing unnecessary keys from the list_of_incorrect_questions
    for i in listOfQuestionsInTheDB:
        del i["CorrectAnswer"]
    return listOfQuestionsInTheDB

# Testing
# print(sql_data_to_list_of_dicts("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db","Select * from Test where RelatedLesson = (?)","concept of it"))
# print(get_list_of_Questions_from_the_DB("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db",['Who is considered as the first computer programmer?', 'Which of the following technologies has been used in the Third Generation Computers?']))
