from flask import Flask, render_template, redirect, request
#from flask_wtf import FlaskForm
#from wtforms import DecimalField, StringField, SubmitField, IntegerField, validators
#from wtforms.validators import DataRequired, Length
import requests, json
import serial
import time
import pymysql
import pymysql.cursors
import sqlite3
import datetime


app = Flask(__name__)
device = "COM7"
#device = "/dev/ttyUSB1"
# open the serial port to talk over
s1 = serial.Serial(device, 9600)
# clean the serial port
s1.flushInput()

class Arduino:
  def __init__(self):
    self.distance = None
    self.lightStatus = None
    self.threshold = 30
    
  def read(self):
    # make sure there is some data to read
    if s1.inWaiting():
      while s1.inWaiting():
          self.distance = s1.readline()
          self.lightStatus = s1.readline()
          self.threshold = s1.readline()
          
    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("INSERT INTO INCIDENTS (distance, date) VALUES (?, ?)", (self.distance, datetime.datetime.now()))
    conn.commit()
    #data = cur.execute("SELECT distance, date FROM INCIDENTS")
    #if (not data):
    #    print("Error")
    #for row in data:
    #    print ("Distance : ", row[0])
    #    print ("Date : ", row[1], "\n")
    #conn.close()
        #print(self.distance, self.lightStatus, self.threshold)
    return self.distance, self.lightStatus, self.threshold

ard = Arduino()
#data = ard.read()
#print(data)


def getDBConnection():
    #conn = sql.connect('database.db')
    conn = sqlite3.connect('test.db')
    conn.execute('CREATE TABLE if not exists INCIDENTS (distance REAL, date TEXT)')
    return conn

# route used by Flask to show the main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  # collect all information to show to user
  title = 'Smart Light Controller'
  arduinoDistance, arduinoLightStatus, arduinoThreshold = ard.read()
  #formTemp.tempTreshold.data = arduinoThreshold
  # return the webpage and pass it all of the information
  return render_template( 'index.html', title=title, arduinoDistance=arduinoDistance, arduinoLightStatus=arduinoLightStatus)

#data = s1.readline()
#print(data)

# # route used by Flask to show the main page
if __name__ == '__main__':
  #app.run()
  app.run(debug=True)
  app.run(host='0.0.0.0', port=8080)

