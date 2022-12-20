import json
import os
import boto3
import logging

from helper.snsFunctions import SNSHelper
from helper.sesFunctions import SESHelper

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB Boto3 resource
dynamodb = boto3.resource('dynamodb')
dbName = os.environ['ddbName']
table = dynamodb.Table(dbName)

def handler(event, context):
    logger.info(event)
    body = json.loads(event['body'])

    if body['type'] == 'text':
        # Get the list of all verified phone nos from SMS Sandbox
        phone_nos = SNSHelper().list_phone_nos()
        # If the phone number is not present in Sandbox
        if body['contact'] not in phone_nos:
            return {
                "statusCode": 500,
                "body": "Phone number not verified in SMS sandbox"
            }
    elif body['type'] == 'email': 
        verified_emails = SESHelper().list_verified_emails()
        if body['contact'] not in verified_emails:
            return {
                "statusCode": 500,
                "body": "Email not verified in SES sandbox"
            }

    # Insert the record to DynamoDB
    item = {
        'user': f"USER#{body['contact']}",
        'ttl': body['ttl'],
        'owner': body['owner'],
        'message': body['message'],
        'type': body['type'],
        'contact': body['contact']
    }
    table.put_item(Item=item)
    logger.info("Record inserted into the DB")

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }  