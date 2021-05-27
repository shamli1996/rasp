import time
import RPi.GPIO as GPIO
##from pulsesensor import Pulsesensor
import serial
import sys
import urllib3
import time
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

myAPI = 'GTS3IEI1CHCWAXTE' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

hb=16
trig=21
echo=23

rs=11
en=13
d4=22
d5=24
d6=26
d7=32

GPIO.setup(hb,GPIO.IN)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5, GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

beat=0
p=0
sec=0
temperature=0


######################################################################## GSM #########################################################################

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
        port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
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
        serial_Print("heartbeat increases\n")
        serial_Print("BPM Out of Range:"+ str(beat))
        delay(500)
        ##port.write(26.encode())
        serial_Print("\x1A")
        #serial_receive()
        #serial_receive()
        print("SMS1 SEND")
        delay(1000)


def gsm_2():
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
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
    serial_Print("temperature increase:\n")
    serial_Print("High Temperature:" +str(temperature))
    delay(500)
    ##port.write(26.encode())
    serial_Print("\x1A")
    #serial_receive()
    #serial_receive()
    print("SMS3 SEND")
    delay(1000)


def gsm_3():
        port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
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
        serial_Print("urine level is exceeded\n")
        delay(500)
        ##port.write(26.encode())
        serial_Print("\x1A")
        #serial_receive()
        #serial_receive()
        print("SMS2 SEND")
        delay(1000)
                     
########################### LCD fnnnnn ################################################

def lcd_cmd(cmd):
    #cmd=ord(cmd)
    #print(cmd)
    GPIO.output(rs, GPIO.LOW)
    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    
  
        
    if(cmd & 0x10==0x10):
       GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x20==0x20):
       GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x40==0x40):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x80==0x80):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.005)
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.005)

    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    
  
        
    if(cmd & 0x01==0x01):
       GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x02==0x02):
       GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x04==0x04):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x08==0x08):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.005)
    
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.0005)
   

def lcd_data(cmd):
    cmd=ord(cmd)
    #print(cmd)
    GPIO.output(rs, GPIO.HIGH)
    
    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)

    
    if(cmd & 0x10==0x10):
       GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x20==0x20):
       GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x40==0x40):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x80==0x80):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.0005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.0005)
    
    GPIO.output(en, GPIO.HIGH)
    time.sleep(0.0005)

    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    
  
        
    if(cmd & 0x01==0x01):
       GPIO.output(d4, GPIO.HIGH)
    if(cmd & 0x02==0x02):
       GPIO.output(d5, GPIO.HIGH)
    if(cmd & 0x04==0x04):
        GPIO.output(d6, GPIO.HIGH)
    if(cmd & 0x08==0x08):
        GPIO.output(d7, GPIO.HIGH)
       
    time.sleep(0.005)
    GPIO.output(en, GPIO.LOW)
    time.sleep(0.005)
    
    GPIO.output(en, GPIO.HIGH)
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

############################################################################################################################################################



while True:
   ## print("insideee")    
##    lcd_cmd(0x01)
##    lcd_string("comatose")
##    time.sleep(0.5)
    cnt=GPIO.input(hb);
    if(cnt==False):
        beat=beat+1
        time.sleep(0.05)
        print("beat")
    
    else:
        time.sleep(0.05);
        p+=1
    
        if(p>5):
            p=0
            sec=sec+1
   #print(sec);

            if(sec>60):
                sec=0
                print("beat:",beat)
                bt=str(beat)
       
                #time.sleep(1);
      
                if((beat<60) and (beat!=0) or (beat>120)):
                    print("heart beat exceeded")
                    bt=str(beat)
                    lcd_cmd(0x01)
                    lcd_string("beat:")
                    lcd_cmd(0x06)
                    lcd_string(bt)
                    lcd_cmd(0xc0)
                    lcd_string("heart beat exceeded")
                    time.sleep(1)
                    gsm()
          
                elif((beat>60) or (beat<120)):
                    print("heart beat normal")
                    lcd_cmd(0x01)
                    lcd_string("beat:")
                    lcd_cmd(0x06)
                    lcd_string(bt)
                    lcd_cmd(0xc0)
                    lcd_string("heart beat normal")
                    time.sleep(1)


                pulse_end=0
                count=0
                GPIO.output(trig,False)
                time.sleep(0.2)
                GPIO.output(trig,True)
                time.sleep(0.00001)
                GPIO.output(trig,False)
                while GPIO.input(echo)==0:
                    pulse_start=time.time()
                    count=count+1
                    if count>1000:
                        count=0
                        break
                count=0
                while GPIO.input(echo)==1:
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
                watel=round(watel,2)
                dist=str(watel)
                
                print("Distance:",watel,"cm")
                lcd_cmd(0x01)
                lcd_string("Dist:")
                lcd_cmd(0x06)
                lcd_string(dist)
                time.sleep(1)

                if watel<5:
                     print("urine level is exceeded")
                     lcd_cmd(0xc0)
                     lcd_string("level is exceeded")
                     time.sleep(1)
                     gsm_3()

                else:
                     print("urine level is normal")
                     lcd_cmd(0xc0)
                     lcd_string("level is normal")
                     time.sleep(1)

                temperature = sensor.get_temperature()
                print("The temperature is %s celsius:" , temperature)
                tem=str(temperature)
                lcd_cmd(0x01)
                lcd_string("Temp:")
                lcd_cmd(0x06)
                lcd_string(tem)
                time.sleep(1)
                
                if(temperature>33):
                     print("High Temperature")
                     lcd_cmd(0xc0)
                     lcd_string("High Temperature")
                     time.sleep(1)
                     gsm_2()
                    
                else:
                     print("Normal Temperature")
                     lcd_cmd(0xc0)
                     lcd_string("Normal temperature")
                     time.sleep(1)

                http = urllib3.PoolManager()
                url = baseURL +'&field1=%s' % (beat)+'&field2=%s' % (temperature)+'&field3=%s' % (dist)

                print(url)
                resp = http.request('GET', url)


                     
        
    
                print()
                time.sleep(4)
