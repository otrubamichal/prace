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

# from werkzeug.security import generate_password_hash, check_password_hash

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





@app.route("/admin/", methods=["GET"])
def admin():
    if 'user' not in session:
        flash("Tato stánka je pouze pro příhlášené!")
        return redirect(url_for("login", url=request.path))
    
    a = request.args.get("a", 0)
    b = request.args.get("b", 0)
    try:
        c = int(a) + int(b)
    except ValueError:
        c = "Error"
    return render_template("admin.html", a=a, b=b, c=c)


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
    if jmeno and heslo == "fixa":
        session["user"] = jmeno
        flash("Jsi přihlášen!", "success")
        if url:
            return redirect(url)
        else:
            return redirect(url_for("root"))
    else:
        flash("Nesprávné přihlašovací údaje!", "error")
    return redirect(url_for("login", url=url))


@app.route("/logout/")
def logout():
    session.pop("user", None)
    flash("Byl jsi odhlášen!", "success")
    return redirect(url_for("root"))
