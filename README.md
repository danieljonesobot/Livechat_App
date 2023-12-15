# Project Name: Live Chat Application

## Technologies


- Html
- Css
- Bootstrap
- Javascript
- Python
- Flask
- SQLAlchemy
- Socet.IO
- Mysql


## About the Project
The Application is developed with flask and socketio. The app allows users to chat with other users in real time. Users can create accounts, upload and update their profile pictures, engage with other users and send messages to other users real time.



## How to create and connect local Mysql DB

`#python script to create a DB on local machine
import mysql.connector

mydb = mysql.connector.connect(
host="root",
user="yourusername",
passwd="yourpassword",
)


my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE database_name")

#list all databases present on the console
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)`
