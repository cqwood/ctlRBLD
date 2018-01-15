import boto3
#services = ["IQDB", "BVoIP", "BRIX", "SIP", "WHOLESALE VoIP"]
#CUG = "asdf"
#prefix = "1.1.1.1/29"
#VPRN = "1234"
#communities = []
#policies = []



def handler(event, context):
    params = event["body"].split("&")
    CUG, platform, services = params[0].split("=")[1], params[1].split("=")[1], params[2].split("=")[1].split("+")

    if "-" in CUG:
        VPRN = CUG.split("-")[1]
    else:
        resp = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": "invalid CUG name"
        }
        return resp

    if len(params) == 4:
        prefix = params[3].split("=")[1]
    else:
        prefix = ""

    if platform == "ALLU":
        communities = []
        policies = []
        dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
        table = dynamodb.Table('Templates')
        response = table.get_item(Key={'Platform':'ALLU'})
        template, communityoptions, policyoptions = response["Item"]["template"], response["Item"]["community"], response["Item"]["policy-statement"]
        del services[len(services) - 1]
        for svc in services:
            if svc in communityoptions and svc in policyoptions:
                policies.append(policyoptions[svc])
                communities.append(communityoptions[svc])
            else:
                resp = {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": "invalid service name" + str(services)
                }
                return resp

        template = template.replace("{communities}", " ".join(communities))
        template = template.replace("{policies}", "".join(policies))
        if "BVoIP" in services or "SIP" in services or "WHOLESALE VoIP" in servies:
                pfxList = "prefix-list \"{CUG}-export\" prefix {0} longer".replace("{0}", prefix)
                template = template.replace("{prefix-list}", pfxList)
        else:
                template = template.replace("{prefix-list}", "")
        template = template.replace("{CUG}", CUG)
        template = template.replace("{VPRN}", VPRN)
        template = template.replace("\n", "<br>")

        resp = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": template
        }

        return resp
    else:
        resp = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "body": platform
        }
        return resp
