# Get the NYT data and send to the cleanData module for code cleanup

import csv
import urllib.request
import json

def lambda_handler(event, context):
    # Data from NYT
    nyt_data = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
    nyt_response = urllib.request.urlopen(nyt_data)
    nyt_contents = csv.reader(nyt_response.read().decode('utf-8').splitlines())

    # Data from JHU for recoveries
    jhu_data = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv?opt_id=oeu1606875624763r0.5077944167011417'
    jhu_response = urllib.request.urlopen(jhu_data)
    jhu_contents = csv.reader(jhu_response.read().decode('utf-8').splitlines())

    # Dictionary to store the data
    data_dict = {}

    # Add NYT data to dictionary
    for row in nyt_contents:
        if row[0] != 'date':
            data_dict[row[0]] = {'cases': row[1], 'deaths': row[2], 'recovered': 0}

    # Update dictionary to include recoveries from JHU data
    for row in jhu_contents:
        if row[1] == 'US':
            data_dict[row[0]]['recovered'] = row[4]

    print("2020-12-10 data: ", data_dict['2020-12-10'])
    return {
        'statusCode': 200,
        'body': data_dict
    }