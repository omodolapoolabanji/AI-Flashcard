from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, PasswordField, BooleanField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import (
    DataRequired,
    ValidationError,
    EqualTo,
    Email,
    Length,
)


class uploadForm(FlaskForm):
    file = FileField(
        "Upload your file here: ",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png", "jpeg", "png", "pdf"], ["Images and pdf only!"]),
        ],
    )

    submit = SubmitField("Upload")

    def validate_file(self, file):
        if file.data.filename == "":
            raise ValidationError("Please select a file")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password"), Length(min=8)],
    )

    submit = SubmitField("Register")

    def validate_username(self, username):
        pass

    def validate_email(self, email):
        pass
