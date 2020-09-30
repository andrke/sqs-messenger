import argparse
import json
import time

from config import *


def send_message(message_attributes={}, message_body=("")):
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        DelaySeconds=10,
        MessageAttributes=message_attributes,
        MessageBody=message_body
    )

    return response['MessageId']


def receive_message():
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    try:
        message = response['Messages'][0]
    except KeyError:
        return {}
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=SQS_QUEUE_URL,
        ReceiptHandle=receipt_handle
    )
    return message


def poll(sleep=1):
    while True:
        msg = receive_message()
        if msg:
            logging.info(json.dumps(msg))
        time.sleep(sleep)


def parse_args():
    parser = argparse.ArgumentParser(description='Simple SQS handler')
    parser.add_argument('cmd', choices=('send', 'receive', 'poll'),
                        help='Actions to proceed')
    parser.add_argument('--msg', help='Message string')
    parser.add_argument('--msg-attr', help='Message attributes JSON')
    parser.add_argument('--receive-all', dest="all", action='store_true', help='Receive all queued messages')

    return parser.parse_args()


def main(args=parse_args()):
    if args.cmd == "send":
        message_attributes = json.loads(args.msg_attr)
        logging.info(send_message(message_attributes, (args.msg)))
        return 0
    elif args.cmd == "receive":
        if args.all:
            while args.all:
                msg = receive_message()
                if not msg:
                    args.all = False
                else:
                    logging.info(json.dumps(msg))
        else:
            msg = receive_message()
            if msg:
                logging.info(json.dumps(msg))

        return 0
    elif args.cmd == "poll":
        poll()
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
