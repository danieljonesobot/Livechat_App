from flask import Flask, render_template, request, flash
from flask_login import UserMixin, login_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from forms.forms import (Registration, LoginForm)
from uuid import uuid4
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = str(uuid4())
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)



@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title='Home')



@app.route("/register", methods=["POST","GET"])
def registration():
    form = Registration()
    userName = form.Username.data
    passWord = form.Username.data
    if request.method == "POST" and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(passWord)
        newuser = User(username = userName, password = hashed_password)
        user = db.session.query(User).filter_by(username = userName).first()
        if user is not None:
            return None # to be change to flash error message
        else:
            db.session.add(newuser)
            db.session.commit()
    return render_template("register.html", title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome {user.username}!!', 'success')
        else:
            flash("Login failed. Please check username and password", 'danger')
    return render_template("login.html", title='Login', form=form)




if __name__ == "__main__":
    app.run(debug=True)