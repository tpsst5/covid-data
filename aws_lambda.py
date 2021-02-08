import csv
import urllib.request
import json
import boto3

# Get the NYT data and send to the cleanData module for code cleanup


# import CovidCreateTable
import Database

# def lambda_handler(event, context):
# Data from NYT

nyt_data = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
nyt_response = urllib.request.urlopen(nyt_data)
nyt_contents = csv.reader(nyt_response.read().decode('utf-8').splitlines())

# Data from JHU for recoveries
jhu_data = ('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined'
            + '.csv?opt_id=oeu1606875624763r0.5077944167011417')
jhu_response = urllib.request.urlopen(jhu_data)
jhu_contents = csv.reader(jhu_response.read().decode('utf-8').splitlines())

# Dictionary to store the data & database object variable
data_dict = {}

# dynamoDB endpoint for local testing and CovidData table
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
table = dynamodb.Table('CovidData')

# Hash value for data
counter = 0
# database = Database.Database()


# Add NYT data to dictionary
for row in nyt_contents:
    # Check to see if past header
    if row[0] != 'date':
        counter += 1
        ########33 REPLACE DATE TO NUM FORMAT
        date_to_num = row[0]
        data_dict[row[0]] = {'hash': counter, 'date': row[0], 'cases': row[1], 'deaths': row[2], 'recovered': 0}

# Update dictionary to include recoveries from JHU data
for row in jhu_contents:
    # Get just the US data
    if row[1] == 'US':
        data_dict[row[0]]['recovered'] = row[4]



# Data added to DynamoDB table
for date in data_dict:
    # print(date)
    print('------------------')
    item = {'hash': None, 'date': None, 'cases': None, 'deaths': None, 'recovered': None}
    for row in data_dict[date]:
        if row == 'hash':
            item['hash'] = data_dict[date][row]
        elif row == 'date':
            item['date'] = data_dict[date][row]
        elif row == 'cases':
            item['cases'] = data_dict[date][row]
        elif row == 'deaths':
            item['deaths'] = data_dict[date][row]
        elif row == 'recovered':
            item['recovered'] = data_dict[date][row]
    # print(item)
    table.put_item(Item=item)
    # print('-------------------')




#     for item in covid_dict:
#         for metric in covid_dict[item]:
#             if metric == 'date':
#                 date = covid_dict[item][metric]
#                 test_item = {'Date': '01/01/0001', 'var2': 'test', 'var3': 'test2'}
#                 print("Adding date: ", date)
#                 table.put_item(Item=test_item)


json_data = json.dumps(data_dict, indent=4)

# print(json_data)


# send_data = CovidCreateTable(json_data)




# Test adding data
# def load_data(covid_dict, dynamodb=None):
#     if not dynamodb:
#         dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
#
#     table = dynamodb.Table('CovidData')
#     for item in covid_dict:
#         for metric in covid_dict[item]:
#             if metric == 'date':
#                 date = covid_dict[item][metric]
#                 test_item = {'Date': '01/01/0001', 'var2': 'test', 'var3': 'test2'}
#                 print("Adding date: ", date)
#                 table.put_item(Item=test_item)
#
#
# if __name__ == '__main__':
#     load_data(data_dict)
