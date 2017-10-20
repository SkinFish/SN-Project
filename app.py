from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3


app = Flask(__name__)

def get_value(text):
    db = sqlite3.connect("db/users.db")
    csr = db.cursor()
    csr.execute(text)
    result = csr.fetchall()
    return result

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        form_name = request.form["name"]
        form_passw = request.form["passw"]
        # Начало нормальной авторизации
        db = sqlite3.connect("db/users.db")
        csr = db.cursor()
        # print(get_value("select * from users where login='" + form_name + "' and password='" + form_passw + "'"))
        if get_value("select * from users where login='"+form_name+"' and password='"+form_passw+"'") != []:
            print("[Log] User "+form_name+" logged in successfully")
        db.commit()
        db.close()
        print("[Log] Logged in user: " + form_name + ", password: " + form_passw)
        return redirect(url_for("hello", name=form_name, passw=form_passw))

    return render_template("login.html")

@app.route("/page", methods=["POST","GET"])
def user_page():
    if request.args != []:
        login = request.args["login"]
        email = request.args["email"]
@app.route("/hello", methods=["POST", "GET"])
def hello():
    name = request.args["name"]
    passw = request.args["passw"]
    context = {'name': name, 'passw': passw}

    return render_template("hello.html", context=context)

@app.route("/register", methods=["POST","GET"])
def registration():
    print("[Log] Someone opened /register")
    if request.method == "POST":
        db = sqlite3.connect("db/users.db")
        csr = db.cursor()
        login = request.form.get("login")
        email = request.form.get("email")
        password = request.form.get("password")
        csr.execute("INSERT INTO users (id, login, password, email) VALUES (NULL, '"+login+"','"+password+"','"+email+"')")
        print(csr.execute("select * from users where id=1"))
        db.commit()
        db.close()
        print("[Log] Registered login: " + login + ", email: "+ email + " with password: " + password)
        return render_template("done.html")

    return render_template("registration_page.html")

if __name__ == '__main__':
    app.run(debug=True)
