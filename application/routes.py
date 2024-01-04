from application import app
from flask import render_template, Flask, request, redirect, url_for
from application.forms import uploadForm


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
@app.route("/home")
def index():
    form = uploadForm()
    if form.validate_on_submit() and request.method == "POST":
        pass
    return render_template("index.html", form=form, index=True)


@app.route("/flashcards")
def flashcards():
    return render_template("flashcards.html", flashcards=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", login=True)
