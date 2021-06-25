import sys
import Adafruit_DHT
import RPi.GPIO as IO # Import Raspberry Pi GPIO library
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()
from Adafruit_IO import RequestError, Client, Feed
import time
from time import sleep
import serial
IO.setwarnings(False)
IO.setmode(IO.BCM) 
pump1=21
pump2=20
pump3=16
trig=26
echo=6
soil=17
buzzer=1

ser = serial.Serial(
port='/dev/ttyUSB0',
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)
ADAFRUIT_IO_KEY = 'aio_BlvS21qTXQV1sCVDL0bEO3RefkER'
ADAFRUIT_IO_USERNAME = 'heenim96'
aio = Client(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY)
 

t1_hum = aio.feeds('planthum')
t1_temp=aio.feeds('planttemp')
t1_level=aio.feeds('plantlevel')
t2_temp=aio.feeds('fishtemp')
t2_level=aio.feeds('fishlevel')
t2_ph = aio.feeds('fishph')
##moisture_feed=aio.feeds('soilmoisture')

IO.setup(soil,IO.IN,pull_up_down=IO.PUD_UP)
##IO.setup(soil1,IO.IN,pull_up_down=IO.PUD_UP)
IO.setup(pump1, IO.OUT, initial=IO.LOW) # Set pin 40 to be an output pin
IO.setup(trig,IO.OUT)
IO.setup(echo,IO.IN)
IO.setup(buzzer, IO.OUT, initial=IO.LOW)
IO.setup(pump2, IO.OUT, initial=IO.LOW) # Set pin 38 to be an output pin
IO.setup(pump3, IO.OUT, initial=IO.LOW) # Set pin 38 to be an output pin



while True:
    humidity, temperature1 = Adafruit_DHT.read_retry(11, 12)
    sleep(1)
    tem=str(temperature1)
    hum=str(humidity)
    print("temperature"  ,temperature1)
    print("humidity"  ,humidity)
    time.sleep(1)
        
############################# Tank 1 ######################################

    aio.send(t1_temp.key, tem)
    aio.send(t1_hum.key, hum)
    IO.output(pump2,IO.LOW)
    IO.output(pump1,IO.LOW)
    if IO.input(soil)==IO.HIGH:
        print("empty")
        IO.output(pump2,IO.HIGH)
        print("pump2 on")
        
       
    elif IO.input(soil)==IO.LOW:
        print("full")
        IO.output(pump1,IO.HIGH)
        print("pump1 on")
    aio.send(t1_level.key, str(soil))
        
      

########################################### Fish Tank2 #############################################
    
    temperature = sensor.get_temperature()
    temp=str(temperature)
    print("The temperature is %s celsius" % temperature)
    time.sleep(1)
    aio.send(t2_temp.key, temp)
    pulse_end=0
    count=0
    IO.output(trig,False)
    time.sleep(0.2)
    IO.output(trig,True)
    time.sleep(0.00001)
    IO.output(trig,False)
    while IO.input(echo)==0:
        pulse_start=time.time()
        count=count+1
        if count>1000:
            count=0
            break
    count=0
    while IO.input(echo)==1:
        pulse_end=time.time()
        count=count+1
        if count>1000:
            count=0
            break
    count=0
    pulse_duration=pulse_end - pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    print(distance)
    level=distance-0.5
    watel=float(level)
    dist=str(watel)
    print("Distance:",watel,"cm")
    aio.send(t2_level.key,dist)
   
    sleep(2)
    time.sleep(0.03)
    received_data=ser.read()
    data_left=ser.inWaiting()
    received_data+=ser.read(data_left)
    #print(received_data[2:10])
    ph=received_data[5:9]
    print("PH:", ph)
    #print(ph)
   ## acid=str(ph)
    
    acid=float(ph)

    print("Ph value uploaded")
    aio.send(t2_ph.key,str(acid))
    time.sleep(3)
    IO.output(buzzer,IO.LOW)
    IO.output(pump3,IO.LOW)
    
    if IO.input(soil)==IO.LOW and watel<3:
        IO.output(pump3,IO.LOW)
        IO.output(pump1,IO.LOW)
        print("both tank are full")

    if acid>12:
        IO.output(buzzer,IO.HIGH)
        print("waste water")


    if watel>3:
        IO.output(pump3,IO.HIGH)
        time.sleep(1)
        print("pump3 on")
        print("water is low")

    
        
time.sleep(2)


