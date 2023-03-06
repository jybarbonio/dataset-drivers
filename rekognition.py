import csv
import boto3

# basic image function to fetch AWS AI face recognition data results
# currently researching how to 
def send_image(imgpath):
    # your access .csv may have a different name
    with open('access_credentials.csv', 'r') as input:
        next(input)
        rd = csv.reader(input)
        for line in rd:
            id_access_key = line[0]
            key_secret_access = line[1]

    client = boto3.client('rekognition', 
                        region_name = 'us-west-1',
                        aws_access_key_id = id_access_key,
                        aws_secret_access_key = key_secret_access)

    # send off local file imgpath to AWS Rekognition with face detect results returned
    with open(imgpath, 'rb') as source_image:
        source_bytes = source_image.read()

    response = client.detect_faces(Image = {'Bytes': source_bytes})

    print(response)