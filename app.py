from flask import Flask, render_template, request, redirect, flash
from datetime import datetime, timedelta
from weather import weather_forecast
from register import register_db
from login import login_account
from dashboard import *
from flask import session
import secrets
from flask import get_flashed_messages

app = Flask(__name__)
app.secret_key = f"{secrets.token_hex(32)}"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    city = None

    if request.method == "POST":
        city = request.form["city"]
        weather_data = weather_forecast(city)
    return render_template("home.html", weather_data=weather_data, city=city)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")
        gender = request.form.get("gender")
        birthdate = request.form.get("birthdate")

        if password != repeat_password:
            flash("Password tidak sama, coba lagi","danger")
        if "@" not in username or "." not in username:
            flash("Username harus berupa email yang valid","danger")
        elif password == repeat_password:
            save_register = register_db(username,password,gender,birthdate)
            if save_register == "Akun sudah terdaftar, silahkan lakukan login":
                flash(save_register,"danger")
            elif save_register == "Success":
                flash("Registrasi berhasil!", "success")
                return redirect("/login")
            
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        login_result = login_account(username,password)
        if login_result == "Username atau password salah":
            flash(login_result,"danger")
        elif login_result == "Username tidak ditemukan, silahkan lakukan pendaftaran akun":
            flash(login_result,"danger")
        elif login_result == "Login berhasil":
            session["username"] = username
            session["password"] = password
            flash(login_result,"success")
            return redirect("/dashboard")            
    return render_template("login.html")

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    _ = get_flashed_messages()
    question = None
    options = None 
    correct_answer = None
    explanation = None
    feedback = None

    username = session.get("username")
    materi = request.form.get("materi")
    user, above, below, rank = get_user_rank_info(username)
    if request.form.get("start_quiz") == "yes":
        quiz = create_quiz(materi)
        question = quiz["question"]
        options = quiz["choices"]
        correct_answer = quiz["correct_answer"]
        explanation = quiz["explanation"]
        session["correct_answer"] = correct_answer
        session["explanation"] = explanation
        session["question"] = question
        session["options"] = options
        session["materi"] = materi

    return render_template("dashboard.html", 
                           username=username, 
                                  score=user[2],
                                  rank=rank,
                                  user_above=above,
                                  user_below=below,
                                  question=question, 
                                  options=options, 
                                  explanation=None)

@app.route("/submit_quiz",methods=["GET","POST"])
def submit_quiz():
    if request.method == "POST":
        correct_answer = session.get("correct_answer")
        answer = request.form.get("answer")
        explanation = session.get("explanation")
        username = session.get("username")
        question = session.get("question")
        options = session.get("options")

        if answer == correct_answer:
            flash("✅ Jawaban benar!", "success")
            new_score = update_score(username,True)
            print("correct",new_score)
        if answer != correct_answer:
            flash("❌ Jawaban salah!", "danger")
            new_score = update_score(username,False)
            print("false",new_score)
        user, above, below, rank = get_user_rank_info(username) 

    return render_template("dashboard.html", 
                            username=username, 
                            score=user[2],
                            rank=rank,
                            user_above=above,
                            user_below=below,
                            question=question, 
                            options=options, 
                            explanation=explanation)
    
@app.route("/next",methods=["GET","POST"])
def next_question():
    username = session.get("username")
    materi = session.get("materi")
    quiz = create_quiz(materi)
    question = quiz["question"]
    options = quiz["choices"]
    correct_answer = quiz["correct_answer"]
    explanation = quiz["explanation"]
    session["correct_answer"] = correct_answer
    session["explanation"] = explanation
    session["question"] = question
    session["options"] = options
    session["materi"] = materi
    user, above, below, rank = get_user_rank_info(username)

    return render_template("dashboard.html", 
                           username=username, 
                                  score=user[2],
                                  rank=rank,
                                  user_above=above,
                                  user_below=below,
                                  question=question, 
                                  options=options, 
                                  explanation=None)

if __name__ == "__main__":
    app.run(debug=True)
