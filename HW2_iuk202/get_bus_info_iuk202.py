#importing relevant packages
from __future__ import print_function
import os
import pandas as pd
import numpy as np
import urllib2
import sys
import json

#system arguments
if len(sys.argv) != 4:
    print("You did not enter the appropriate number of arguments. Please try again")
    sys.exit()
mta_key = sys.argv[1]
bus_line = sys.argv[2]
bus_line_csv = sys.argv[3]

#reading data
url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + mta_key + "&VehicleMonitoringDetailLevel=calls&LineRef=" + bus_line
response = urllib2.urlopen(url)
data = response.read()
data = json.loads(data)

#getting data for each independent bus
indbus = data['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

#creating the datalist and populating the dataframe
datalist = []
for i in indbus:
    dict = {}
    dict['Longitude'] = str(i['MonitoredVehicleJourney']['VehicleLocation']['Longitude'])
    dict['Latitude'] = str(i['MonitoredVehicleJourney']['VehicleLocation']['Latitude'])
    try:
    	dict['Stop'] = str(i['MonitoredVehicleJourney']['MonitoredCall']['StopPointName'])
    except BaseException:
    	dict['Stop'] = 'N/A'
    try:
    	dict['Status'] = str(i['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance'])
    except BaseException:
		dict['Status'] = 'N/A'
    datalist.append(dict)
df = pd.DataFrame(datalist)

#writing the dataframe to the csv file
df.to_csv(str(bus_line_csv))
