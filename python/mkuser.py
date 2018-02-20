from __future__ import print_function
import boto3
import datetime
from os import environ
from bcrypt import hashpw, gensalt



def lambda_handler(event, context):
    user, pw, mail = event["body"].split("&")[0].split("=")[1], event["body"].split("&")[1].split("=")[1],event["body"].split("&")[2].split("=")[1]
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Users')
    hashedpw = hashpw(pw.encode('utf-8'), gensalt())

    response = table.put_item(Key={'username':str(user)})
    try:
        len(response['Item'])
    except:
        resp = {
            "statusCode": 304,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": "User ID already exists"
        }
        return resp
    Item={
        'username': user,
        'password': hashedpw.decode('utf-8'),
        'email': mail,
        'registered': str(datetime.datetime.now()),
        'verified': True
    }

    status = 200
    respBody = "successfully registered user {user}".format(user=user)
    resp = {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": respBody

    }

    return resp
#    return "handler works"
