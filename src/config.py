import logging
import os
import sys

import boto3

required_envs = ["AWS_DEFAULT_REGION", "AWS_ACCESS_KEY_ID",
                 "AWS_SECRET_ACCESS_KEY", "SQS_QUEUE_URL"]

for r in required_envs:
    if not os.environ.get(r):
        print("Missing {} env".format(r))
        sys.exit(100)

SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL")

sqs = boto3.client('sqs')

logging.basicConfig(format='%(message)s', level=logging.INFO)