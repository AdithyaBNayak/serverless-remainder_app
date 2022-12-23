import logging

from helper.snsFunctions import SNSHelper
from helper.sesFunctions import SESHelper

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_sms(phone, message):
    # Trying to send the message            
    if SNSHelper().publish_message(phone,message) != 200:
        logger.info(f"Message not sent for the given number {phone} ")
    logger.info(f"Message sent for the given number {phone} ")

def send_email(email_id, message):
    # Trying to send the EMail
    if SESHelper().send_email(email_id,message) != 200:
        logger.info(f"Email not sent for the given {email_id} ")
    logger.info(f"Email  sent successfully for {email_id}")   

def handler(event, context):
    logger.info(event)
    records = event["Records"]

    # Fetch each reacord that got streamed from DynamoDB
    for record in records:
        try: 
            image = record['dynamodb']['OldImage']
            message = image['message']['S']

            # If the reminder type is SMS/text
            if image['type']['S'] == 'text':
                logger.info("Fetching the mobile number and sending the SMS..")
                phone = image['contact']['S']
                send_sms(phone, message)

            # If the reminder type is Email
            elif image['type']['S'] == 'email':
                logger.info("Fetching the emailId and sending the email...")
                email_id = image['contact']['S']
                send_email(email_id, message)
                                
        except:
            logger.info(f"Reminder  not sent due to errors!")
    return