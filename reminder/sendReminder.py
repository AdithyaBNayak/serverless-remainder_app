import logging
from helper.snsFunctions import SNSHelper

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(event)
    records = event["Records"]

    # Fetch each reacord that got streamed from DynamoDB
    for record in records:
        try: 
            image = record['dynamodb']['OldImage']
            phone = image['user']['S']
            message = image['message']['S']

            # Trying to send the message            
            if SNSHelper().publish_message(phone,message) != 200:
                logger.info(f"Message not sent for the given number {phone} ")
            logger.info(f"Message sent for the given number {phone} ")
        except:
            logger.info(f"Message  not sent for the given number {phone} ")
    return