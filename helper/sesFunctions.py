import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('ses')

class SESHelper:
    def send_email(self, email_id, message):
        send_email = client.send_email(
            Source= os.environ['fromEmail'],
            Destination={
                'ToAddresses': [email_id],                
            },
            Message={
                'Subject': { 'Data': 'Reminder!!'},
                'Body': {
                    'Text': {'Data': message},                    
                }
            },            
        )

        logger.info(send_email)
        return send_email['ResponseMetadata']['HTTPStatusCode']

        

