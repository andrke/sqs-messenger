# sqs-messenger
SQS Messenger example
# Requrements
- IAM account with AmazonSQSFullAccess
- Amazon SQS url

## Example
### virtual env

0. clone it

``git@github.com:andrke/sqs-messenger.git``

``cd sqs-messenger``
1. Set env variables

``SQS_QUEUE_URL=<https://sqs.<aws-region>.amazonaws.com>;``

``AWS_ACCESS_KEY_ID=<aws-access-key>;``

``AWS_SECRET_ACCESS_KEY=<aws-secret-access-key>;``

``AWS_DEFAULT_REGION=<aws-region>``

2. Create virtual env

`python3 -mvenv venv` 

3. Activate venv

``venv/bin/activate``

4. Install dependencies

``pip install -r requirements.txt``

5.1 Send the message

``src/sqs-handler send --msg "Message" --msg-attr "{\"Subject\": { \"DataType\": \"String\", \"StringValue\": \"message\"}}"``

5.2 Receive the last message

`src/sqs-handler receive`

5.3 Receive all messages and exit

`src/sqs-handler receive`

5.4 Poll messages every second

`src/sqs-handler poll`

### Dockerfile

`docker build -t <image_tag> . && docker run --env AWS_ACCESS_KEY_ID=<aws-access-key> --env AWS_SECRET_ACCESS_KEY=<aws-secret-access-key> --env SQS_QUEUE_URL=<sqs-url> --env AWS_DEFAULT_REGION=<aws-region> <image_tag> send --msg "<Message>" --msg-attr "{\"ExampleAttr\": { \"DataType\": \"String\", \"StringValue\": \"examplevalue\"}}"`