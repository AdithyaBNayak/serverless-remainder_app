## AWS Services Used
- DynamoDB
- API Gateway
- AWS Lambda
- Simple Notification Service

## Concepts Covered
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

## Pattern 
![pattern](https://github.com/AdithyaBNayak/serverless-remainder_app/blob/dbSTreamAndTTL/images/reminder-app.jpg) 