"""
Simple client script that uses Amazon's SNS to publish notifications to a topic.
The glory of SNS is that multiple subscribers can subscribe to a single topic, in multiple
formats. We currently have text messaging set up along with emails, but it's easy to set up other 
kinds of subscriptions (including HTTP, which can be used to integrate into the Slack API).

The configuration details, along with the access secret, are set as enviornment variables, 
or set in a config file in '~/.aws/credentials'. A sample credentials file is

*******************
[default]
aws_access_key_id = XXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXxXXXXXXXXX
*******************

We use the boto3 library to access SNS. For my particular SNS topic, I have chosen to host it in
N. Virginia (the zone hence being us-east-1).
"""
import boto3

client = boto3.client('sns', region_name = 'us-east-1')


def sendNotification(msg, subject='Unusual Stream Rate'):
	"""
	Send notifications to a topic ARN (which is basically the topic ID) with the msg and a subject.

	NOTE : Text Message only recieve the Subject Line, not the actual message. Emails are formatted the
	way we expect it to. Hence the texts serve as a reminder to check out Emails.
	"""
	msg = str(msg)
	response = client.publish(
    TopicArn='arn:aws:sns:us-east-1:002265909788:Wikipedia-Edits',
    Message=msg,
    Subject=subject
	)
	print subject, msg
	return response


# Simple testing of the sendNotification function if this is run as a mail module.
if __name__ == '__main__':
	sendNotification("test")