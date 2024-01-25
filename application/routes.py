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
        return jsonify(User.objects.all())

    def post(self):
        data = api.payload
        user = User(
            user_id=User.objects.count() + 1,
            email=data["email"],
            username=data["username"],
        )
        user.set_password(data["password"])
        user.save()
        text = processHandler.Handler.return_flashcards(data["text"])
        text = json.loads(text)
        n_text = text["flashcards"]
        index = []
        for key in n_text:
            count = 0
            vals = list(key.values())
            for i in range(len(vals[::2])):
                n_index = {vals[count]: vals[count + 1]}
                index.append(n_index)
                count += 1
        for i in index:
            for key, value in i.items():
                flashcard = Flashcards(
                    flashcard_id=Flashcards.objects.count() + 1,
                    question=key,
                    answer=value,
                    user_id=user.user_id,
                )
                flashcard.save()
        return jsonify(User.objects(user_id=user.user_id))


# this class is intended to get a specific flashcard
@app.route("/api/<idx>")
class GetUpdateDelete(Resource):
    def get(self, idx):
        return jsonify(User.objects(user_id=idx))

    def put(self):
        data = api.payload
        user = User.objects(user_id=data["user_id"]).update(**data)
        return jsonify(User.objects(user_id=data["user_id"]))

    def delete(self):
        User.objects(user_id=api.payload["user_id"]).delete()
        return jsonify("User is deleted!")


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
        result = processHandler.Handler.json_toflashcards(text)

        # flash(filename)
        return redirect(url_for("flashcards", text=text, result=result))

    return render_template("index.html", form=form, index=True)


@app.route("/flashcards", methods=["GET", "POST"])
def flashcards():
    # if request.method == "POST":
    text = request.args.get("text")
    result = request.args.get("result")
    if text:
        """under this line is solely for debugging purposes"""
        text = json.loads(text)
        n_text = text["flashcards"]
        index = []
        for key in n_text:
            count = 0
            vals = list(key.values())
            for i in range(len(vals[::2])):
                n_index = {vals[count]: vals[count + 1]}
                index.append(n_index)
                count += 1

        # flash(index)

        # flash(n_text)

        # flash(result)
        for i in index:
            for key, value in i.items():
                flashcard = Flashcards(
                    flashcard_id=Flashcards.objects.count() + 1,
                    question=key,
                    answer=value,
                    user_id=session["user_id"],
                )
                flashcard.save()

        return render_template(
            "flashcards.html", flashcards=True, index=index, noFlashcards=False
        )
    else:
        if session.get("username"):
            index = Flashcards.objects.filter(user_id=session["user_id"])
            if index:
                return render_template(
                    "flashcards.html",
                    flashcards=True,
                    index=index,
                    noFlashcards=False,
                )
            else:
                return render_template(
                    "flashcards.html",
                    flashcards=True,
                    text=" You have no flashcards yet!",
                    noFlashcards=True,
                )
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


@app.route("/delete/<int:flashcard_id>")
def delete(flashcard_id):
    flashcard = Flashcards.objects(flashcard_id=flashcard_id).first()
    flashcard.delete()
    flash("Flashcard has been deleted!", "success")
    return redirect(url_for("flashcards"))
