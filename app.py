from flask import Flask, render_template, redirect

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
    return render_template("register-success.html")

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

if __name__ == "__main__":
    app.run(debug=True)