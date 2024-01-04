from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import DataRequired, ValidationError


class uploadForm(FlaskForm):
    file = FileField(
        "Upload your file here: ",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png", "jpeg", "png"], ["Images and pdf only!"]),
        ],
    )
    submit = SubmitField("Upload")

    def validate_file(self, file):
        if file.data.filename == "":
            raise ValidationError("Please select a file")
