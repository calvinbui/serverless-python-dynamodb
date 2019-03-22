#!/usr/bin/env python3
import os
import json
import jwt
import boto3

jwt_secret = "superdupersecret"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def jwt_valid(token):
    try:
        # 'Bearer <token>'
        jwt.decode(token.split()[1], jwt_secret, algorithms=['HS256'])
        return True
    except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError, AttributeError, IndexError, TypeError):
        return False

def create(event, context):
    if jwt_valid(event.get('headers', '').get('Authorization', '')):
        data = json.loads(event.get('body'))
        try:
            # dont use .get() on dict to raise exception
            astronaut = {
                'astronaut_id': data['astronaut_id'],
                'astronaut_name': data['astronaut_name']
            }
            table.put_item(Item=astronaut)
            response = {
                'statusCode': 200,
                'body': json.dumps(astronaut)
            }
        except KeyError:
            response = {
                'statusCode': 400,
                'body': json.dumps('Missing astronaut_id or astronaut_name')
            }
    else:
        response = {
            'statusCode': 401,
            'body': json.dumps('Unauthorized')
        }

    return response


def get(event, context):
    if jwt_valid(event.get('headers', '').get('Authorization', '')):
        results = table.get_item(
            Key={
                'astronaut_id': event.get('pathParameters').get('astronaut_id')
            }
        )
        if results.get('Item'):
            response = {
                'statusCode': 200,
                'body': json.dumps(results.get('Item'))
            }
        else:
            response = {
                'statusCode': 404,
                'body': json.dumps('No astronaut found')
            }
    else:
        response = {
            'statusCode': 401,
            'body': json.dumps('Unauthorized')
        }

    return response
