from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, HiddenField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class Registration(FlaskForm):
    Username = StringField("Username",validators=[DataRequired()])
    Password = PasswordField("Password", validators=[DataRequired()])
    ConfirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("Password", message="Password does not match")])
    Submit = SubmitField("Sign up")



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')