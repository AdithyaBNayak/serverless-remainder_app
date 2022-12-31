import json
import os
import boto3
import logging
from boto3.dynamodb.conditions import Key
from decimal import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB Boto3 resource
dynamodb = boto3.resource('dynamodb')
dbName = os.environ['ddbName']
table = dynamodb.Table(dbName)

def getAllReminders(event,context):
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    logger.info(data)    
    return {
        "statusCode": 200,
        # "body": data
        "body":  json.dumps(data, cls=DecimalEncoder)
    }    


def getReminder(event,context):
    logger.info(event)
    # body = json.loads(event['pathParameters'])
    body = event['pathParameters']
    records = table.query(
        KeyConditionExpression=Key('user').eq(f"USER#{body['id']}")
    )['Items']
    logger.info(records)
    return {
        "statusCode": 200,
        "body": json.dumps(records, cls=DecimalEncoder)
    }

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)    