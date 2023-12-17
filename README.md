# Project Name: Live Chat Application


## About the Project
This is my final project done at ALX SE Program.  This project was designed with a passion for fostering instant and meaningful conversations and connecting people.  The platform provides a user-friendly and efficient way to engage in real-time conversations.

The Application is developed with flask and socketio. The app allows users to chat with other users in real time. Users can create accounts, upload and update their profile pictures, engage with other users and send messages to other users real time.





## Link to Deployed Application
danieljonesobot.pythonanywhere.com/






## Technologies
I used HTML5, CSS3, JavaScript and bootstrap for the frontend development.  Then I used Python and Flask, SQLAlchemy for the backend, SQLite for the database design during development.  I chose flask because of how easy it is to comprehend its syntax which ultimately impacts speed in development.  I chose SQLite during development because of the ease of connecting the database URI and persisting data to the database.  During deployment the database was changed to MySQL. 


- HTML
- CSS
- Bootstrap
- Javascript
- Python
- Flask
- SQLAlchemy
- Socket.IO
- Mysql





## Connectors for Mysql 
`pip install mysql-connector`

`pip install mysql-connector-python`

`pip install mysql-connector-python-rf`

`pip install pymysql`







## To install all dependencies on this project
`pip install -r requirements.txt`






## How to create and connect local Mysql DB

`import mysql.connector`

`mydb = mysql.connector.connect(host="root", user="yourusername", passwd="yourpassword")`


`my_cursor = mydb.cursor()`

`my_cursor.execute("CREATE DATABASE database_name")`



`my_cursor.execute("SHOW DATABASES")`


''' loop through to see all databases created '''

`for db in my_cursor:`

   `print(db)`

