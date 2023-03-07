import sqlite3
import uuid

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

class Classroom:
    def __init__(self, name, unit, code, details, cover):
        self.name = name
        self.unit = unit
        self.code = code
        self.details = details
        self.cover = cover
        self.id = id
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


