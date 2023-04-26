from botocore.exceptions import ClientError
import boto3 
from boto3.dynamodb.conditions import Key

# Referenced: 
# https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html
# https://www.section.io/engineering-education/python-boto3-and-amazon-dynamodb-programming-tutorial/

def put_item(item_name, item_id, color, length, fabric, dynamodb=None):

    # Example call: put_item("Elliatt Espousal Sweetheart Mini Dress", 7, "Ivory", "33", "Polyester")
    # Example print: pprint(item_resp) (need to import pprint from pprint)

    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table
    items_table = dynamodb.Table('Items')
    response = items_table.put_item(
        # Data to be inserted
        Item={
            'item_name': item_name,
            'item_id': item_id,
            'info': {
                'Color': color,
                'Length': length,
                'Fabric': fabric,
                'Sold_Out': "False"
            }
        }
    )
    return response

def delete_item_func(item_name, item_id, dynamodb=None):

    # Example Usage: delete_response = delete_item("Reformation Zenni Dress", 3)
    # Example Print: if delete_response: pprint(delete_response)

    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    # Get items table
    items_table = dynamodb.Table('Items')

    try:
        response = items_table.delete_item(
            Key={
                'item_name': item_name,
                'item_id': item_id
            }
        )
    except ClientError as er:
        if er.response['Error']['Code'] == "FailedException":
            print(er.response['Error']['Message'])
        else:
            raise
    else:
        return response

def query_items(item_name, dynamodb=None):
    
    # Example query_id: query_id = "Selkie Strapless Mini Dress"
    # Example usage: items_data = query_items(query_id)
    # Example print: print(item_data['item_name'], ":", item_data['item_id']) for item_data in items_data

    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table to query
    items_table = dynamodb.Table('Items')
    response = items_table.query(
        KeyConditionExpression=Key('item_name').eq(item_name)
    )
    return response['Items']

def get_item(item_name, item_id, dynamodb=None):

    # Example usage: item = get_item("Reformation Zenni Dress", 3,)
    # Example print: if item: print(item) 
    
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    # Get items table to read from
    items_table = dynamodb.Table('Items')

    try:
        response = items_table.get_item(
            Key={'item_name': item_name, 'item_id': item_id})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']
    
# A method for printing items
def print_items(items):
    for item in items:
        print(f"\n{item['item_name']} : {item['item_id']}")
        print(item['info'])

def scan_items(dynamodb=None):

    # Example usage: scan_items(print_items)

    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    # Get items table
    items_table = dynamodb.Table('Items')
    done = False
    start_key = None
    item_list = []
    while not done:
        response = items_table.scan()
        items = response.get('Items', [])
        for item in items:
            item_list.append(item)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    
    return item_list

def update_item(item_name, item_id, color, sold_out, dynamodb=None):
    # Example usage: update_response = update_item("Reformation Zenni Dress", 3, "Ivory", 'True')
    # Example print: pprint(update_response) (must import pprint from pprint)

    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    # Specify the table
    items_table = dynamodb.Table('Items')

    response = items_table.update_item(
        Key={
            'item_name': item_name,
            'item_id': item_id
        },
        UpdateExpression="set info.Color=:color, info.Sold_Out=:sold_out",
        ExpressionAttributeValues={
            ':color': color,
            ':sold_out': sold_out
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def get_inventory_from_search(search_term):

    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    items_table = dynamodb.Table('Items')
    search_term = search_term.capitalize()
    scan_filter = {
        "item_name": {
            'ComparisonOperator': "CONTAINS",
            'AttributeValueList': [search_term]
        }
    }
    
    done = False
    start_key = None
    item_list = []
    while not done:
        response = items_table.scan(ScanFilter=scan_filter)
        items = response.get('Items', [])
        for item in items:
            item_list.append(item)
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    
    return item_list

if __name__ == '__main__':
    # item = get_item("Farm Rio Banana Cover-Up Dress", 2)
    # if item:
    #     # Print the data read
    #     print(item)
    # delete_item("Elliatt Espousal Sweetheart Mini Dress", 7)
    delete_item_func("Reformation Zenni Dress", 3)
    print('deleted')
    print(get_inventory_from_search("Zenni"))
    print('proof')
    put_item("Reformation Zenni Dress", 3, "White", "35", "Polyester")
    print(get_inventory_from_search("Zenni"))
    update_item("Reformation Zenni Dress", 3, "Ivory", 'True')
    print(get_inventory_from_search("Zenni"))
    # query_id = "Selkie Strapless Mini Dress"
    # items_data = search_items(query_id)
    # for item_data in items_data:
    #     print(item_data['item_name'], ":", item_data['item_id'])

    # items = scan_items()
    # print(items)