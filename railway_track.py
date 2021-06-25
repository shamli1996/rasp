import RPi.GPIO as GPIO
import sys
import numpy as np
import os, time
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser                  
import serial
import pynmea2
import smtplib
import os.path
import threading
from time import sleep


def GPS_Info():
        global gps
        global map_link
        port="/dev/ttyAMA0"
        

        ser=serial.Serial(port,baudrate=9600,timeout=0.5)

        dataout =pynmea2.NMEAStreamReader()

        newdata=ser.readline()
        print(newdata)

        if newdata[0:6]==b'$GPRMC':
                newmsg=pynmea2.parse(newdata.decode('ASCII'))

                lat=newmsg.latitude

                lng=newmsg.longitude

                lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
                long_in_degrees = convert_to_degrees(lng)

                gps="Latitude=" +str(lat) + "and Longitude=" +str(lng)
                map_link='http://maps.google.com/?q=' + str(lat)+ ',' + str(lng)
                print(map_link)
                print(gps)

def convert_to_degrees(raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position

    
gpgga_info = "$GPGGA,"
#ser = serial.Serial ("/dev/ttyS0")            #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)

def delay(a):
        for i in range (0,a):
                for j in range (0,5000):
                        b=0
                        b=b+1
                
def serial_receive() :
        while True :
                received_data = port.read(10)              #read serial port
                print (received_data)
                if(received_data) :
                        received_data=0
                        break
def serial_Print(text):
        _text=str(text)
        _length=len(_text)
        for i in range (0,_length):
                _a=_text[i].encode()
                port.write(_a)

def gsm():
        global gps
        #port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
        print("SENDING SMS")
        delay(10)
        serial_Print('AT\r\n')
        delay(100)
        #serial_receive()
        serial_Print('AT+CMGF=1\r\n')
        delay(100)
        #serial_receive()
        serial_Print('AT+CMGS=\"08459199189\"\r')
        delay(500)
        serial_Print(" Accident "+map_link)
        delay(500)
        ##port.write(26.encode())
        serial_Print("\x1A")
        #serial_receive()
        #serial_receive()
        print("SMS SEND")
        delay(1000)

while True:
    print("Tracking gps")
    map_link=""
    GPS_Info()
    gsm()







    
