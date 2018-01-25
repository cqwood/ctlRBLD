from __future__ import print_function
import boto3
import datetime
from os import environ
from bcrypt import hashpw, gensalt



def lambda_handler(event, context):
    formData = event["body"]
    user = formData['username']
    pw = formData['PW']
    mail = formData['EM']
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Users')
    hashedpw = hashpw(pw.encode('utf-8'), gensalt())

    response = table.put_item(
    Item={
        'username': user,
        'password': hashedpw.decode('utf-8'),
        'email': mail,
        'registered': str(datetime.datetime.now()),
        'verified': False
    }
    )
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
