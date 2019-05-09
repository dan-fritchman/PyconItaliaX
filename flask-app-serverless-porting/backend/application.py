# Copyright 2013. Amazon Web Services, Inc. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import json

import boto3
from botocore.something import ConditionalCheckFailedException

TABLE_NAME = os.environ['STARTUP_SIGNUP_TABLE']
SNS_TOPIC = os.environ['NEW_SIGNUP_TOPIC']

client = boto3.client('sns')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def welcome():
    return flask.render_template('index.html')


def signup(event, context):
    print("[DEBUG] Signup with body: %s" % event['body'])

    signup_data = json.loads(event['body'])

    try:
        store_in_dynamo(signup_data)
        publish_to_sns(signup_data)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedError':
            return _response(400, "OK")
    except Exception as e:
        print(e)
        return _response(500, "KO")
    return Response(json.dumps(signup_data), status=201, mimetype='application/json')


def _response(status, message):
    return {
        'statusCode': status,
        'body': json.dumps({'message': message})
    }


def store_in_dynamo(signup_data):
    signup_item = Item(ddb_table, data=signup_data)
    signup_item.save()


def publish_to_sns(signup_data):
    client.publish(
        TopicArn=SNS_TOPIC,
        Message="New Signup",

    )
    try:
        client.publish(app.config['NEW_SIGNUP_TOPIC'], json.dumps(signup_data), "New signup: %s" % signup_data['email'])
    except Exception as ex:
        print("Error publishing subscription message to SNS: %s" % ex.message)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
