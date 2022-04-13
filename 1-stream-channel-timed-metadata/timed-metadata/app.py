#!/usr/bin/env python3

import datetime
import json
import time
import boto3
import sys
from random import randrange

'''
Creating a boto3 client for IVS. Noticed the explicit region_name argument. 
'''
ivs = boto3.client("ivs", region_name="us-east-1")

if __name__ == "__main__":
    '''
    This app only works if user passes IVS ARN as an argument. If not, print out message how to retrieve the ARN and use it with the app.
    '''
    if len(sys.argv) != 2:
        print("Usage: python app.py <channel_arn>")
        print("You will need to retrieve your channel ARN on IVS dashboard. https://us-east-1.console.aws.amazon.com/ivs/")
        sys.exit()

    channel_arn = sys.argv[1]
    '''
    Var i is only for identifier.
    '''
    i = 1

    '''
    Forever loop. Makes it easier to debug and do demo. :)
    '''
    while True:
        '''
        This is the metadata payload.
        '''
        data = {
            "current_time": datetime.datetime.utcnow().strftime('%Y-%b-%d-%H%M%S'),
            "question": "Question : {}".format(i),
            "answers": [
                "True",
                "False"
            ]
        }

        try:
            '''
            This is the call to put_metadata into IVS channel.
            '''
            response = ivs.put_metadata(
                channelArn=channel_arn,
                metadata=json.dumps(data)
            )
            print("***\n\nRequest: {}\n\nResponse: {}\n\n***".format(
                json.dumps(data), response["ResponseMetadata"]))
            i += 1
        except Exception as e:
            print("ERROR: {}".format(e))
        '''
        Sleep for 10 seconds so it won't bombard the API
        '''
        time.sleep(10)
