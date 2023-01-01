# Reminder App (using Serverless Framework)

This mini app allows the user to send the reminder message to a particular person whenever specified. The user can set the reminder, to deliver it to the destination via SMS text or an email.


![pattern](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/main/images/reminderapp.png) 


## Requirements
---
- AWS Account with sufficient permissions to make necessary AWS service calls and manage AWS resources.
- AWS CLI installed and configured.
- Serverless installed to create a template using [Serverless Framework](https://www.serverless.com/).



## How it works
---

Note: It is required that the EmailId or the Contact Number has to be verified in SES Sandbox and SNS Sandbox respectively inorder to send the reminder. There is a API created for the same.

![verifyUser](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/main/images/verifyUser.png)

![verifyEmail](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/main/images/emailNotverified.png)

![verifyPhone](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/main/images/phoneNotVerified.png)

You can also try to move out of [Sandbox](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html) account to avoid this particular step.


### AWS Services Used
---
- DynamoDB
- API Gateway
- AWS Lambda 
- Simple Notification Service
- Simple Email Service


### Concepts Covered
---
- #### Request Body Validation in API Gateway
  You can configure API Gateway to perform [basic validation of an API request](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-method-request-validation.html) before proceeding with the integration request. When the validation fails, API Gateway immediately fails the request, returns a 400 error response to the caller.
  In API Gateway, a model defines the data structure of a payload. In [API Gateway models](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-create-model.html) are defined using the [JSON schema draft 4](https://datatracker.ietf.org/doc/html/draft-zyp-json-schema-04).

  Below is the JSON Schema we define. We can specify all the mandatory fields in the request body in the 'required' list. Also inside properties we have mentioned the datatype of each of the field values, the enum type present for 'type' field and also the regex pattern to enter phone number/emailId.
  ```
  {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "The reminder POST Schema",
    "required": ["ttl", "type", "message", "owner", "contact"],
    "properties": {
      "owner": { "type": "string" },
      "type": { 
        "type": "string",
        "enum": [ "email", "text"]
    },
      "message": { "type": "string" },
      "contact": { 
        "type": "string",
        "pattern": "([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,})|(^\\++[1-9][0-9]{7,14}$)"
    },
      "ttl": { "type": "number"}
    }
  }
  ```
  The above JSON Schema is referenced in serverless.yml file in functions section. We can also define the model name and model description here.
    ```
    request:
      schemas:
        application/json:
          schema: ${file(post_request.json)}
          name: addReminderModel
          description: 'Validation model for Adding Reminder'
    ```
  ANy validation failure will result in status code '400', with the message 'Invalid Request Body' as shown in the figures below.  
  ![models](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/main/images/contact-regexerror.png)
  In the above image, we see that the regex doesnt match with the emailId provided.
  ![models](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/main/images/enum-error.png)
  In the schema specified, we have mentioned 'type' field to be of enum type. Any value other than 'email'/'text' will fail the validation process.

- #### DynamoDB TTL
  Amazon DynamoDB [Time to Live](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) (TTL) is useful to delete items that lose relevance after a specific time.

  Points to be noted:
  - No extra cost is involved in using ttl.
  - The DB item must contain the attribute specified when TTL was enabled on the table.
  - The TTL attribute’s value must be a top-level Number data type.
  - The TTL attribute’s value must be a timestamp in Unix epoch time format in seconds.
  - The TTL attribute value must be a datetimestamp with an expiration of no more than five years in the past.

  We set the reminder time(ttl field) of each record to be the ttl attribute in each reminder. Since we wont be needing the record after the reminder gets sent, we will be deleting the record setting the ttl.
  ```
  TimeToLiveSpecification: 
    AttributeName: ttl
    Enabled: True
  ```
    
- #### DynamoDB Streams
  A [DynamoDB stream](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) is an ordered flow of information about changes to items in a DynamoDB table.
  While enabling DynamoDB Stream we choose the information that will be written to the stream whenever the data in the table is modified:
    - Key attributes only (`KEYS_ONLY`) — Only the key attributes of the modified item.
    - New image (`NEW_IMAGE`) — The entire item, as it appears after it was modified.
    - Old image (`OLD_IMAGE`) — The entire item, as it appeared before it was modified.
    - New and old images (`NEW_AND_OLD_IMAGES`) — Both the new and the old images of the item.
  ```
  StreamSpecification: 
    StreamViewType: NEW_AND_OLD_IMAGES 
  ```

  As the reminder record gets deleted from the DyanamoDB table, we stream it to sendReminder lambda function. The sendReminder lambda function is responsible to send the reminder message to mentioned emailId or mobile number.
  We mention the stream event for the sendReminder lambda as shown below:
  ```
  events:
    - stream:
        type: dynamodb
        arn:
          Fn::GetAtt: [reminderTable, StreamArn]
        filterPatterns:
          - eventName: [REMOVE]
  ```
  Here we specify the stream type to be of 'dynamodb', and also the arn of the DynamoDB table from where the record is getting streamed.         
  
- #### Lambda Event Filtering for DynamoDB
  With [Lambda event filtering](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html) you can use filter expressions to control which events Lambda sends to your function for processing.
  Whenever an action on DynamoDB putItem or updateItem or deleteItem occurs, the `INSERT` or `MODIFY` or `REMOVE` events are triggered respectively if DynamoDB Streams are enabled.
  Heres how we filter the DynamoDB record, which gets deleted from our table.
  ```
  filterPatterns:
    - eventName: [REMOVE]
  ```
  
- #### Sending SMS using SNS and Emails using SES
  We use boto3 [SNS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html) and [SES](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html) Client to interact with the SNS and SES Service from AWS Lambda function using Python Programming language.

  To send  the reminder through SNS, we use `set_sms_attributes()` function to set the default settings for sending SMS messages and `publish()` function to directly send the SMS to the provided phone number.
  ```
  client = boto3.client('sns')

  set_sms_attributes = client.set_sms_attributes(
      attributes={'DefaultSMSType': 'Transactional'}
    )
  logger.info(set_sms_attributes)
  
  publish_message_response = client.publish(
      PhoneNumber= phone_num,
      Message= message,        
    )
  ```
  To send an email through SES, we use `send_email()` function.
  Note: We can provide the 'from emailId' in the config.conf file.

  ```
  client = boto3.client('ses')

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
  ```


### Testing
---
When we successfully add an Email Reminder we get the following response:
![addEmailReminder](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/main/images/addemailReminderSuccess.png)

Successfully adding SMS text reminder:
![addPhoneReminder](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/main/images/success-addReminder.png)

Reminder messages in phone and email is shown below:
![phoneReminder](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/main/images/text-reminder.jpeg)
![emailReminder](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/main/images/email-reminder.jpeg)