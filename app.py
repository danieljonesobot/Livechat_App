import random
import os
import secrets
from PIL import Image
from string import ascii_uppercase
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_login import UserMixin, LoginManager, login_user,logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from forms.forms import (Registration, LoginForm, UpdateAccountForm)
from uuid import uuid4
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = str(uuid4())
socketio = SocketIO(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'
db = SQLAlchemy(app)



'''
*********************
    DEPENDENCIES
*********************

- pip install flask-socketio


'''

'''You must add this function.  It is an extension of LoginManager and its associated functions i.e
login_user, current_user, logout_user, login_required '''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')



rooms = {}


def generate_unique_code(length):
    while True:
        code = ""
        for i in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break
    return code



@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        ''' The get() function gets value of the keys " name, code, join & create" from the "form" dictionary.'''
        name = request.form.get("name")
        code = request.form.get("code")
        ''' Here, if the keys do not have a value it returns None.  
        By passing "False" as an argument we set the default value to be False'''
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please Enter a Name", title='Home', code=code, name=name)
        
        if join != False and code is None:
            return render_template("home.html", error="Please a room code", title='Home', code=code, name=name)
        

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members":0, "messages":[]}
        elif code not in rooms:
            return render_template("home.hmtl", error="Room does not exist", title='Home', code=code, name=name)    
    
    
    return render_template("home.html", title='Home')



@app.route("/register", methods=["POST","GET"])
def registration():
    form = Registration()
    userName = form.Username.data
    passWord = form.Password.data
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



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    form_picture.save(picture_path)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



'''Route to display user info'''
@app.route("/profile", methods=['GET', 'POST'])
# @login_required
def profile():
     form = UpdateAccountForm()
     if form.validate_on_submit():
         '''if a picture is uploaded'''
         if form.picture.data:
             picture_file = save_picture(form.picture.data)
             current_user.image_file = picture_file
         current_user.username = form.username.data
         current_user.email = form.email.data
         db.session.commit()
         flash("Account details updated", 'success')
         return redirect(url_for('profile'))
     elif request.method == 'GET':
         form.username.data = current_user.username
         form.email.data = current_user.email
         '''current user image is the default img in the static/profile_pics directory'''
     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
     return render_template('profile.html', title='Profile', image_file=image_file, form=form)






if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, debug=True)