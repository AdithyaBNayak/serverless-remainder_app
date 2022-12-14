import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class SNSHelper:
    
    def __init__(self):
        # SNS Boto3 Client
        self.client = boto3.client('sns')

    # get the list pof verified phone numbers
    def list_phone_nos(self):        
        response = self.client.list_sms_sandbox_phone_numbers()
        logger.info(response)
        phone_nos = [phone_no['PhoneNumber'] for phone_no in response['PhoneNumbers'] 
                        if phone_no['Status'] == 'Verified']
        logger.info(f"Verified Phone Nos: {phone_nos}")
        return phone_nos        

    # Sending the message through SNS
    def publish_message(self, phone_num, message):
        set_sms_attributes = self.client.set_sms_attributes(
            attributes={'DefaultSMSType': 'Transactional'}
        )
        logger.info(set_sms_attributes)
        publish_message_response = self.client.publish(
            PhoneNumber= phone_num,
            Message= message,        
        )
        logger.info(publish_message_response)
        # return the status code
        return publish_message_response['ResponseMetadata']['HTTPStatusCode']

    # Verify the OTP sent to insert the number to SMS Sandbox
    def verify_number(self, phone_num, otp):    
        response = self.client.verify_sms_sandbox_phone_number(
                    PhoneNumber=phone_num,
                    OneTimePassword=otp
                )
        logger.info("Phone number verified and saved in Sandbox")

    # Send the OTP to the given number inorder to verify it
    def send_otp_for_verification(self, phone_num):
        response = self.client.create_sms_sandbox_phone_number(
                PhoneNumber=phone_num,
                LanguageCode='en-US'
            )
        logger.info("OTP Sent..")