from time import sleep
from RPLCD import CharLCD
import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode(IO.BCM) 
lcd = CharLCD(cols=16, rows=2, pin_rs=22, pin_e=23, pins_data=[25, 8, 7, 1])

lcd.write_string(u'Hello world!')
time.sleep(2)
lcd.clear()
