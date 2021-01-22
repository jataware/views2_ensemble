
import boto3
import requests

profile = "wmuser"
bucket_name = "world-modelers"

session = boto3.Session(profile_name=profile, aws_access_key_id="get key", aws_secret_access_key="get key")

s3 = session.resource("s3")
s3_client = session.client("s3")

bucket = s3.Bucket(bucket_name)

count = 0
for obj in bucket.objects.all():
    if obj.key == "data/views2/storage/data.zip":
        print(obj.key)

file_name = "/home/ubuntu/views2_ensemble_updated/OpenViEWS2/storage.zip"
s3_key = "data/views2/storage/data.zip"



s3_client.upload_file(file_name,
                      bucket_name,
                      s3_key,  # here we specify the key we wish the file to have in S3
                      ExtraArgs={'ACL':'public-read'}) # here we make the file public


print('done')
