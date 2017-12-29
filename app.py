from flask import Flask, render_template, request, redirect, url_for, g, session, current_app
import sqlite3
import re
import secrets

def redirect_url():
    return request.args.get('next') or \
           request.referrer

def sessionCheck():
    if session.get("login") == None:
        return redirect("/")

def check(data):
    data = str(data)
    if len(data) < 6:
        return False
    elif re.search(r"[a-z]", data) is None:
        return False
    # elif re.search(r"[A-Z]", data) is None:
    #     return False
    # elif re.search(r"[0-9]", data) is None:
    #     return False
    else:
        return True


app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)

def get_value(conn, sql):
    db = sqlite3.connect(conn)
    cursor = db.cursor()
    cursor.execute(sql)

    return cursor.fetchone()[0]

def getSessionID():
    sessionCheck()
    db = sqlite3.connect("db/users.db")
    csr = db.cursor()
    sql = "SELECT id FROM users WHERE login = '"+ str(session.get("login")) +"'"
    result = get_value("db/users.db",sql)
    return result


@app.route("/", methods=["GET", "POST"])
def home():
    sessionCheck()
    if request.method == "POST":
        form_name = request.form["name"]
        form_passw = request.form["passw"]
        if form_name == "" or len(form_name) < 6 or len(form_passw) < 6 or form_passw == "":
            return render_template("login_witherr.html")
        db = sqlite3.connect("db/users.db")
        csr = db.cursor()
        # print(get_value("select * from users where login='" + form_name + "' and password='" + form_passw + "'"))
        if get_value("db/users.db","select * from users where login='" + form_name + "' and password='" + form_passw + "'") != []:
            session["login"] = str(form_name)
            print("[Log] User " + form_name + " logged in successfully")
        else:
            return redirect(url_for("/"))
        db.commit()
        db.close()
        print("[Log] Logged in user: " + form_name + ", password: " + form_passw)
        return redirect(url_for("hello", name=form_name, passw=form_passw))

    return render_template("login.html")


@app.route("/page", methods=["POST", "GET"])
def user_page():
    if request.args != []:
        login = request.args["login"]
        email = request.args["email"]

@app.route("/edit", methods=["POST", "GET"])
def edit():
    sessionCheck()
    if request.method == "POST":
        new_email = request.form["email"]
        db = sqlite3.connect("db/users.db")
        csr = db.cursor()
        csr.execute("UPDATE users SET email="+ new_email +" WHERE login='"+ session.get("login") +"'")
        db.commit()
        db.close()
        return redirect("/")

    return render_template("edit.html")

@app.route("/home", methods=["POST", "GET"])
def hello():
    sessionCheck()
    name = session.get("login")
    status = get_value("db/users.db", "SELECT status_text FROM users WHERE login = '"+ session.get("login") +"'")
    avatar = get_value("db/users.db", "SELECT avatar FROM users WHERE login = '" + session.get("login") + "'")

    context = {'name': name, 'status': status, 'avatar': avatar}

    return render_template("home.html", context=context)

@app.route("/logout")
def logout():
    user = session.get("login", None)
    if user:
        del session["login"]
    return redirect("/")

@app.route("/add_friend", methods=["GET"])
def add_friend():
    if request.method == "GET":
        friend_id = request.args["id"]
        db = sqlite3.connect("db/users.db")
        csr = db.cursor()
        own_id = get_value("db/users.db","SELECT id FROM users WHERE login = '" + session.get("login") + "'")

        # params = (1 ,int(own_id), int(str(friend_id)),0)
        sql = "INSERT INTO friends (id,user_id,user2_id,block) VALUES (NULL, "+own_id+", "+friend_id+", 0)"
        print(sql)
        csr.execute(sql)
        db.commit()
        print("OWN: "+str(own_id))
        print("FRIEND: "+str(friend_id))
        print("[LOG] ADDED "+str(own_id) + " AND "+str(friend_id)+" TO FRIENDS")
        return redirect("done.html")

@app.route("/group_create", methods=["GET"])
def group_create():
    sessionCheck()

    group_name = request.args["name"]
    users_db = sqlite3.connect("db/users.db")
    groups_db = sqlite3.connect("db/groups.db")
    u_csr = users_db.cursor()
    g_csr = groups_db.cursor()
    owner_id = session.get("login")
    sql = "insert into groups (id, name, owner_id) values (null, '"+ group_name +"', "+ getSessionID() +")"
    return render_template("done.html")

@app.route("/remove_friend", methods=["GET"])
def remove_friend():
    if request.method == "GET":
        unfriend_id = request.args["id"]
        db = sqlite3.connect("db/users.db")
        own_id = str(get_value("db/users/db","SELECT id FROM users WHERE login = '" + session.get("login")+"'"))

        csr = db.cursor()
        csr.execute("DELETE FROM friends WHERE user_id = "+ own_id + " AND user2_id = " + str(unfriend_id))
        db.commit()

        return render_template("done.html")

@app.route("/register", methods=["POST", "GET"])
def registration():
    print("[Log] Someone opened /register")
    if request.method == "POST":
        db = sqlite3.connect("db/users.db")
        csr = db.cursor()
        login = request.form.get("login")
        email = request.form.get("email")
        password = request.form.get("password")
        # Проверка сложности пароля
        if check(password) == False:
            return render_template("registration_page.html")
        # Проверка длинны, наличия логина и почты
        if len(login) < 6 or login == "" or len(email) < 4 or email == "":
            return render_template("registration_page.html")
        csr.execute(
            "INSERT INTO users (id, login, password, email) VALUES (NULL, '" + login + "','" + password + "','" + email + "')")
        print(csr.execute("select * from users where id=1"))
        db.commit()
        db.close()
        print("[Log] Registered login: " + login + ", email: " + email + " with password: " + password)
        return render_template("done.html")

    return render_template("registration_page.html")

@app.route("/test", methods=["GET", "POST"])
def test():
    return render_template("login/done_login.html")

@app.route("/profile", methods=["POST","GET"])
def profile():
    if request.method == "POST":
        if session["login"] != None:
            return render_template("profile.html")
if __name__ == '__main__':
    app.run(debug=True)
