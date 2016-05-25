#!/usr/bin/python

# SOFTWARE.
import os
import sys
import time
import datetime

import Adafruit_DHT

# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
DHT_TYPE = Adafruit_DHT.DHT22

# Example of sensor connected to Raspberry Pi pin 23
DHT_PIN  = 4
# Example of sensor connected to Beaglebone Black pin P8_11
#DHT_PIN  = 'P8_11'

# Setup parameter to connect Netpie Cloud
APP = 'DomeTempStations'
TOPIC = 'temp'
URL = 'https://api.netpie.io/topic/{0}/{1}'.format(APP,TOPIC)

KEY = 'NtkXjByk5bQZJLs'
SECRET = 'd76t0i3DdU6z2hbtEm4jcsFJ0'
ALIAS = 'Dome'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 5

while True:

    # Attempt to get sensor reading.
    humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)

    # Skip to the next reading if a valid measurement couldn't be taken.
    # This might happen if the CPU is under a lot of load and the sensor
    # can't be reliably read (timing is critical to read the sensor).
    if humidity is None or temp is None:
        time.sleep(2)
        continue

    print('Temperature: {0:0.1f} C'.format(temp))
    print('Humidity:    {0:0.1f} %'.format(humidity))

    # Append the data in the spreadsheet, including a timestamp
    try:
        temp = '{0:0.1f}'.format(temp)
        command = 'curl -X PUT "{0}" -d "{1}" -u {2}:{3}'.format(URL,temp,KEY,SECRET)
        os.system(command)
    except:
        # Error appending data, most likely because credentials are stale.
        # Null out the worksheet so a login is performed at the top of the loop.
        print('Sending to Netpie Error')
        time.sleep(FREQUENCY_SECONDS)
        continue

    # Wait xx seconds before continuing
     time.sleep(FREQUENCY_SECONDS)

