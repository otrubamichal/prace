from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    Markup,
    escape,
    flash,
)
import functools
from sqlitewrap import SQLite
from sqlite3 import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"
app.secret_key = b"x6\x87j@\xd3\x88\x0e8\xe8pM\x13\r\xafa\x8b\xdbp\x8a\x1f\xd41\xb8"


slova = ("Super", "Perfekt", "Úža", "Flask")


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def root():
    a = 3
    b = 8
    # a = 1 + '1'
    return render_template("base.html")


@app.route("/info/")
def info():
    retezec = Markup("<strong>neco</strong>")
    return render_template("info.html", slova=slova, retezec=retezec)







@app.route("/Fortnite/")
def Fortnite():
    return render_template("Fortnite.html",)










@app.route("/COD/")
def Cod():
    return render_template("COD.html",)











@app.route("/vzkazy/", methods=["GET"])
def vzkazy():
    if 'user' not in session:
        flash("Tato stánka je pouze pro příhlášené!")
        return redirect(url_for("login", url=request.path))
    
    with SQLite("data.sqlite") as cursor:
        response = cursor.execute(
            "SELECT login, body, datetime, message.id FROM user JOIN message "
            "  ON user.id = message.user_id "
            "  ORDER BY datetime DESC"
        )
        response= response.fetchall()[:]
        print(response)
    
    return render_template("vzkazy.html", response =response, d=datetime.datetime)

@app.route("/vzkazy/", methods=["POST"])
def vzkazy_post():
    if "user" not in session:
        flash("Tato stánka je pouze pro příhlášené!")
        return redirect(url_for("login", url=request.path))

    with SQLite("data.sqlite") as cursor:
        response = cursor.execute(
            "SELECT id FROM user WHERE login=?", [session["user"]]
        )
        response = response.fetchone()
        user_id = list(response)[0]

    vzkaz = request.form.get("vzkaz")
    if vzkaz:
        with SQLite("data.sqlite") as cursor:
            cursor.execute(
                "INSERT INTO message (user_id, body, datetime,) VALUES (?,?,?)",
                [user_id, vzkaz, datetime.datetime.now()],
            )
    return redirect(url_for("vzkazy"))












@app.route("/admin/", methods=["POST"])
def spenat_post():
    # pokus = request.form['pokus']
    pokus = request.form.get("pokus", "")
    print(pokus)
    return redirect(url_for("spenat"))  # spenat je jmeno Funkce!!!


@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/login/", methods=["POST"])
def login_post():
    jmeno = request.form.get("jmeno", "")
    heslo = request.form.get("heslo", "")
    url = request.args.get("url", "")  # url je obsažená v adrese. proto request.args

    with SQLite('data.sqlite') as cursor:
        response = cursor.execute(
            f"SELECT login, password FROM user WHERE login = ?", [jmeno,] )
        response = response.fetchone()

        


        if response:
            login,password =list(response)
            if check_password_hash(password,heslo):
                session["user"] = jmeno
                flash("Jsi přihlášen!", "success")

                if url:
                    return redirect(url)
                else:
                    return redirect(url_for("root"))
            else:flash("Nesprávné přihlašovací údaje!", "error")
        else:
            flash("Nesprávné přihlašovací údaje!", "error")
        return redirect(url_for("login", url=url))


@app.route("/logout/")
def logout():
    session.pop("user", None)
    flash("Byl jsi odhlášen!", "success")
    return redirect(url_for("root"))


@app.route("/registration/", methods=["GET"])
def registration():
    return render_template("registration.html")

@app.route("/registration/", methods=["POST"])
def registration_post():
    jmeno = request.form.get("jmeno", "")
    heslo1 = request.form.get("heslo1", "")
    heslo2 = request.form.get("heslo2", "")
    if len(jmeno) <5:
        flash("Jméno musí mít alespoň 5 znaků", "error")
        return redirect(url_for("registration"))
    if len(heslo1) <5:
        flash("Heslo musí mít alespoň 5 znaků", "error")
        return redirect(url_for("registration"))
    if heslo1 != heslo2:
        flash("Musíte zadat dvakrát stejné heslo!", "error")
        return redirect(url_for("registration"))
    
    hash_ = generate_password_hash(heslo1)
    try:
        with SQLite("data.sqlite") as cursor:
            cursor.execute('INSERT INTO user (login,password) VALUES (?,?)', [jmeno, hash_ ])
        flash(f"Uživatel `{jmeno}` byl přidán!", "success")
    except IntegrityError:
        flash(f"Uživatel `{jmeno}` již existuje!", "error")
    return redirect(url_for("registration"))
