# Importing the required modules
from flask import Flask, url_for, render_template, request
from predict import predictDisease
from response import check_all_messages
from flask_mysqldb import MySQL
import yaml

# Creating the Flask app
app=Flask(__name__)

# Configure db
db= yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST']= db['mysql_host']
app.config['MYSQL_USER']= db['mysql_user']
app.config['MYSQL_PASSWORD']= db['mysql_password']
app.config['MYSQL_DB']= db['mysql_db']


mysql= MySQL(app)


# Creating the route
@app.route('/')

# Function to return the required template
def home():
    return render_template('index.html')

is_name = False
is_age = False
is_contact= False
Name=""
Age=""
ContactNumber=""


#Creating the route to communicate with the user
@app.route('/get')
def reply():
    userText=request.args.get('msg')
    global is_name
    global is_age
    global is_contact
    global Name
    global Age
    global ContactNumber
    if(is_name == False):
        Name=userText
        is_name = True
        return "Could you please mention your age?"
    elif(is_age == False):
        Age=userText
        is_age = True
        return "Please Provide your contact number."
    elif(is_contact == False):
        ContactNumber=userText
        is_contact = True
        # Connecting to MySQL and Inserting user details
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO users(UserName,Age,ContactNumber) VALUES(%s, %s, %s)",(Name,Age,ContactNumber))
        mysql.connection.commit()
        cur.close()
        return "Thank you for providing the details. How may I help you?"
    return str(check_all_messages(userText))


if __name__=='__main__':
    app.run(debug=True)