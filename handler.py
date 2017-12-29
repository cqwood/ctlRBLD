import requests
import datetime
from requests_aws_sign import AWSV4Sign
from boto3 import session
import boto3

date = str(datetime.datetime.now())
    

def hello(event, context):
    input = event["body"]
    user, pw = input.split("&")[0], input.split("&")[1]
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Users')
    
    response = table.get_item(Key={'username':str(user.split("=")[1])})
    if pw.split("=")[1] == response['Item']["password"]:
        if response['Item']["verified"] == True:
            url = getURL()
            status = 200
            update = table.update_item(
            Key={
                'username': str(user.split("=")[1])
            },
            UpdateExpression="set lastLogin = :d",
            ExpressionAttributeValues={
                ':d' : date
            },
            ReturnValues="UPDATED_NEW"
            )
        else:
            status = 403
            url = "Please validate email"
    else:
        url = "Invalid login"
        status = 403

    resp = {
        "statusCode": status,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": str(url)
    }
    
    return resp
def getURL():
    sess = session.Session()
    credentials = sess.get_credentials()
    region = sess.region_name or 'us-east-2'
    service = 'execute-api'

    # let's talk to our AWS Elasticsearch cluster
    auth=AWSV4Sign(credentials, region, service)

    response = requests.get('https://qgmg1prdi9.execute-api.us-east-2.amazonaws.com/prod/getURL',
                        auth=auth)
    return str(response.content).split("'")[1]

