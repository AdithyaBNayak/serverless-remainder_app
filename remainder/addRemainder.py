import json
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
dbName = os.environ['ddbName']
table = dynamodb.Table(dbName)

client = boto3.client('sns')

def handler(event, context):
    logger.info(event)
    body = json.loads(event['body'])
    logger.info(body)

    response = client.list_sms_sandbox_phone_numbers()
    logger.info(response)
    phone_nos = []
    for phone_no in response['PhoneNumbers']:
        if phone_no['Status'] == 'Verified':
            phone_nos.append(phone_no['PhoneNumber'])

    if body['user'] not in phone_nos:
        # response = client.create_sms_sandbox_phone_numbber(
        #     PhoneNumber= body['user'],
        #     LanguageCode='en-US'
        # )
        return {
            "statusCode": 200,
            "body": "Phone number not verified in SMS sandbox"
        }       


    item = {
        'user': body['user'],
        'ttl': body['ttl'],
        'owner': body['owner'],
        'message': body['message']
    }    

    table.put_item(Item=item)
    logger.info("Record inserted into the DB")

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }  
