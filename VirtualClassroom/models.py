import sqlite3
import string
import uuid
import random

from flask import Flask
from sqlalchemy.testing import db
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['DATABASE'] = 'VirtualClassroom/db.sqlite3'


class User:
    def __init__(self, username, email, password, confirm_password, is_student, is_teacher, is_active, is_superuser,
                 is_staff):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.confirm_password = confirm_password
        self.is_student = is_student
        self.is_teacher = is_teacher
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.is_staff = is_staff
        self.id = id
def get_random_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(7))
    return result_str
class Classroom:

    def __init__(self, name, unit, code, details):
        self.name = name
        self.unit = unit
        self.code = code
        self.details = details
        self.id = id
def init_classroom(Classroom):
    conn = sqlite3.connect(app.config['DATABASE'])
    id = str(uuid.uuid4())
    user= current_user()
    teacher= get_id(user)
    teacher_user_id= teacher[0]
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO classroom_classroom (id, name, unit, code, details, teacher_id) VALUES (?, ?, ?, ?, ?, ?)",
        (id, Classroom.name, Classroom.unit, Classroom.code, Classroom.details, teacher_user_id))
    conn.commit()
    cur.close()
def register_user(user):
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO profiles_user (username, email, password,confirm_password, is_student, is_teacher, is_active, is_superuser, is_staff) VALUES (?, ?, ?, ?, ?, ? , ?, ?, ?)",
        (user.username, user.email, user.password_hash, user.confirm_password, user.is_student, user.is_teacher,
         user.is_active, user.is_superuser, user.is_staff))
    conn.commit()
    cur.close()
def register_teacher(username):
    user=get_user_by_username(username)
    teacher_id=user[0]
    conn = sqlite3.connect(app.config['DATABASE'])
    id = str(uuid.uuid4())
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO profiles_teacher (id, user_id, name) VALUES (?, ?, ?)",
        (id, teacher_id, username))
    conn.commit()
    cur.close()
def Log_active(usernames):
    conn = sqlite3.connect(app.config['DATABASE'])
    u_name = usernames
    cur = conn.cursor()
    cur.execute("UPDATE profiles_user SET is_active = ? WHERE username = ?", (True, u_name))

    conn.commit()
    cur.close()
def Log_deactive():
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("UPDATE profiles_user SET is_active = ? WHERE is_active = ?", (False, True))

    conn.commit()
    cur.close()
def check_code(code,user):
    user_id = user[0]
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles_student WHERE user_id=?", (user_id,))
    st_user=cur.fetchone()
    st_user_id=st_user[0]

    try:

        cur.execute("SELECT * FROM classroom_classroom WHERE code=?", (code,))
        classroom = cur.fetchone()
        room_id = classroom[2]
        cur.execute('SELECT EXISTS(SELECT 1 FROM classroom_membership WHERE room_id =? AND student_id=?)',(room_id,st_user_id))
        result = cur.fetchone()[0]
        if result:
            cur.close()
            return True
        else:
            cur.execute(
                "INSERT INTO classroom_membership (is_join, room_id, student_id) VALUES (?, ?, ?)",
                (True, room_id, st_user_id))
            conn.commit()
    except:
        print("code invalid")
        return False
    cur.close()
    return True
def current_user():
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles_user WHERE is_active=?", (True,))
    user = cur.fetchone()
    cur.close()
    return user
def get_id(user):
    User_= user[0]
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    if user[6]:
        cur.execute("SELECT * FROM profiles_teacher WHERE user_id=?", (User_,))
        teacher = cur.fetchone()
        cur.close()
        return teacher
    else:
        cur.execute("SELECT * FROM profiles_student WHERE user_id=?", (User_,))
        student = cur.fetchone()
        cur.close()
        return student
def register_student(username):
    user=get_user_by_username(username)
    student_id=user[0]
    conn = sqlite3.connect(app.config['DATABASE'])
    id = str(uuid.uuid4())
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO profiles_student (id, user_id, name) VALUES (?, ?, ?)",
        (id, student_id, username))
    conn.commit()
    cur.close()

def get_user_by_username(username):
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles_user WHERE username=?", (username,))
    user = cur.fetchone()
    cur.close()

    return user
def check_type(username):
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles_user WHERE username=?", (username,))
    user = cur.fetchone()
    result=user[5]
    cur.close()
    return result
def create_post(user_id,post,room_id,username):
    id = str(uuid.uuid4())
    conn = sqlite3.connect(app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO classroom_roomstream (id, post, is_featured, room_id, user_id, user_name) VALUES (?, ?, ?, ?, ?, ?)",
        (id, post, False, room_id, user_id, username))
    conn.commit()
    cur.close()
def view_posts(room_id):
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute("SELECT * FROM classroom_roomstream WHERE room_id=?", (room_id,))
    posts = c.fetchall()
    c.close()
    return posts

def db_upload(t_id,r_id, file, file_name):
    id = str(uuid.uuid4())

    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()
    c.execute(
        "INSERT INTO classroom_classfiles (id, class_files, room_id, teacher_id, file_name) VALUES (?, ?, ?, ?, ?)",
        (id, file, r_id, t_id, file_name))
    conn.commit()
    c.close()