from flask import Flask, render_template, redirect, request
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Text, Separator
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField, IntegerField, validators
from wtforms.validators import DataRequired, Length
import requests, json
import serial
import time
import pymysql
import pymysql.cursors




# open the serial port to talk over
# s1 = serial.Serial('COM6', 9600)
# # clean the serial port
# s1.flushInput()

# create the Flask instance
app = Flask(__name__)
nav = Nav(app)

nav.register_element('navbar', Navbar(
    'nav', 
    View('Home', 'index'), 
    View('Incidents', 'list')
    ))
# set a key used for the form
app.config['SECRET_KEY'] = 'a-good-password'

# Get time stamp
def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])

# # 

# Connect to the database
# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              db='iotassignment',
#                              port=3306)

# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "CREATE TABLE IF NOT EXISTS `TRIGGERS`(`id` int(4) NOT NULL AUTO_INCREMENT, `distance` float(4) NOT NULL,`time` datetime NOT NULL, PRIMARY KEY (`id`)) AUTO_INCREMENT=1"
#         #sql = "INSERT INTO `TRIGGERS` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql)

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()

# finally:
#     connection.close()

# this class us used to interface with the Arduino
class Arduino:
  def __init__(self):
    self.distance = 0
    self.lightStatus = 'Off'
    self.threshold = 30

  # def write(self,value):
  #   value = str( value )
  #   s1.write( str( value + '\r' ).encode() )

  # def read(self):
  #   # make sure there is some data to read
  #   if s1.inWaiting():
  #     # there could be more then one message in the queue
  #     # not sure if this is how it works
  #     # but get most reacent message (i think, test!)
  #     while s1.inWaiting():
  #       # read the last message
  #       result = str( s1.readline() )[2:-5]
  #       # split into parts, each part having some of the data
  #       # print( 'serial string: ' + result )
  #       parts = result.split(', ')
  #       # for each of the datas
  #       for part in parts:
  #         # print( 'part: ' + part )
  #         # take data name and assign it to its value
  #         vals = part.split(':')
  #         # print( 'vals: ' + vals[0] + ' ' + vals[1] )
  #         if vals[0] == 'distance':
  #           # print( 'vals is temp' )
  #           self.temp = float(vals[1])
  #         elif vals[0] == 'lightStatus':
  #           # print( 'vals is fanStatus' )
  #           self.fanStatus = True if int(vals[1]) > 0 else False
  #         elif vals[0] == 'threshold':
  #           # print( 'vals is threshold' )
  #           self.threshold = float(vals[1])
  #       print( 'local memory: ' + 'temp: ' + str( self.temp ) + ', fanStatus: ' + str( self.fanStatus ) + ', threshold: ' + str( self.threshold ))

  #   return self.distance, self.lightStatus, self.threshold

# instace of Arduino class
ard = Arduino()


# # class for the form to change temp threshold
# class DistanceForm(FlaskForm):
#   distanceTreshold = DecimalField('Distance Threshold', validators=[DataRequired()])
#   submit = SubmitField('Submit')

def getDBConnection():
    #conn = sql.connect('database.db')
    conn = sqlite3.connect('test.db')
    conn.execute('CREATE TABLE if not exists INCIDENTS (distance REAL, date TEXT)')
    return conn


# # route used by Flask to show the main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  # collect all information to show to user
  title = 'Fan Controller'
  #arduinoDistance, arduinoLightStatus, arduinoThreshold = ard.read()
  # return the webpage and pass it all of the information
  return render_template( 'index.html', title=title) #,arduinoDistance=arduinoDistance, arduinoLightStatus=arduinoLightStatus)

@app.route('/list')
def list():
  conn = getDBConnection()
  conn.row_factory = sql.Row
  cur = conn.cursor()
  cur.execute("select * from Incidents")
  rows = cur.fetchall();
  # return the webpage and pass it all of the information
  return render_template( 'list.html', rows=rows )


# # route used when button to submit temp threshold is clicked, the user never sees this
# @app.route('/changeTempThreshold', methods=['GET', 'POST'])
# def changeDistanceThreshold():
#   # make sure this has been accessed from a POST
#   # form submited
#   if request.method == 'POST':
#       # grab data from form
#     distanceTreshold = request.form['distanceTreshold']
#     try:
#       # try and change value
#       # probably don't need the try catch for our needs here
#       # but goot to make sure value ented into form is an int
#       ard.write( distanceTreshold )
#     except:
#       pass
#   # return the user to the main page
#   return redirect('/')

# # route used when button to submit city is clicked, the user never sees this
# @app.route('/changeCity', methods=['GET', 'POST'])
# def changeCity():
#   # make sure this has been accessed from a POST
#   # form submited
#   if request.method == 'POST':
#     # grab data from form
#     city = request.form['city']
#     try:
#       # try and change value
#       # probably don't need the try catch for our needs here
#       ard.city = str( city )
#     except:
#       pass
#   # return the user to the main page
#   return redirect('/')

# run the app
# this if chechs to make sure this is the python file is the one that is being run
# this is one way to do testing
if __name__ == '__main__':
  #app.run()
  app.run(debug=True)
  app.run(host='0.0.0.0')
