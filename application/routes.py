from application import app, api
from flask import render_template, Flask, request, redirect, url_for
from application.forms import uploadForm
from flask_restx import Resource


@app.route("/api", "/api/")
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
        pass

    def put(self):
        pass

    def delete(self):
        pass


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
