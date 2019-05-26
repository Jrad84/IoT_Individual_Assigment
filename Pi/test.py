from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField, IntegerField, validators
from wtforms.validators import DataRequired, Length
import requests, json
import serial
import time
import sqlite3 as sql
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-good-password'

deviceA = "/dev/ttyUSB0"
#deviceB = "/dev/ttyUSB1"
# open the serial port to talk over
s1 = serial.Serial(deviceA, 9600)
#s2 = serial.Serial(deviceB, 9600)

# clean the serial port
s1.flushInput()

def getDBConnection():
    #conn = sql.connect('database.db')
    conn = sql.connect('test.db')
    #conn.execute('DROP TABLE INCIDENTS')
    conn.execute('CREATE TABLE if not exists INCIDENTS (distance REAL, date TEXT)')
    return conn

class Arduino:
  def __init__(self):
    self.distance = None
    self.lightStatus = None
    self.threshold = None
    
  def write(self,value):
      value = str( value )
      s1.write( str( value + '\r' ).encode() )
    
  def read(self):
    # make sure there is some data to read
    #if s1.in_waiting:
    #    while s1.in_waiting:
    result = str( s1.readline() )[2:-5]
              # split into parts, each part having some of the data
              # print( 'serial string: ' + result )
    parts = result.split(', ')
            # for each of the datas
    for part in parts:
            # print( 'part: ' + part )
            # take data name and assign it to its value
        vals = part.split(':')
        #print( 'vals: ' + vals[0] + ' ' + vals[1] )
        if vals[0] == 'distance':
            # print( 'vals is temp' )
            if 'd' not in vals[1]:
                self.distance = float(vals[1])
        elif vals[0] == 'lightStatus':
            # print( 'vals is fanStatus' )
            self.lightStatus = True if int(vals[1]) > 0 else False
        elif vals[0] == 'threshold':
            # print( 'vals is threshold' )
            self.threshold = float(vals[1])
            
    #return self.distance, self.lightStatus, self.threshold
    conn = getDBConnection()
    cur = conn.cursor()
    #if (self.distance < 60.0):
    cur.execute("INSERT INTO INCIDENTS (distance,date) VALUES (?,?)", (self.distance,datetime.datetime.now()))
    conn.commit()
    conn.close()
    return self.distance, self.lightStatus, self.threshold

# class for the form to change distance threshold
class DistanceForm(FlaskForm):
  distanceThreshold = DecimalField('Distance Threshold', validators=[DataRequired()])
  submit = SubmitField('Submit')

class QueryForm(FlaskForm):
    numResults = DecimalField('Number of Incidents', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
ard = Arduino()

# route used by Flask to show the main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  # collect all information to show to user
  title = 'Smart Light Controller'
  arduinoDistance, arduinoLightStatus, arduinoThreshold = ard.read()
  formDistance = DistanceForm()
  formDistance.distanceThreshold.data = arduinoThreshold
  # return the webpage and pass it all of the information
  return render_template( 'index.html',title=title, arduinoDistance=arduinoDistance, arduinoLightStatus=arduinoLightStatus, formDistance=formDistance)

# route used when button to submit temp threshold is clicked, the user never sees this
@app.route('/changeDistanceThreshold', methods=['GET', 'POST'])
def changeDistanceThreshold():
  # make sure this has been accessed from a POST
  # form submited
  if request.method == 'POST':
      # grab data from form
    distanceThreshold = request.form['distanceThreshold']
    try:
      # try and change value
      # probably don't need the try catch for our needs here
      # but goot to make sure value ented into form is an int
      ard.write(distanceThreshold)
    except:
      pass
      # return the user to the main page
    return redirect('/')

@app.route('/list', methods = ['GET', 'POST'])
def list():
  conn = getDBConnection()
  conn.row_factory = sql.Row
  cur = conn.cursor()
  formQuery = QueryForm()
  #formQuery.
  if request.method == 'POST':
      results = request.form['numResults']
      cur.execute("select * from Incidents LIMIT (?)", (results,))
  rows = cur.fetchall();
  # return the webpage and pass it all of the information
  return render_template( 'list.html', rows=rows, formQuery=formQuery )

# # route used by Flask to show the main page
if __name__ == '__main__':
  #app.run()
  app.run(debug=True)
  app.run(host='0.0.0.0', port=8080)

