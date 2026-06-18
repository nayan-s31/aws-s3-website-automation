import boto3
import json

bucket_name = "nayan-sdk-website-2026"

s3 = boto3.client('s3')

print("Connected to AWS S3 successfully!")

#Create a Bucket
#3.create_bucket(
#    Bucket=bucket_name,
#    CreateBucketConfiguration={
#        'LocationConstraint': 'ap-south-1'
#    }
#)

#print("Bucket Created Successfully")

#Enable Static Website Hosting
s3.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    }
)

print("Static Website Hosting Enabled")

# Upload HTML file
s3.upload_file(
    'website/index.html',
    bucket_name,
    'index.html',
    ExtraArgs={'ContentType': 'text/html'}
)

# Upload CSS file
s3.upload_file(
    'website/style.css',
    bucket_name,
    'style.css',
    ExtraArgs={'ContentType': 'text/css'}
)

print("Website Files Uploaded Successfully")

#Set Public Access Block Configuration to allow public access
s3.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': False,
        'IgnorePublicAcls': False,
        'BlockPublicPolicy': False,
        'RestrictPublicBuckets': False
    }
)

print("Public Access Enabled")

#Set Bucket Policy to allow public read access to the objects in the bucket
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": ["s3:GetObject"],
            "Resource": [
                f"arn:aws:s3:::{bucket_name}/*"
            ]
        }
    ]
}

s3.put_bucket_policy(
    Bucket=bucket_name,
    Policy=json.dumps(policy)
)

print("Bucket Policy Applied")

website_url = (
    f"http://{bucket_name}.s3-website.ap-south-1.amazonaws.com"
)

print("\nWebsite URL:")
print(website_url)