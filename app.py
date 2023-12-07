import random
import os
import secrets
from PIL import Image
from string import ascii_uppercase
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
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
            DEPENDENCIES
******************************************
pip install flask-socketio
pip install flask
pip install Pillow
pip install flask-SQLAlchemy
pip install flask-bcrypt
pip install flask-login

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





@app.route("/")
@app.route("/landing")
def landing():
    return render_template("landing.html")



@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/home", methods=['GET', 'POST'])
def home():
    '''session.clear() function automatically clears the session when user goes to the home route'''
    # session.clear()
    if request.method == "POST":
        ''' The get() function gets value of the keys " name, code, join & create" from the 
        form(which is a dictionary) in the home.html template.'''
        name = request.form.get("name")
        code = request.form.get("code")
        ''' Here, if the keys do not have a value it returns None as it default value.  
        By passing "False" as an argument we set the default value to be False instead'''
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please Enter a Name", title='Home', code=code, name=name)
        
        if join != False and code is None:
            return render_template("home.html", error="Please enter a room code", title='Home', code=code, name=name)
        

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members":0, "messages":[]}
        elif code not in rooms:
            return render_template("home.hmtl", error="Room does not exist", title='Home', code=code, name=name)    

        '''else if values are provided for room and name, create and store sessions and redirect to room route'''
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))
    
    return render_template("home.html", title='Home')



@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))
    return render_template("room.html")



@socketio.on("connect")
def connect(auth):
    '''we get the room and name sessions and store them in '''
    room = session.get("room")
    name = session.get("name")
    '''checks that a user can't connect to the socket without going through the home route'''
    if not room or not name:
        return
    
    '''if the user's room does not exist in "rooms", then we use the built-in leave_room() 
    function in socket to exit the user and return'''
    if room not in rooms:
        leave_room(room)
        return
    

    '''else, if the user's room exist, we use the join_room() function in socket to admit the user to the 
    room and also send a general message in the room that the user has joined using the built-in send()
    function in socket and increase the number of members in the room by 1'''
    
    join_room(room)
    send({"name":name, "message":"has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")





'''socket for user to leave room'''
@socketio.on("disconnect")
def disconnect(auth):
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -=1
        if rooms[room]["members"] <= 0:
            del rooms[room]


    send({"name":name, "message":"has left the room"}, to=room)
    print(f"{name} has left the room {room}")









@app.route("/register", methods=["POST","GET"])
def registration():    
    form = Registration()
    if form.validate_on_submit():
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        check_user = db.session.query(User).filter_by(username=form.username.data).first()

        if check_user:
            flash("Username already exists. Please try again", 'warning')
            return redirect(url_for('registration'))
        else:
            db.session.add(user)
            db.session.commit()

            flash('Account created Successfully! Please Proceed to log in', 'success')
            return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome {user.username}! 😀', 'success')
            return redirect(url_for("home"))
        else:
            flash("Login failed. Please check username and password", 'danger')
    return render_template("login.html", title='Login', form=form)





@app.route("/logout")
def logout():
    logout_user()
    flash("You have been Logged out 😔", "success")
    return redirect(url_for("landing"))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    form_picture.save(picture_path)

    '''resizes image to smaller size of 300 by 300 pixels'''
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



'''Route to display user info'''
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
         '''if a value is provided / a picture is uploaded'''
         if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
         current_user.username = form.username.data
        #  current_user.email = form.email.data
         db.session.commit()
         flash("Your account information has been updated", 'success')
         return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)






if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    # app.run(debug=True)
    socketio.run(app, debug=True)