
# coding: utf-8

# ### Lesson 4: Save Raspberry Pi Sensor Data to MySQL Database
# 
# 
# #### Learning Objectives:
# <ol>
#     <li>Model how IoT device can save sensor data to back end database server for later analyis</li>
#     <li>Learn how to access data from MySQL databases from a Raspberry Pi Python program</li>  
# </ol>

# <b>Exercise 1: Modify Python script to add code to save data to MySQL database</b>

# In[ ]:

#!/usr/bin/env python
#
# This project will collect temperature and humidity information using a DHT22 sensor
# and send this information to a MySQL database.
#
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import datetime
import MySQLdb

# General settings
prog_name = "pilogger2.py"

# Settings for database connection
hostname = '172.20.101.81'
username = 'piuser3'
password = 'logger'
database = 'pidata'

dht_sensor_port = 4                     # Connect the DHT sensor to port D
dht_sensor_type = Adafruit_DHT.DHT11    # Sensor type

device = 'pi-003'			            # Host name of the Pi

GPIO.setmode(GPIO.BCM)                  # Use the Broadcom pin numbering
GPIO.setup(led, GPIO.OUT)               # LED pin set as output
GPIO.setup(dht_sensor_port, GPIO.IN)    # DHT sensor port as input

# Routine to insert temperature records into the pidata.temps table:
def insert_record( device, datetime, temp, hum ):
	query = "INSERT INTO temps3 (device,datetime,temp,hum) "                 "VALUES (%s,%s,%s,%s)"
    	args = (device,datetime,temp,hum)

    	try:
        	conn = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
		cursor = conn.cursor()
        	cursor.execute(query, args)
		conn.commit()

    	except Exception as error:
        	print(error)

    	finally:
        	cursor.close()
        	conn.close()

# Print welcome 
print('[{0:s}] starting on {1:s}...'.format(prog_name, datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

# Main loop
try:
	while True:
		hum, temp = Adafruit_DHT.read_retry(dht_sensor_type, dht_sensor_port)
		temp = temp * 9/5.0 + 32
		now = datetime.datetime.now()
		date = now.strftime('%Y-%m-%d %H:%M:%S')
		insert_record(device,str(date),format(temp,'.2f'),format(hum,'.2f'))
		time.sleep(180)

except (IOError,TypeError) as e:
	print("Exiting...")

except KeyboardInterrupt:  
    	# here you put any code you want to run before the program   
    	# exits when you press CTRL+C  
	print("Stopping...")

finally:
	print("Cleaning up...")  
	GPIO.cleanup() # this ensures a clean exit


# <b>Exercise 2: Test the temperature logger program</b>
# 
# Run the python code on the Raspberry Pi by running the program as follows:
# <pre>
# $ sudo chmod +x pylogger2.py
# $ sudo ./pylogger2.py
# </pre>
# 
# 

# Now let's check the database`

# In[5]:

get_ipython().magic(u'load_ext sql')


# In[7]:

get_ipython().run_cell_magic(u'sql', u'mysql://piuser3:logger@172.20.101.81/pidata', u'select * from temps3;')


# Press CTRL+C to cancel the program<br>
# 
# You may want to change the sleep time to a larger number to take samples ever 5 minutes (300) seconds for example.
