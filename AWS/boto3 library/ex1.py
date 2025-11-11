import boto3
#using client
s3=boto3.client('s3')

response=s3.list_buckets()

for i in response['Buckets']:
    print(i.get('Name'))
print("-"*55)
#using resource

s2=boto3.resource('s3')

for i in s2.buckets.all():
    print(i.name)