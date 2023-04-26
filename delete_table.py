import boto3

# Referenced: 
# https://docs.aws.amazon.com/code-library/latest/ug/python_3_dynamodb_code_examples.html
# https://www.section.io/engineering-education/python-boto3-and-amazon-dynamodb-programming-tutorial/

def delete_items_table(dynamodb=None):
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    # get items table so it can be deleted
    items_table = dynamodb.Table('Items')
    items_table.delete()


if __name__ == '__main__':
    delete_items_table()
    # Once successful,
    print("Table deleted.")