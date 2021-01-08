# Get the NYT data and send to the cleanData module for code cleanup

import csv
import urllib.request

# Data from NYT
nytData = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
nytResponse = urllib.request.urlopen(nytData)
nytContents = csv.reader(nytResponse.read().decode('utf-8').splitlines())

# Data from JHU for recoveries
jhuData = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv?opt_id=oeu1606875624763r0.5077944167011417'
jhuResponse = urllib.request.urlopen(jhuData)
jhuContents = csv.reader(jhuResponse.read().decode('utf-8').splitlines())

# Dictionary to store the data
dataDict = {}

# Add NYT data to dictionary
for row in nytContents:
    if row[0] != 'date':
        dataDict[row[0]] = {'cases': row[1], 'deaths': row[2], 'recovered': 0}

# Update dictionary to include recoveries from JHU data
for row in jhuContents:
    if row[1] == 'US':
        dataDict[row[0]]['recovered'] = row[4]

# print("2020-12-10 data: ", dataDict['2020-12-10'])