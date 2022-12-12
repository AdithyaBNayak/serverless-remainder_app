import boto3
import logging

client = boto3.client('sns')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)
    records = event["Records"]

    for record in records:
        try: 
            image = record['dynamodb']['OldImage']
            phone_num = image['user']['S']
            message = image['message']['S']
            set_sms_attributes = client.set_sms_attributes(
                attributes={'DefaultSMSType': 'Transactional'}
            )
            logger.info(set_sms_attributes)
            publish_message_response = client.publish(
                PhoneNumber= phone_num,
                Message= message,        
            )
            logger.info(publish_message_response)
            
            if publish_message_response['ResponseMetadata']['HTTPStatusCode'] != 200:
                logger.info(f"Message not sent for the given number {phone_num} ")

            logger.info(f"Message sent for the given number {phone_num} ")

        except:
            logger.info(f"Message sent for the given number {phone_num} ")

    return