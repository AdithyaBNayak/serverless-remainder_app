import json
import logging
from botocore.exceptions import ClientError
from helper.snsFunctions import SNSHelper
from helper.sesFunctions import SESHelper


# client = boto3.client('ses')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(event)
    body = json.loads(event['body'])
    logger.info(body)

    if body['type'] == 'email':
        email_id = body['contact']
        ses = SESHelper()

        verified_emails = ses.list_verified_emails()
        if email_id in verified_emails:
            return {
                    "statusCode": 200,
                    "body": "Email Id already verified/ Check your mail box"
                }

        status_code = ses.send_verification_email(email_id)
        if status_code == 200:
            return {
                "statusCode": 200,
                "body": "Verification Email Sent.. Please Verify!!"
            }

        return {
            "statusCode": 500,
            "body": "Cannot send the verification email!"
        }      

    elif body['type'] == 'text':
        sns = SNSHelper()
        # Get the list of all verified phone nos from SMS Sandbox
        phone_nos = sns.list_phone_nos()
        if body['contact'] in phone_nos:
            return {
                    "statusCode": 200,
                    "body": "Phone number already verified"
                }

        # If OTP provided in the input try to verify it.
        if 'otp' in body:
            try:
                otp = body['otp']
                phone_num = body['contact']
                sns.verify_number(phone_num, otp)
                return {
                    "statusCode": 200,
                    "body": "Phone number verified and saved in Sandbox"
                }      
            except Exception as e:
                logger.info(e)
                return {
                    "statusCode": 400,
                    "body": "Wrong OTP Provided"
                }
                        
        # If OTP not provided in the input, try to send it
        else:    
            logger.info("Trying to send the OTP")
            try:
                sns.send_otp_for_verification(body['contact'])
                return {
                    "statusCode": 200,
                    "body": "Sent the OTP, verify it!!"
                }
            except ClientError:
                logger.info("Error.. Check if the number you provided is right")
                return {
                    "statusCode": 500,
                    "body": "Error.. Check if the number you provided is right"
                }            

    return {
            "statusCode": 500,
            "body": "Phone number already registered!!"
        }    