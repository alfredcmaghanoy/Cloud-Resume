import json  # Importing JSON module to handle JSON data
import boto3 # library used to interact with AWS resources (in this case dynamoDB)

class PageViewCounter:
    def __init__(self, table_name):
        # Creating a DynamoDB resource object
        self.dynamodb = boto3.resource('dynamodb')

        # Accessing the specific DynamoDB table
        self.table = self.dynamodb.Table(table_name)

    def get_views(self):
        # Fetch current views count
        response = self.table.get_item(Key={'id': '0'})

        # Check if 'views' exists, otherwise start at 0
        return response.get('Item', {}).get('views', 0)

    def increment_views(self):
        # Increment views
        views = self.get_views() + 1

        # Update the table with the new views count
        self.table.put_item(Item={'id': '0', 'views': views})

        # Return the updated view count
        return views

def lambda_handler(event, context):
    # Create an instance of the counter class
    counter = PageViewCounter('cloudresume-test')
    
    # Increment and get the updated view count
    updated_views = counter.increment_views()
    return updated_views