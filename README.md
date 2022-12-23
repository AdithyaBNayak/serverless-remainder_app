# Reminder App (using Serverless Framework)
This mini app allows the user to send the reminder message to a particular person whenever specified. The user can set the reminder, to deliver it to the destination via SMS text or an email.


![pattern](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/emailIntegration/images/reminderapp.png) 


## Requirements
---
- AWS Account with sufficient permissions to make necessary AWS service calls and manage AWS resources.
- AWS CLI installed and configured.
- Serverless installed to create a template using Serverless Framework.

## How it works
---

Note: It is required that the EmailId or the Contact Number has to be verified in SES Sandbox and SNS Sandbox respectively inorder to send the reminder.

![verifyUser](https://github.com/AdithyaBNayak/serverless-reminder_app/blob/emailIntegration/images/verifyUser.png)


You can also try to move out of [Sandbox](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html) account to avoid this particular step 






## AWS Services Used
---
- DynamoDB
- API Gateway
- AWS Lambda
- Simple Notification Service
- Simple Email Service

## Concepts Covered
---
- ### DynamoDB TTL
  Amazon DynamoDB [Time to Live](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) (TTL) is useful to delete items that lose relevance after a specific time.

  Points to be noted:
  - No extra cost is involved in using ttl.
  - The DB item must contain the attribute specified when TTL was enabled on the table.
  - The TTL attribute’s value must be a top-level Number data type.
  - The TTL attribute’s value must be a timestamp in Unix epoch time format in seconds.
  - The TTL attribute value must be a datetimestamp with an expiration of no more than five years in the past

- ### DynamoDB Streams
  
- ### Lambda Event Source Filtering for DynamoDB
- ### Text Messaging (SMS) using SNS
- ### Sending Emails using SES

