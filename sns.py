import boto3

client = boto3.client('sns', region_name = 'us-east-1')


def sendNotification(msg):
	msg = str(msg)
	response = client.publish(
    TopicArn='arn:aws:sns:us-east-1:002265909788:Wikipedia-Edits',
    Message=msg,
    Subject='Unusual Stream Rate'
	)
	return 

if __name__ == '__main__':
	sendNotification("test")