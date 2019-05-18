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



device = "/dev/ttyUSB0"
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
      # there could be more then one message in the queue
      # not sure if this is how it works
      # but get most reacent message (i think, test!)
      while s1.inWaiting():
        # read the last message
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
          if vals[0] == 'temp':
            # print( 'vals is temp' )
            if 't' not in vals[1]:
              self.temp = float(vals[1])
          elif vals[0] == 'fanStatus':
            # print( 'vals is fanStatus' )
            self.fanStatus = True if int(vals[1]) > 0 else False
          elif vals[0] == 'threshold':
            # print( 'vals is threshold' )
            self.threshold = float(vals[1])
        # print( 'local memory: ' + 'temp: ' + str( self.temp ) + ', fanStatus: ' + str( self.fanStatus ) + ', threshold: ' + str( self.threshold ) )

    conn = getDBConnection()
    cur = conn.cursor()
    cur.execute("INSERT INTO INCIDENTS (distance, date) VALUES (?, ?)", (self.distance, datetime.datetime.now()))
    conn.commit()
    return self.distance, self.lightStatus, self.threshold

ard = Arduino()

conn = sqlite3.connect('test.db')
def getDBConnection():
    conn = sql.connect('database.db')
    conn.execute('CREATE TABLE if not exists INCIDENTS (distance REAL, date TEXT)')
    return conn

# route used by Flask to show the main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
  # collect all information to show to user
  title = 'Smart Light Controller'
  arduinoDistance, arduinoLightStatus, arduinoThreshold = ard.read()
  formTemp.tempTreshold.data = arduinoThreshold
  # return the webpage and pass it all of the information
return render_template( 'index.html', title=title, arduinoDistance=arduinoDistance, arduinoLightStatus=arduinoLightStatus

data = s1.readline()
print(data)

# # 





# # class for the form to change the city
# class CityForm(FlaskForm):
#   city = StringField('R O O M', validators=[DataRequired()])
#   submit = SubmitField('Submit')

# # class for the form to change temp threshold


# # covert the temp received from API from kelvin to celsius
# def k2c(k):
#   return k - 273.15

# # get temp from web API
# def getTemp(city):
#   api_key = '9fa3fb4430697b4e1df38a932096bdaa'
#   base_url = 'http://api.openweathermap.org/data/2.5/weather?'
#   complete_url = base_url + 'appid=' + api_key + '&q=' + city

#   response = requests.get(complete_url)
#   x = response.json()

#   if x['cod'] != '404':
#     y = x['main']
#     current_temperature = y['temp']
#     return k2c(current_temperature)
#   else:
#     return 'Price Not Found'


# # route used by Flask to show the main page
