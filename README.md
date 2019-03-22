# Serverless Python DynamoDB

Serverless Python 3 function that reads and writes to a DynamoDB table.

- API Gateway that makes the Lambda function accessible from the public internet
- DynamoDB table that is only accessible from the Lambda function
- Running in a virtual private cloud (VPC)
- IAM role that serves the smallest possible set of permissions to get the job done
- AWS boto3 Python library
- JWT

## Usage

Above stack is supposed to allow for the following simple use case:

1. Send a POST request to the API Gateway endpoint with JSON body (see below). The Lambda function writes the JSON body into the DynamoDB table
JSON body:
```
{
  "astronaut_id": "1234567890",
  "astronaut_name": "calvinbui"
}
```
Also set a JWT Authorization header:
`Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.QszFqwfE2A9GFj3f81FWVckgbJabfmYUffFJnBKuqsc`
2. Send a GET request to the API Gateway REST endpoint with the astronaut ID as the path parameter (`/astronaut/1234567890`). The Lambda function reads the respective entry from the DynamoDB table and returns it as JSON


## Setup

Install serverless: `npm install -g serverless`

Create a new serverless service: `serverless create --template aws-python3 --path serverless-python-dynamodb`

Configure credentials in `~/.aws/credentials`

Deploy to different profiles: `serverless deploy --aws-profile dev --region ap-southeast-2`

Delete stack: `serverless remove -v --aws-profile dev --region ap-southeast-2`

Get Info: `serverless info --aws-profile dev --region ap-southeast-2`

JWT: `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.QszFqwfE2A9GFj3f81FWVckgbJabfmYUffFJnBKuqsc`

## Areas of Improvement

1. Lock down Lambda security egress so it can only talk to API Gateway. Still using default 0.0.0.0/0 * outbound but has no gateway so cant talk to Internet
2. VPC Endpoint for API Gateway, see how that works
3. Abstraction layer
4. Router/Authenticating class, refactor + reuse