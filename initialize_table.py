import json 
from decimal import Decimal
import boto3 

# Referenced: 
# https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html
# https://www.section.io/engineering-education/python-boto3-and-amazon-dynamodb-programming-tutorial/

# Create table for items being sold
def create_items_table(dynamodb=None):
    # Create dynamodb object
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    # Create table with item name and id as the key
    table = dynamodb.create_table(
        TableName='Items',
        KeySchema=[
            {
                'AttributeName': 'item_name',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'item_id',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'item_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'item_id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            # 10 strongly consistent reads per second
            'ReadCapacityUnits': 10,
            # 10 writes per second
            'WriteCapacityUnits': 10
        }
    )
    return table

def load_data(items, dynamodb=None):
    # Create dynamodb object
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    # Get items table
    items_table = dynamodb.Table('Items')
    # Import items into table
    for item in items:
        item_name = (item['item_name'])
        item_id = item['item_id']
        # Print to ensure item is imported
        print("Imported item:", item_name, item_id)
        items_table.put_item(Item=item)


if __name__ == '__main__':
    item_table = create_items_table()
    # Ensure table prints that it is available
    print("Status:", item_table.table_status)

    # Import all items from data.json
    with open("data.json") as json_file:
        item_list = json.load(json_file, parse_float=Decimal)
    load_data(item_list)