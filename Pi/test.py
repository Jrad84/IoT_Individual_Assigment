from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField, IntegerField, validators
from wtforms.validators import DataRequired, Length
import requests, json
import serial
import os
from pushbullet import Pushbullet
import time
import face_recognition
import sqlite3 as sql
import datetime


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'a-good-password'

# set up push bullet with API key
api_key = "o.TTnGHTsfO2tV7jPh6SaQyWV8UBBCX1PP"
pb = Pushbullet(api_key)

#device to send notifications to
oppo = pb.devices[0]

# Arduino 
deviceA = "/dev/ttyUSB0"
#deviceB = "/dev/ttyUSB1"
# open the serial port to talk over
s1 = serial.Serial(deviceA, 9600)
#s2 = serial.Serial(deviceB, 9600)

# clean the serial port
s1.flushInput()

def faceMatch():
    # list of approved people
    images = os.listdir("./face_recognition/known")
    # image to be checked
    unknown = face_recognition.load_image_file("./face_recognition/unknown/download.jpeg")
    # add image to feature vector
    unknown_encoding = face_recognition.face_encodings(unknown)[0]
    # iterate over each image
    for image in images:
        # load the image
        current_image = face_recognition.load_image_file("./face_recognition/known/" + image)
        # encode the loaded image into a feature vector
        current_image_encoded = face_recognition.face_encodings(current_image)[0]
        # check for match
        result = face_recognition.compare_faces([unknown_encoding],current_image_encoded)
    return result
    

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
    self.threshold = 60
    
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
    cur.execute("INSERT INTO INCIDENTS (distance,date) VALUES (?,?)", (self.distance, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    conn.commit()
    conn.close()
    return self.distance, self.lightStatus, self.threshold

# class for the form to change distance threshold
class DistanceForm(FlaskForm):
  distanceThreshold = DecimalField('Change Threshold', validators=[DataRequired()])
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
  if arduinoLightStatus == True:
      with open("./static/images/download.jpg", "rb") as pic:
          file_data = pb.upload_file(pic, "security_cam.jpg")
          image = faceMatch()
          print(image)
          if (image):
              alert = pb.push_note("Alert!", "Unauthorized person")
              push = pb.push_file(**file_data)
  formDistance = DistanceForm()
  formDistance.distanceThreshold.data = arduinoThreshold
  # return the webpage and pass it all of the information
  return render_template( 'index.html',title=title, arduinoDistance=arduinoDistance, arduinoLightStatus=arduinoLightStatus, arduinoThreshold=arduinoThreshold, formDistance=formDistance)

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
      ard.write( distanceThreshold )
    except:
      pass
      # return the user to the main page
    return redirect('/')

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/image1')
def image1():
    return render_template('image1.html')

@app.route('/list', methods = ['GET', 'POST'])
def list():
  conn = getDBConnection()
  conn.row_factory = sql.Row
  cur = conn.cursor()
  formQuery = QueryForm()
  #formQuery.
  if request.method == 'POST':
      results = request.form['numResults']
      cur.execute("select * from Incidents ORDER BY date DESC LIMIT (?)", (results,))
  rows = cur.fetchall();
  # return the webpage and pass it all of the information
  return render_template( 'list.html', rows=rows, formQuery=formQuery )

# # route used by Flask to show the main page
if __name__ == '__main__':
  #app.run()
  app.run(debug=True)
  app.run(host='0.0.0.0', port=8080)

