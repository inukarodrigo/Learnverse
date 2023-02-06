from flask import Flask, render_template, redirect, jsonify, request
import importlib.machinery
import importlib.util
import os

# Creating a reference to the examPaperGeneration.py file so that functions in that file can be used
current_dir = os.getcwd()
abs_path = "E:\Apps\Python\Pycharm Projects\Learnverse\Exam Paper Generation\Application\examPaperGeneration.py"
rel_path = os.path.relpath(abs_path, current_dir)

loader = importlib.machinery.SourceFileLoader('examPaperGeneration.py', rel_path)
spec = importlib.util.spec_from_loader('examPaperGeneration.py', loader)
examPaperGeneration = importlib.util.module_from_spec(spec)
loader.exec_module(examPaperGeneration)

# Creating a reference to the examPaperGeneration.py file so that functions in that file can be used
loader1 = importlib.machinery.SourceFileLoader('examPaperResults.py',
                                               "E:\Apps\Python\Pycharm Projects\Learnverse\Exam Paper Generation\Application\examPaperResults.py")
spec1 = importlib.util.spec_from_loader('examPaperResults.py', loader1)
examPaperResults = importlib.util.module_from_spec(spec1)
loader1.exec_module(examPaperResults)

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


# Using the functions of other classes and returning the values in JSON format
@app.route('/get_questions_for_paper1', methods=['GET'])
def get_questions_for_paper1():
    abs_path_for_the_db = "E:/Apps/Sqlite/DB Browser/Databases/DataSetDSGP.db"
    rel_path = os.path.relpath(abs_path_for_the_db, current_dir)
    return jsonify(examPaperGeneration.transform_the_questions_for_the_application_paper1(rel_path))


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
    questionsFromTheDB = examPaperResults.get_list_of_Questions_from_the_DB(
        "E:/Apps/Sqlite/DB Browser/Databases/DataSetDSGP.db", listOfIncorrectQuestions)
    # Transforming the questions that can be used to the front end
    transformationOfTheQuestions = examPaperGeneration.transform_the_questions_for_the_application_paper2(
        "E:/Apps/Sqlite/DB Browser/Databases/DataSetDSGP.db", questionsFromTheDB)
    return transformationOfTheQuestions


if __name__ == "__main__":
    app.run(debug=True)
