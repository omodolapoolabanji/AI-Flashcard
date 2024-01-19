from application import app, api
from flask import (
    render_template,
    Flask,
    request,
    redirect,
    url_for,
    json,
    jsonify,
    flash,
    session,
)
from application.forms import uploadForm, LoginForm, RegisterForm
from application.models import User, Flashcards
from flask_restx import Resource
from application import processHandler
from werkzeug.utils import secure_filename
import os


@api.route("/api", "/api/")
# this gets all
class GetAndPost(Resource):
    def get(self):
        pass

    def post(self):
        pass


# this class is intended to get a specific flashcard
@app.route("/api/<idx>")
class GetUpdateDelete(Resource):
    def get(self, idx):
        filename = idx
        suffix = filename.split(".")[-1]
        text = processHandler.Handler.getText(filename, suffix)
        return json.dumps(text)

    def put(self):
        pass

    def delete(self):
        pass


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    form = uploadForm()
    if form.validate_on_submit() and request.method == "POST":
        file = form.file.data
        file.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                secure_filename(file.filename),
            )
        )
        filename = secure_filename(file.filename)
        suffix = filename.split(".")[-1]
        text = processHandler.Handler.getText(
            f"application\\static\\files\\{filename}", suffix
        )
        text = processHandler.Handler.return_flashcards(text)
        # flash(filename)
        return redirect(url_for("flashcards", text=text))

    return render_template("index.html", form=form, index=True)


@app.route("/flashcards", methods=["GET", "POST"])
def flashcards():
    # if request.method == "POST":
    text = request.args.get("text")
    if text:
        text = request.args.get("text")
        return render_template(
            "flashcards.html", flashcards=True, text=text, noFlashcards=False
        )
    else:
        return render_template(
            "flashcards.html",
            flashcards=True,
            text=" You have no flashcards yet!",
            noFlashcards=True,
        )


# return render_template("flashcards.html", flashcards=True, text="")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.check_password(password):
            flash("You have been logged in!", "success")
            session["user_id"] = user.user_id
            session["username"] = user.username
            return redirect(url_for("index"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")

    return render_template("login.html", form=form, title="Login", login=True)


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("username"):
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1

        email = form.email.data
        password = form.password.data
        username = form.username.data

        user = User(user_id=user_id, email=email, username=username)
        user.set_password(password)
        user.save()
        flash("You have been registered!", "success")
        return redirect(url_for("index"))
    return render_template("register.html", form=form, title="Register", register=True)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("index"))
