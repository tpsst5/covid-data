import csv
import urllib.request
import boto3

# Gets COVID-19 data from two csv links - from NYT and John Hopkins University. Puts data inside a dictionary
# and adds each date of data to an AWS DynamoDB table. Commented out sections for the code intended to be used
# as part of the AWS Lambda function.


# def lambda_handler(event, context): ## FOR AWS ##
# Data from New York Times
nyt_data = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
nyt_response = urllib.request.urlopen(nyt_data)
nyt_contents = csv.reader(nyt_response.read().decode('utf-8').splitlines())

# JHU CSV DATASET NO LONGER ACTIVE. REMOVED FROM CODE.
# Data from John Hopkins University for recoveries
# jhu_data = ('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined'
#            + '.csv?opt_id=oeu1606875624763r0.5077944167011417')
# jhu_response = urllib.request.urlopen(jhu_data)
# jhu_contents = csv.reader(jhu_response.read().decode('utf-8').splitlines())

# Dictionary to store the data & database object variable
data_dict = {}

# dynamoDB endpoint for local testing and CovidData table variable
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
table = dynamodb.Table('CovidData')

# Hash value for date row data
counter = 0

# Add NYT data to dictionary
for row in nyt_contents:
    # Check to see if past header
    if row[0] != 'date':
        counter += 1
        date_to_num = int(row[0].replace("-", ""))
        data_dict[row[0]] = {'hash': counter, 'date': date_to_num, 'cases': row[1], 'deaths': row[2]}

# JHU DATASET NO LONGER ACTIVE
# Merge JHU recovery data into dictionary
# for row in jhu_contents:
#    # Get just the US data
#    if row[1] == 'US':
#        data_dict[row[0]]['recovered'] = row[4]

# Add dictionary contents to DynamoDB table
item = {'hash': None, 'date': None, 'cases': None, 'deaths': None}  # 'recovered': None}
for date in data_dict:
    print('------------------')
    for row in data_dict[date]:
        if row == 'hash':
            item['hash'] = data_dict[date][row]
        elif row == 'date':
            item['date'] = data_dict[date][row]
        elif row == 'cases':
            item['cases'] = data_dict[date][row]
        elif row == 'deaths':
            item['deaths'] = data_dict[date][row]
        # JHU DATASET NO LONGER ACTIVE
        # elif row == 'recovered':
        #    item['recovered'] = data_dict[date][row]
    print('Adding: ', item)
    table.put_item(Item=item)

# For aws use only inside aws lambda function
# return {
#     'statusCode': 200,
#     'body': data_dict
# }
