# Flask Setup
import os
import sqlite3

import self as self
from flask import Flask, jsonify, request

app = Flask(__name__)
# Google Sheets API Setup
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class examPaperResults:
    # Accessing the Google sheet we want to modify
    def accessingGoogleSheet(self, jsonFilePath):
        credential = ServiceAccountCredentials.from_json_keyfile_name(jsonFilePath,

                                                                      ["https://spreadsheets.google.com/feeds",
                                                                       "https://www.googleapis.com/auth/spreadsheets",
                                                                       "https://www.googleapis.com/auth/drive.file",
                                                                       "https://www.googleapis.com/auth/drive"])
        client = gspread.authorize(credential)
        return client.open("Sample Paper (Responses)").sheet1

    # Retrieving the data in the sheet
    def retrieveDataFromTheSheet(self):
        gsheet = self.accessingGoogleSheet("credentials.json")
        # This object has all the data stored in the sheet
        dataInTheSheet = gsheet.get_all_records()

        # Removing Timestamp and Score columns
        del dataInTheSheet[0]["Timestamp"]
        del dataInTheSheet[0]["Score"]

        return dataInTheSheet

    # Retrieving all the data from the sheet
    # An example GET Route to get all reviews
    @app.route('/all_reviews/', methods=["GET"])
    def all_reviews(self):
        return jsonify(self.retrieveDataFromTheSheet())

    # Retrieving the questions with answers from the DB
    # This function is to retrieve relevant questions from the DB as a list of dict
    @app.route('/')
    def sql_data_to_list_of_dicts(self, path_to_db, select_query, specific_question):
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

    # This function will retrieve the questions given in the exam paper
    @app.route('/get_list_of_questions_given_in_the_paper/', methods=["GET"])
    def get_list_of_questions_given_in_the_paper(self):
        dataInTheSheet = self.retrieveDataFromTheSheet()
        return dataInTheSheet[0]  # Returns a dictionary

    # This is to retrieve the questions which student answered from the DB
    @app.route('/get_list_of_Questions_from_the_DB/', methods=["GET"])
    def get_list_of_Questions_from_the_DB(self, pathToTheDataBase):
        # Same list of questions given in the paper including the correct answer and the related lesson
        listOfQuestionsInTheDB = []
        for question in self.get_list_of_questions_given_in_the_paper():
            Query = "SELECT Question,CorrectAnswer, RelatedLesson from Test where Question = (?)"
            # Changing the format of the question
            if str(question).find("\n") != -1:
                modifiedQuestion = str(question).replace("\n", "\r\n")
            else:
                modifiedQuestion = str(question)

            questionInTheDB = self.sql_data_to_list_of_dicts(pathToTheDataBase, Query, modifiedQuestion)
            listOfQuestionsInTheDB.append(questionInTheDB[0])

        return listOfQuestionsInTheDB

    # Retrieving the incorrectly answered questions
    @app.route('/incorrect_questions/', methods=["GET"])
    def incorrect_questions(self):
        list_of_incorrect_questions = []
        count = -1
        for key, value in self.get_list_of_questions_given_in_the_paper().items():
            count += 1
            questionInTheDataBase = self.get_list_of_Questions_from_the_DB("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db")[count]
            if value != questionInTheDataBase.get("CorrectAnswer"):
                list_of_incorrect_questions.append(questionInTheDataBase)

        # Removing unnecessary keys from the list_of_incorrect_questions
        for i in list_of_incorrect_questions:
            del i["CorrectAnswer"]
        return list_of_incorrect_questions

    # Updating the data in the sheet (If required)
    # An example PATCH Route to update a review
    @app.route('/update_review/', methods=["PATCH"])
    def update_review(self):
        req = request.get_json()
        gsheet = self.accessingGoogleSheet("credentials.json")
        cells = gsheet.findall(
            req["email"])  # Email means the column name given in the internet, can change it accordingly
        for c in cells:
            gsheet.update_cell(c.row, 3, req["score"])  # Score means the column name which needs to be update
        return jsonify(self.retrieveDataFromTheSheet())

x = examPaperResults()
print(x.get_list_of_questions_given_in_the_paper())
print(x.get_list_of_Questions_from_the_DB("E:\Apps\Sqlite\DB Browser\Databases\DataSetDSGP.db"))
print(x.incorrect_questions())
# Run the app
if __name__ == "__main__":
    with app.test_request_context():
        # Use this link to run the application : http://localhost:80/mathod_name/
        app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))
