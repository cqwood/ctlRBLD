import requests
import datetime
from requests_aws_sign import AWSV4Sign
from boto3 import session
import boto3
from bcrypt import checkpw
from json import loads
date = str(datetime.datetime.now())
    

def hello(event, context):
    formData = event["body"]
    user, pw = formData['username'], formData['PW']
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('Users')

    response = table.get_item(Key={'username':str(user)})
    hashtest = checkpw(pw.encode('utf-8'), response['Item']["password"].encode('utf-8'))

    if hashtest ==  True:
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

    # let's talk to our AWS Elasticsearch cluster
    auth=AWSV4Sign(credentials, region, service)

    response = requests.get('https://4on98xzlnb.execute-api.us-east-2.amazonaws.com/dev/api/geturl',
                        auth=auth)
    responseJSON = loads(response.content.decode("utf-8"))
    return responseJSON["body"]

