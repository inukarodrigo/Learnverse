import sys
# from django.template.backends import django
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
    return render_template("index2.html")


@app.route("/spBot", methods=['GET'])
def specialPaperBot():
    return render_template("spBot.html")


@app.route("/generalBot")
def generalBot():
    return render_template("generalBot.html")


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

@app.route('/vc_logout')
def vc_logout():
    models.Log_deactive()
    return render_template('register/login.html')


@app.route('/vc_login', methods=['GET', 'POST'])
def vc_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = models.get_user_by_username(username)
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        if user and check_password_hash(user[10], password):
            models.Log_active(username)
            # user is authenticated
            if models.check_type(username):
                user = models.current_user()
                student = models.get_id(user)
                student_user_id = student[0]
                c.execute("SELECT * FROM classroom_membership WHERE student_id=?", (student_user_id,))
                rows = c.fetchall()
                Student_rooms = []
                for r in rows:
                    room = r[2]
                    c.execute("SELECT * FROM classroom_classroom WHERE id=?", (room,))
                    rooms = c.fetchall()
                    Student_rooms.append(rooms)
                print(Student_rooms)
                c.close()
                return render_template('dashboard/student/student.html', Student_rooms=Student_rooms)
            user = models.current_user()
            teacher = models.get_id(user)
            teacher_user_id = teacher[0]
            c.execute("SELECT * FROM classroom_classroom WHERE teacher_id=?", (teacher_user_id,))
            rows = c.fetchall()
            c.close()
            return render_template('dashboard/teacher/teacher.html', rows=rows)

        else:
            # invalid credentials
            return "Invalid username or password."
    else:
        return render_template('register/login.html')


@app.route('/vc_signup_as_teacher', methods=['GET', 'POST'])
def vc_signup_as_teacher():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        is_teacher = True
        is_student = False
        is_active = False
        is_superuser = False
        is_staff = False
        if password == confirm_password:
            user = models.User(username, email, password, confirm_password, is_student, is_teacher, is_active,
                               is_superuser, is_staff)
            models.register_user(user)
            models.register_teacher(username)
            return render_template('register/login.html')
        else:
            return "Passwords do not match."
    else:
        return render_template('register/signup_teacher.html')


@app.route('/vc_signup_as_student', methods=['GET', 'POST'])
def vc_signup_as_student():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        is_teacher = False
        is_student = True
        is_active = False
        is_superuser = False
        is_staff = False
        if password == confirm_password:
            user = models.User(username, email, password, confirm_password, is_student, is_teacher, is_active,
                               is_superuser, is_staff)
            models.register_user(user)
            models.register_student(username)
            return render_template('register/login.html')
        else:
            flash('Password Incorrect')
            return render_template('register/signup_student.html')
    else:
        return render_template('register/signup_student.html')


@app.route('/stream_post/<r_id> ', methods=['GET', 'POST'])
def stream_post(r_id):
    room_id = r_id
    user = models.current_user()
    user_id = user[0]
    username = user[9]

    if request.method == 'POST':
        post = request.form['post']
        models.create_post(user_id, post, room_id, username)
    posts = models.view_posts(room_id)
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("SELECT * FROM classroom_classroom WHERE id=?", (room_id,))
    row = c.fetchall()
    c.close()
    return render_template('class/single.html', posts=posts,user=user,row=row)


def teachers():
    user = models.current_user()
    teacher = models.get_teacher_id(user)
    teacher_user_id = teacher[0]
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("SELECT * FROM classroom_classroom WHERE teacher_id=?", (teacher_user_id,))
    rows = c.fetchall()
    c.close()
    return render_template('dashboard/teacher/teacher.html', rows=rows)

@app.route('/view_class/<id>')
def view_class(id):
    classroom_id = id
    print(classroom_id)
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("SELECT * FROM classroom_classroom WHERE id=?", (classroom_id,))
    row = c.fetchall()
    c.close()
    user = models.current_user()
    user_id = user[0]
    posts = models.view_posts(classroom_id)

    return render_template('class/single.html', row=row, user=user, posts=posts)


@app.route('/join_class', methods=['GET', 'POST'])
def join_class():
    global room_id
    if request.method == 'POST':
        code = request.form['code']
        user = models.current_user()
        result = models.check_code(code, user)
        if result:
            conn = sqlite3.connect(app.config['DATABASE'])
            cur = conn.cursor()
            cur.execute("SELECT * FROM classroom_classroom WHERE code=?", (code,))
            row = cur.fetchall()
            cur.close()
            for r in row:
                room_id = r[2]
            posts = models.view_posts(room_id)
            return render_template('class/single.html', user=user, row=row, posts=posts)
        else:
            flash("Code is invalid")
    return render_template('dashboard/student/student.html')


@app.route('/create_class', methods=['GET', 'POST'])
def create_class():
    if request.method == 'POST':
        name = request.form['name']
        unit = request.form['unit']
        details = request.form['detail']
        code = models.get_random_string()
        Vclass = models.Classroom(name, unit, code, details)
        models.init_classroom(Vclass)

        user = models.current_user()
        teacher = models.get_id(user)
        teacher_user_id = teacher[0]
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute("SELECT * FROM classroom_classroom WHERE teacher_id=?", (teacher_user_id,))
        rows = c.fetchall()
        return render_template('dashboard/teacher/teacher.html', rows=rows)

    return render_template('class/create_class.html')

@app.route('/detail/<r_id>')
def detail(r_id):
    room_id=r_id
    print(room_id,"this 1")
    user = models.current_user()
    teacher= models.get_id(user)
    teacher_id = teacher[0]
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("SELECT * FROM classroom_classfiles WHERE room_id=?", (room_id,))
    data = c.fetchall()
    c.execute("SELECT * FROM classroom_classroom WHERE id=?", (room_id,))
    row = c.fetchall()
    c.close()
    return render_template('class/detail.html', data=data, room_id=room_id, user=user, row=row)

@app.route('/upload_file/<r_id>', methods=['GET', 'POST'])
def upload_file(r_id):
    file = request.files['file']
    file_name= request.form['data_name']
    user = models.current_user()
    teacher= models.get_id(user)
    teacher_id= teacher[0]
    if file:

        filename = secure_filename(file.filename)
        models.db_upload(teacher_id, r_id, filename, file_name)
        path = os.path.join(directory, filename)
        file.save(path)
        return redirect(url_for('detail', r_id=r_id))
    else:
        return 'No file selected'

@app.route('/download_file/<filename>')
def download_file(filename):
    print(filename)
    path = os.path.join(directory, filename)
    return send_file(path, as_attachment=True)

@app.route('/people/<id>')
def people(id):
    room_id=id
    user = models.current_user()
    teacher = models.get_id(user)
    teacher_id = teacher[0]
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("SELECT * FROM classroom_membership WHERE room_id=?", (room_id,))
    students=c.fetchall()
    names= []
    for s in students:
        s_id= s[3]
        c.execute("SELECT * FROM profiles_student WHERE id=?", (s_id,))
        temp = c.fetchall()
        names.append(temp)
    print(names)
    c.execute("SELECT * FROM classroom_classroom WHERE id=?", (room_id,))
    row = c.fetchall()
    c.close()
    return render_template('class/people.html', room_id=room_id, user=user, row=row, names=names)

    return
@app.route('/predict')
def predict():
    return render_template("prediction.html")


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
