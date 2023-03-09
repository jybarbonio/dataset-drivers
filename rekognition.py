import os
import time
import re
import csv
import boto3
import json
import pathlib

# performance timer decorator measuring function performance 
def runtimer(func):
    def wrapper(dir, file):
        t1 = time.time()
        list = func(dir, file)
        t2 = time.time() - t1
        print(f'{func.__name__} took {t2} seconds to complete')
        return list
    return wrapper

# send image to AWS Rekognition which returns json dictionary of face detect results
@runtimer
def send_image(dir, file):
    # first create the dir to hold .json results if doesn't exist
    if(os.path.isdir(dir + "\\rekog_dataset") == False):
        os.mkdir(dir + "\\rekog_dataset")

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

    f = os.path.join(dir, file)
    # checking if it is a file, otherwise ignore
    if os.path.isfile(f):
        # send off local file imgpath to AWS Rekognition with face detect results returned
        with open(f, 'rb') as source_image:
            source_bytes = source_image.read()

        dict_rkg = client.detect_faces(Image = {'Bytes': source_bytes})
        # dict_rkg = json.dumps(dict_rkg, indent=2)  # write dictionary lines to file as str

        with open(dir + "\\rekog_dataset\\" + file + ".json", "w", encoding='utf-8') as outfile:
            json.dump(dict_rkg, outfile, indent=2)

# dictionary of AI results is returned
dir = 'C:\\Users\\John\\Desktop\\AIScooter\\imagesC\\imagesC'

for file in os.listdir(dir):
    send_image(dir, file)
