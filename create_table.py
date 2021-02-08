import boto3


# Create table
def create_covid_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='CovidData',
        KeySchema=[
            {
                'AttributeName': 'hash',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'date',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'hash',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'date',
                'AttributeType': 'S'
            }

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    covid_table = create_covid_table()
    print("Table status:", covid_table.table_status)
