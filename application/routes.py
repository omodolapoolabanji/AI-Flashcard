from application import app
from flask import render_template, Flask, request
from application.forms import uploadForm


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    form = uploadForm()
    if form.validate_on_submit() and request.method == "POST":
        pass
    return render_template("index.html", form=form, index=True)
