from flask import Flask, render_template, redirect, jsonify, request
import importlib.machinery
import importlib.util
import os
import json

# Creating a reference to the examPaperGeneration.py file so that functions in that file can be used
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path_for_the_examPaperGenerationFile = os.path.join(current_dir, 'Exam Paper Generation', 'Application',
                                                         'examPaperGeneration.py')
abs_path = os.path.abspath(file_path_for_the_examPaperGenerationFile)

loader = importlib.machinery.SourceFileLoader('examPaperGeneration.py', abs_path)
spec = importlib.util.spec_from_loader('examPaperGeneration.py', loader)
examPaperGeneration = importlib.util.module_from_spec(spec)
loader.exec_module(examPaperGeneration)

# Creating a reference to the examPaperGeneration.py file so that functions in that file can be used
file_path_for_the_examPaperResultsFile = os.path.join(current_dir, 'Exam Paper Generation', 'Application',
                                                      'examPaperResults.py')
abs_path1 = os.path.abspath(file_path_for_the_examPaperResultsFile)
loader1 = importlib.machinery.SourceFileLoader('examPaperResults.py', abs_path1)
spec1 = importlib.util.spec_from_loader('examPaperResults.py', loader1)
examPaperResults = importlib.util.module_from_spec(spec1)
loader1.exec_module(examPaperResults)

# Creating a reference to the modelTraining.py file
file_path_for_the_modelTrainingFile = os.path.join(current_dir, 'Exam Paper Generation', 'Model Training',
                                                   'modelTraining.py')
abs_path_for_the_modelTrainingFile = os.path.abspath(file_path_for_the_modelTrainingFile)

# Creating a reference to the abs_path_for_the_table_to_use_in_the_model_for_prediction.csv file
file_path_for_the_csvFile = os.path.join(current_dir, 'Exam Paper Generation', 'Model Training',
                                         'table_to_use_in_the_model_for_prediction.csv')
abs_path_for_the_csv_file = os.path.abspath(file_path_for_the_csvFile)

# Creating a reference to the DataSetDSGP.db file
file_path_for_the_DBFile = os.path.join(current_dir, 'Exam Paper Generation', 'Model Training', 'DataSetDSGP.db')
abs_path_for_the_db_file = os.path.abspath(file_path_for_the_DBFile)

# Creating a reference to the table_to_train_the_model.csv file
file_path_for_the_csvFile2 = os.path.join(current_dir, 'Exam Paper Generation', 'Model Training',
                                          'table_to_train_the_model.csv')
abs_path_for_the_csv_file2 = os.path.abspath(file_path_for_the_csvFile2)

app = Flask(__name__)


# @app.route("/")
# def home():
#     return render_template("index.html")
@app.route("/")
def redirect_to_landing():
    return render_template("landing.html")


@app.route("/examPapers")
def exam_papers():
    return render_template("examPapers.html")


# @app.route("/landing")
# def landing():
#     return render_template("landing.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/redirect_to_login')
def redirect_to_login():
    return redirect('/login')


@app.route("/login-error")
def login_error():
    return render_template("login-error.html")


@app.route("/logout")
def logout():
    return render_template("logout.html")


@app.route("/navigationError")
def navigation_error():
    return render_template("navigationError.html")


@app.route("/paper1")
def paper1():
    return render_template("paper1.html")


@app.route("/paper2")
def paper2():
    return render_template("paper2.html")


@app.route("/paper3")
def paper3():
    return render_template("paper3.html")


@app.route("/paper4")
def paper4():
    return render_template("paper4.html")


@app.route("/paper5")
def paper5():
    return render_template("paper5.html")


@app.route("/paper6")
def paper6():
    return render_template("paper6.html")


@app.route("/paper7")
def paper7():
    return render_template("paper7.html")


@app.route("/paper8")
def paper8():
    return render_template("paper8.html")


@app.route("/paper9")
def paper9():
    return render_template("paper9.html")


@app.route("/paper10")
def paper10():
    return render_template("paper10.html")


@app.route("/paper11")
def paper11():
    return render_template("paper11.html")


@app.route("/profilecard")
def profile_card():
    return render_template("profilecard.html")


@app.route("/register-error1")
def register_error1():
    return render_template("register-error1.html")


@app.route("/register-error2")
def register_error2():
    return render_template("register-error2.html")


@app.route("/register-success")
def register_success():
    # return render_template("register-success.html")
    return redirect('/login')


@app.route("/selection")
def selection():
    return render_template("selection.html")


@app.route("/specialPaper")
def special_paper():
    return render_template("specialPaper.html")


@app.route("/viewTestReport")
def view_test_report():
    return render_template("viewTestReport.html")


@app.route("/virtualClassRoom")
def virtualClassRoom():
    return render_template("VirtualClassRoom.html")


@app.route("/spBot", methods=['GET'])
def specialPaperBot():
    return render_template("spBot.html")


@app.route("/botpage")
def botpage():
    return render_template("botpage.html")


# Using the functions of other classes and returning the values in JSON format
@app.route('/get_questions_for_paper1', methods=['GET'])
def get_questions_for_paper1():
    return jsonify(examPaperGeneration.transform_the_questions_for_the_application_paper1(abs_path_for_the_db_file))

@app.route('/get_questions_for_specialPaper', methods=['GET'])
def get_questions_for_specialPaper():
    listOfLessons = request.args.get('listOfLessons').split(',')
    result = jsonify(
        examPaperGeneration.transform_the_questions_for_the_application_specialPaper(abs_path_for_the_db_file,
                                                                                     listOfLessons))
    return result

# This is to retrieve the incorrect questions that was answered by the student and pass it to the
# get_questions_for_the_paper(listOfIncorrectQuestions) to get the questions to be displayed in the next paper
@app.route('/retrieve_incorrect_questions', methods=['POST'])
def retrieve_incorrect_questions():
    listOfQuestionsWhichIsAnsweredIncorrectly = request.get_json()['listOfQuestionsWhichIsAnsweredIncorrectly']
    source = request.get_json()['source']
    listOfQuestions = get_questions_for_the_paper(listOfQuestionsWhichIsAnsweredIncorrectly)
    return jsonify({"listOfQuestions": listOfQuestions})


def get_questions_for_the_paper(listOfIncorrectQuestions):
    # This will take the questions which are answered incorrectly from the DB
    questionsFromTheDB = examPaperResults.get_list_of_Questions_from_the_DB(abs_path_for_the_db_file,
                                                                            listOfIncorrectQuestions)
    # Transforming the questions that can be used to the front end
    transformationOfTheQuestions = examPaperGeneration.transform_the_questions_for_the_application_paper2(
        abs_path_for_the_csv_file2, abs_path_for_the_modelTrainingFile, abs_path_for_the_csv_file,
        abs_path_for_the_db_file, questionsFromTheDB)
    return transformationOfTheQuestions


if __name__ == "__main__":
    app.run(debug=True)
