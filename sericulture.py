import RPi.GPIO as IO
import time
import serial
from time import sleep
import Adafruit_DHT
import os
import sys
##import glob
from Adafruit_IO import RequestError, Client, Feed
from gpiozero import LightSensor
IO.setwarnings(False)
IO.setmode(IO.BCM)

ldr = LightSensor(4)
dht=Adafruit_DHT.DHT11
dhtpin=17
led=27
therm=22
fan=23
rs=10
en=9
d4=11
d5=25
d6=8
d7=7
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
ser = serial.Serial(
port='/dev/ttyS0',
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)
ADAFRUIT_IO_KEY = 'aio_vpIM74yS7ezHqn0Ev68jsPM92aEv'
ADAFRUIT_IO_USERNAME = 'heenim96'
aio = Client(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY)
 

humidity_v = aio.feeds('humidity')
temperature_v=aio.feeds('temperature')
ldr_v=aio.feeds('ldr')


IO.setup(led,IO.OUT)
IO.setup(therm,IO.OUT)
IO.setup(fan,IO.OUT)
IO.setup(d4, IO.OUT)
IO.setup(d5, IO.OUT)
IO.setup(d6, IO.OUT)
IO.setup(d7, IO.OUT)
IO.setup(rs, IO.OUT)
IO.setup(en, IO.OUT)
IO.output(fan,IO.LOW)
IO.output(led,IO.LOW)
IO.output(therm,IO.LOW)

########################### LCD fnnnnn ################################################
def lcd_cmd(cmd):
    #cmd=ord(cmd)
    #print(cmd)
    IO.output(rs, IO.LOW)
    IO.output(d4, IO.LOW)
    IO.output(d5, IO.LOW)
    IO.output(d6, IO.LOW)
    IO.output(d7, IO.LOW)
    
  
        
    if(cmd & 0x10==0x10):
       IO.output(d4, IO.HIGH)
    if(cmd & 0x20==0x20):
       IO.output(d5, IO.HIGH)
    if(cmd & 0x40==0x40):
        IO.output(d6, IO.HIGH)
    if(cmd & 0x80==0x80):
        IO.output(d7, IO.HIGH)
       
    time.sleep(0.005)
    IO.output(en, IO.LOW)
    time.sleep(0.005)
    IO.output(en, IO.HIGH)
    time.sleep(0.005)

    IO.output(d4, IO.LOW)
    IO.output(d5, IO.LOW)
    IO.output(d6, IO.LOW)
    IO.output(d7, IO.LOW)
    
  
        
    if(cmd & 0x01==0x01):
       IO.output(d4, IO.HIGH)
    if(cmd & 0x02==0x02):
       IO.output(d5, IO.HIGH)
    if(cmd & 0x04==0x04):
        IO.output(d6, IO.HIGH)
    if(cmd & 0x08==0x08):
        IO.output(d7, IO.HIGH)
       
    time.sleep(0.005)
    IO.output(en, IO.LOW)
    time.sleep(0.005)
    
    IO.output(en, IO.HIGH)
    time.sleep(0.0005)
   

def lcd_data(cmd):
    cmd=ord(cmd)
    #print(cmd)
    IO.output(rs, IO.HIGH)
    
    IO.output(d4, IO.LOW)
    IO.output(d5, IO.LOW)
    IO.output(d6, IO.LOW)
    IO.output(d7, IO.LOW)

    
    if(cmd & 0x10==0x10):
       IO.output(d4, IO.HIGH)
    if(cmd & 0x20==0x20):
       IO.output(d5, IO.HIGH)
    if(cmd & 0x40==0x40):
        IO.output(d6, IO.HIGH)
    if(cmd & 0x80==0x80):
        IO.output(d7, IO.HIGH)
       
    time.sleep(0.0005)
    IO.output(en, IO.LOW)
    time.sleep(0.0005)
    
    IO.output(en, IO.HIGH)
    time.sleep(0.0005)

    IO.output(d4, IO.LOW)
    IO.output(d5, IO.LOW)
    IO.output(d6, IO.LOW)
    IO.output(d7, IO.LOW)
    
  
        
    if(cmd & 0x01==0x01):
       IO.output(d4, IO.HIGH)
    if(cmd & 0x02==0x02):
       IO.output(d5, IO.HIGH)
    if(cmd & 0x04==0x04):
        IO.output(d6, IO.HIGH)
    if(cmd & 0x08==0x08):
        IO.output(d7, IO.HIGH)
       
    time.sleep(0.005)
    IO.output(en, IO.LOW)
    time.sleep(0.005)
    
    IO.output(en, IO.HIGH)
    time.sleep(0.0005)
    

def lcd_ini():

  lcd_cmd(0x33) 
  lcd_cmd(0x32) 
  lcd_cmd(0x06)
  lcd_cmd(0x0C) 
  lcd_cmd(0x28) 
  lcd_cmd(0x01) 
  time.sleep(0.0005)


def lcd_string(c):
      l=len(c)
      print(c)
      
      for i in range(l):
          lcd_data(c[i])

          
 
lcd_ini()


while True:

    lcd_cmd(0x01)
    lcd_string("SERICULTURE")
    time.sleep(0.5)
    humidity, temperature = Adafruit_DHT.read_retry(dht, dhtpin)
    i=ldr.value
##    print (IO.input(ldr.value))

    
    temp = str(temperature)
    hum = str(humidity)
    ldr1 = str(ldr.value)
    lcd_cmd(0x01)
    lcd_string("Temp:")
    lcd_cmd(0x0c)
    lcd_string(temp)
    time.sleep(1)
    lcd_cmd(0x01)
    lcd_string("Hum:")
    lcd_cmd(0xc0)
    lcd_string(hum)
    time.sleep(1)
    aio.send(temperature_v.key, temp)
    aio.send(humidity_v.key, hum)
    aio.send(ldr_v.key, ldr1)  
 
    print("temp: ",temperature)
    print("hum: ",humidity)
    if (temperature>30) :
        lcd_cmd(0x01)
        lcd_string("temp high")
        
##        print("temp high")
        IO.output(fan,IO.HIGH)
        IO.output(therm,IO.HIGH)
        port.write(b'AT\r\n')
        rcv = port.read(10)
        print(rcv)
        time.sleep(1)

        port.write(b"AT+CMGF=1\r")
        print("Text Mode Enabled…")
        time.sleep(3)
        port.write(b'AT+CMGS="8459199189"\r')
        msg = "temperature high"
        print("sending message….")
        time.sleep(3)
        port.reset_output_buffer()
        time.sleep(1)
        port.write(str.encode(msg+chr(26)))
        time.sleep(1)
        print("message sent…")
    
    else:
        lcd_cmd(0x01)
        lcd_string("temp normal")
        IO.output(fan,IO.LOW)
        IO.output(therm,IO.LOW)
##        print("temp low")

    print(i)
    time.sleep(1)
    if (i>0.0) :
        print("low")
        IO.output(led,IO.LOW)
        lcd_cmd(0x01)
        lcd_string("light off")

        time.sleep(1)
            
        
    else:
        lcd_cmd(0x01)
        lcd_string("light on")
        print("high")
        IO.output(led,IO.HIGH)
        port.write(b'AT\r\n')
        rcv = port.read(10)
        print(rcv)
        time.sleep(1)

        port.write(b"AT+CMGF=1\r")
        print("Text Mode Enabled…")
        time.sleep(3)
        port.write(b'AT+CMGS="8459199189"\r')
        msg = "light on"
        print("sending message….")
        time.sleep(3)
        port.reset_output_buffer()
        time.sleep(1)
        port.write(str.encode(msg+chr(26)))
        time.sleep(1)
        print("message sent…")
    
  
