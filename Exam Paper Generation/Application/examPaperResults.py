# Flask Setup
import os
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)
# Google Sheets API Setup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Accessing the Google sheet we want to modify
credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",

                                                              ["https://spreadsheets.google.com/feeds",
                                                               "https://www.googleapis.com/auth/spreadsheets",
                                                               "https://www.googleapis.com/auth/drive.file",
                                                               "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)
gsheet = client.open("Sample Paper (Responses)").sheet1

# This object has all the data stored in the sheet
# Do not use this object without pre-processing
dataInTheSheet = gsheet.get_all_records()


# Removing unnecessary data from the sheet
@app.route('/preProcessing_sheet/', methods=["GET"])
def preProcessing_sheet():
    # Removing Timestamp and Score columns
    del dataInTheSheet[0]["Timestamp"]
    del dataInTheSheet[0]["Score"]


preProcessing_sheet()  # This is used to get clean data


# Retrieving all the data from the sheet
# An example GET Route to get all reviews
@app.route('/all_reviews/', methods=["GET"])
def all_reviews():
    return jsonify(dataInTheSheet)


# Retrieving the questions with answers from the DB
# This function is to retrieve relevant questions from the DB as a list of dict
@app.route('/')
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


listOfQuestionsGivenInThepaper = dataInTheSheet[0]  # Returns a dictionary
listOfQuestionsInTheDB = []  # Same list of questions given in the paper including the correct answer and the related lesson
pathToTheDataBase = "E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db"

# This is to retrieve the questions which student answered from the DB
for question in listOfQuestionsGivenInThepaper:
    Query = "SELECT Question,CorrectAnswer, RelatedLesson from Test where Question = (?)"
    # Changing the format of the question
    if str(question).find("\n") != -1:
        modifiedQuestion = str(question).replace("\n", "\r\n")
    else:
        modifiedQuestion = str(question)

    questionInTheDB = sql_data_to_list_of_dicts(pathToTheDataBase, Query, modifiedQuestion)
    listOfQuestionsInTheDB.append(questionInTheDB[0])

print(listOfQuestionsGivenInThepaper)
print(listOfQuestionsInTheDB)


# Retrieving the incorrectly answered questions
@app.route('/incorrect_questions/', methods=["GET"])
def incorrect_questions():
    list_of_incorrect_questions = []
    count = -1
    for key, value in listOfQuestionsGivenInThepaper.items():
        count += 1
        questionInTheDataBase = listOfQuestionsInTheDB[count]
        if value != questionInTheDataBase.get("CorrectAnswer"):
            list_of_incorrect_questions.append(listOfQuestionsInTheDB[count])

    # Removing unnecessary keys from the list_of_incorrect_questions
    for i in list_of_incorrect_questions:
        del i["CorrectAnswer"]
    return list_of_incorrect_questions


x = incorrect_questions()
print(x)


# Updating the data in the sheet (If required)
# An example PATCH Route to update a review
@app.route('/update_review/', methods=["PATCH"])
def update_review():
    req = request.get_json()
    cells = gsheet.findall(req["email"])  # Email means the column name given in the internet, can change it accordingly
    for c in cells:
        gsheet.update_cell(c.row, 3, req["score"])  # Score means the column name which needs to be update
    return jsonify(dataInTheSheet)


# Run the app
if __name__ == "__main__":
    with app.test_request_context():
        # Use this link to run the application : http://localhost:80/mathod_name/
        app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))
