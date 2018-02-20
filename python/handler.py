import requests
import datetime
from requests_aws_sign import AWSV4Sign
from boto3 import session
import boto3
from bcrypt import checkpw
from json import loads
date = str(datetime.datetime.now())

#    params = event["body"].split("&")


def hello(event, context):
    user, pw = event["body"].split("&")[0].split("=")[1], event["body"].split("&")[1].split("=")[1]
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Users')

    response = table.get_item(Key={'username':str(user)})
    hashtest = checkpw(pw.encode('utf-8'), response['Item']["password"].encode('utf-8'))
    try:
        len(response['Item'])
    except:
        return "User ID does not exist"
    if hashtest ==  True:
        if response['Item']["verified"] == True:
            url = getURL()
            status = 200
            update = table.update_item(
            Key={
                'username': str(user)
            },
            UpdateExpression="set lastLogin = :d",
            ExpressionAttributeValues={
                ':d' : date
            },
            ReturnValues="UPDATED_NEW"
            )
        else:
            url = "Please verify account"
            status = 403
    else:
        url = "Invalid login"
        status = 403

    resp = {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": url
    }

    return resp
def getURL():
    sess = session.Session()
    credentials = sess.get_credentials()
    region = sess.region_name or 'us-east-2'
    service = 'execute-api'

    auth=AWSV4Sign(credentials, region, service)

    response = requests.get('https://lducscw0wh.execute-api.us-east-2.amazonaws.com/dev/api/geturl',
                        auth=auth)
    responseJSON = loads(response.content.decode("utf-8"))
    return responseJSON["body"]
