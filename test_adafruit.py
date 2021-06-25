
from Adafruit_IO import RequestError, Client, Feed

ADAFRUIT_IO_KEY = 'aio_BlvS21qTXQV1sCVDL0bEO3RefkER'
ADAFRUIT_IO_USERNAME = 'heenim96'

aio = Client(ADAFRUIT_IO_USERNAME,ADAFRUIT_IO_KEY)


adafruit =aio.feeds('adafruit')
t1_hum = aio.feeds('planthum')
t1_temp=aio.feeds('planttemp')
t1_level=aio.feeds('plantlevel')
t2_temp=aio.feeds('fishtemp')
t2_level=aio.feeds('fishlevel')
t2_ph = aio.feeds('fishph')
##except:
##    test_feed  = Feed(name='test')
##    test_feed = aio.create_feed(test_feed)
soil= str(434343)
aio.send_data(adafruit.key, 45)
aio.send(t1_temp.key, 43)
aio.send(t1_hum.key, 34)
aio.send(t1_level.key, 55)
aio.send(t2_temp.key, 'ab a')
aio.send(t2_level.key,'swd')
aio.send(t2_ph.key,soil)
