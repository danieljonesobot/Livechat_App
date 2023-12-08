from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, HiddenField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError


class Registration(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords do not match. Please try again.")])
    Submit = SubmitField("Sign up")



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Change profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], message="Accepted file formats are jpg, png & jpeg ONLY")])
    submit = SubmitField('Update')