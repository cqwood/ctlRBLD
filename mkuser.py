from __future__ import print_function
import boto3
import datetime
from os import environ


def lambda_handler(event, context):
    input = event["body"]
    user, pw, mail = input.split("&")[0], input.split("&")[1], input.split("&")[2]
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Users')
    
    response = table.put_item(
    Item={
        'username': user.split("=")[1],
        'password': pw.split("=")[1],
        'email': mail.split("=")[1],
        'registered': str(datetime.datetime.now()),
        'verified': False
    }
    )
    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": environ['test']

    }
    
    return resp
#    return "handler works"
