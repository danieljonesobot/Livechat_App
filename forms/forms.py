from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email

class Registration(FlaskForm):
    Username = StringField("Username",validators=[DataRequired()])
    Password = PasswordField("Password", validators=[DataRequired()])
    ConfirmPassword = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("Password", message="Password does not match")])
    Submit = SubmitField("Register")



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')