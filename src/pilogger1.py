#!/usr/bin/env python
#
# This project will collect temperature and humidity information using a DHT type sensor.
#

import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import datetime

# General settings
prog_name = "pilogger1.py"

# DHT Sensor settings
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.

dht_sensor_port = 4                     # Connect the DHT sensor to port 4
dht_sensor_type = Adafruit_DHT.DHT11

device = "pi-003"           		    # Host name of the data collector device

GPIO.setmode(GPIO.BCM)                  # Use the Broadcom pin numbering
GPIO.setup(dht_sensor_port, GPIO.IN)    # DHT sensor port as input

# Print welcome 
print('[{0:s}] starting on {1:s}...'.format(prog_name, datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

# Main loop
try:
    while True:
        hum, temp = Adafruit_DHT.read_retry(dht_sensor_type, dht_sensor_port)
        temp = temp * 9/5.0 + 32
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        print('{0:s},{1:s},{2:0.1f},{3:0.1f}'.format(device,date,temp,hum))
        time.sleep(1)

except (IOError,TypeError) as e:
	print("Exiting...")

except KeyboardInterrupt:  
    	# here you put any code you want to run before the program   
    	# exits when you press CTRL+C  
	print("Stopping...")

finally:
	print("Cleaning up...")  
	GPIO.cleanup() # this ensures a clean exit