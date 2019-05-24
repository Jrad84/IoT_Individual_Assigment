from flask import Flask, render_template, redirect, request
#from flask_wtf import FlaskForm
#from flask_nav import Nav
#from flask_nav.elements import Navbar, View, Text, Separator
#from wtforms import DecimalField, StringField, SubmitField, IntegerField, validators
#from wtforms.validators import DataRequired, Length
import requests, json
import serial
import time
#import pymysql
#import pymysql.cursors
import sqlite3 as sql
import datetime


app = Flask(__name__)
device = "/dev/ttyUSB0"
# open the serial port to talk over
s1 = serial.Serial(device, 9600)

# clean the serial port
s1.flushInput()

#nav = Nav(app)

#nav.register_element('navbar', Navbar(
#    'nav',
#    View('Home', 'index'),
#    View('Incidents', 'list')
#    ))
def getDBConnection():
    #conn = sql.connect('database.db')
    conn = sql.connect('test.db')
    conn.execute('CREATE TABLE if not exists INCIDENTS (distance REAL, date TEXT)')
    return conn


class Arduino:
  def __init__(self):
    self.distance = None
    self.lightStatus = None
    self.threshold = 30
    
  def read(self):
    # make sure there is some data to read
    #if s1.inWaiting():
     # while s1.inWaiting():
    #self.distance = s1.readline()
    #self.lightStatus = s1.readline()
    #self.threshold = s1.readline()
    result = str( s1.readline() )[2:-5]
    # split into parts, each part having some of the data
    # print( 'serial string: ' + result )
    parts = result.split(', ')
    # for each of the datas
    for part in parts:
    # print( 'part: ' + part )
        # take data name and assign it to its value
        vals = part.split(':')
        # print( 'vals: ' + vals[0] + ' ' + vals[1] )
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
    return self.distance, self.lightStatus, self.threshold
    conn = getDBConnection()
    cur = conn.cursor()
    if (self.distance < 30):
        cur.execute("INSERT INTO INCIDENTS (distance, date) VALUES (?, ?)", (self.distance, datetime.datetime.now()))
        conn.commit()
    
ard = Arduino()

# route used by Flask to show the main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  # collect all information to show to user
  title = 'Smart Light Controller'
  arduinoDistance, arduinoLightStatus, arduinoThreshold = ard.read()
  #formTemp.tempTreshold.data = arduinoThreshold
  conn = getDBConnection()
  conn.row_factory = sql.Row
  cur = conn.cursor()
  cur.execute("select * from Incidents")
  rows = cur.fetchall();

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
  app.run(debug=True, host='0.0.0.0')


