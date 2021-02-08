import boto3


# Delete covid data DynamoDB table for testing purposes
def delete_covid_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('CovidData')
    table.delete()


if __name__ == '__main__':
    delete_covid_table()
    print("Covid data table deleted.")
