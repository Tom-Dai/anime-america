from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, SelectMultipleField
import re
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User


class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[Length(min=0, max=100)]
    )
    genres = SelectMultipleField(
        "Genres",
        coerce=int,
        choices=[
            (1, "Action"),
            (2, "Adventure"),
            (3, "Comedy"),
            (4, "Drama"),
            (5, "Sci-Fi"),
            (6, "Mystery"),
            (7, "Fantasy"),
            (8, "Sports"),
            (9, "Romance"),
            (10, "Slice of Life"),
            (11, "Horror"),
            (12, "Thriller"),
            (13, "Martial Arts"),
            (14, "Super Power"),
            (15, "School"),
            (16, "Ecchi"),
        ],
    )
    submit = SubmitField("Search")


class AnimeReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")
#Custom validator for our password
class PasswordValidator(object):
    def __init__(self, message=None):
        if not message:
            message = "Invalid password format"
        self.message = message

    def __call__(self, form, field):
        password = field.data.strip()

        if len(password) < 12:
            raise ValidationError("Password must be at least 12 characters long")

        if password.startswith(" ") or password.endswith(" "):
            raise ValidationError("Password cannot begin or end with a space")

        if re.search(r"[A-Z]", password) is None:
            raise ValidationError("Password must contain at least one uppercase letter")

        if re.search(r"[a-z]", password) is None:
            raise ValidationError("Password must contain at least one lowercase letter")

        if re.search(r"\d", password) is None:
            raise ValidationError("Password must contain at least one digit")

        if re.search(r"[#@$&]", password) is None:
            raise ValidationError("Password must contain at least one special character (#@$&)")

        if re.search(r"(\n|\r|\\|/|\*)", password) is not None:
            raise ValidationError("Password cannot contain carriage return, linefeed, /, \\ or * symbols")

        if re.search(r"(.)\1{2,}", password) is not None:
            raise ValidationError("Password cannot contain more than two consecutive identical characters")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(),PasswordValidator()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")

class AddWatchlistForm(FlaskForm):
    name = StringField(
        "Watchlist Name", validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField("Create Watchlist")


#class UpdateWatchlistForm(FlaskForm):

