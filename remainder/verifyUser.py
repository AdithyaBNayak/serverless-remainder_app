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

    if body['phoneNumber'] not in phone_nos:

        if 'otp' in body:
            try:
                response = client.verify_sms_sandbox_phone_number(
                    PhoneNumber=body['phoneNumber'],
                    OneTimePassword=body['otp']
                )
                logger.info("Phone number verified and saved in Sandbox")
                return {
                    "statusCode": 200,
                    "body": "Wrong OTP Provided!!"
                }  
            except Exception as e:
                logger.info(e)
                return {
                    "statusCode": 400,
                    "body": "Phone number verified and saved in Sandbox.."
                }                

        else:    
            logger.info("Trying to send the OTP")
            response = client.create_sms_sandbox_phone_number(
                PhoneNumber=body['phoneNumber'],
                LanguageCode='en-US'
            )
            logger.info("OTP Sent..")
            return {
                "statusCode": 200,
                "body": "Sent the OTP, verify it!!"
            }

        return {
                "statusCode": 500,
                "body": "Phone number not verified.. Try Again!!"
            }    