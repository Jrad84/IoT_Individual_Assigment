from flask import Flask, render_template, redirect, request
#from flask_wtf import FlaskForm
#from wtforms import DecimalField, StringField, SubmitField, IntegerField, validators
#from wtforms.validators import DataRequired, Length
import requests, json
import serial
import time
import pymysql
import pymysql.cursors
import sqlite3 as sql
import datetime


app = Flask(__name__)
#device = "COM7"
deviceA = "/dev/ttyUSB0"
deviceB = "/dev/ttyUSB1"
# open the serial port to talk over
s1 = serial.Serial(deviceA, 9600)
s2 = serial.Serial(deviceB, 9600)

# clean the serial port
s1.flushInput()

def getDBConnection():
    #conn = sql.connect('database.db')
    conn = sqlite3.connect('test.db')
    conn.execute('CREATE TABLE if not exists INCIDENTS (distance REAL, date TEXT)')
    return conn

class Arduino:
  def __init__(self):
    self.distance = None
    self.lightStatus = None
    self.threshold = 60.0
    
  def read(self):
    # make sure there is some data to read
    #if s1.inWaiting():
     # while s1.inWaiting():
    self.distance = s1.readline()
    self.lightStatus = s1.readline()
    self.threshold = s1.readline()
    return self.distance, self.lightStatus, self.threshold
    conn = getDBConnection()
    cur = conn.cursor()
    if (self.distance < 60.0):
        cur.execute("INSERT INTO INCIDENTS (distance, date) VALUES (?, ?)", (self.distance, datetime.datetime.now()))
        conn.commit()
    
ard = Arduino()
data = ard.read()
print(data)




# route used by Flask to show the main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  # collect all information to show to user
  title = 'Smart Light Controller'
  arduinoDistance, arduinoLightStatus, arduinoThreshold = ard.read()
  conn = getDBConnection()
  conn.row_factory = sql.Row
  cur = conn.cursor()
  cur.execute("select * from Incidents")
  rows = cur.fetchall();
  #formTemp.tempTreshold.data = arduinoThreshold
  # return the webpage and pass it all of the information
  return render_template( 'index.html', title=title, arduinoDistance=arduinoDistance, arduinoLightStatus=arduinoLightStatus, rows=rows)

@app.route('/list')
def list():
  conn = getDBConnection()
  conn.row_factory = sql.Row
  cur = conn.cursor()
  cur.execute("select * from Incidents")
  rows = cur.fetchall();
  # return the webpage and pass it all of the information
  return render_template( 'list.html', rows=rows )

#data = s1.readline()
#print(data)

# # route used by Flask to show the main page
if __name__ == '__main__':
  #app.run()
  app.run(debug=True)
  app.run(host='0.0.0.0', port=8080)

