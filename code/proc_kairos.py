import os
import time
import csv
import json
import requests
from joblib import Parallel, delayed
import time
import boto3
from boto3 import client

def is_img_url(url_img):
    try:
        url_img = url_img.replace("http!++", "http://")
        url_img = url_img.replace("+", "/")

        img_format = ('image/png', 'image/jpg', 'image/jpeg')
        r = requests.head(url_img)
        if r.headers['content-type'] in img_format:
            return (url_img, "True")
        else:
            return (url_img, "False")
    except:
        print("IMAGE FAILED TO PROCESS")
        return (url_img, "False")

def wrap_is_img_url(dir_img):
    list_passfail = Parallel(n_jobs = -1)(delayed(is_img_url)
            (file) for file in os.listdir(dir_img))
    
    for i in list_passfail:
        print(i)

    print(len(list_passfail))

def get_kairos(c, app_id, app_key, url, dir_json):
    if(c % 4 == 0):     # assuming no jsons were created for imgs yet, 60 / 14 threads = ~4
        print("WAITING for rate-limit", c)
        time.sleep(60.0)

    try:
        url_kairos = 'https://api.kairos.com/enroll'

        if os.path.exists(dir_json + url[0] + "_detected_kairos" + ".json") == False:
            #print("processing", url_img)
            # post request for kairos enroll
            post_header = {
                'app_id' : app_id,
                'app_key' : app_key,
                'content-type' : 'application/json',
            }
            post_body = {
                'image' : url[1],
                'subject_id' : 'filler',
                'gallery_name' : 'scooter_dataset_kairos',
                'multiple_faces' : 'false'
            }

            r = requests.post(url_kairos, headers=post_header, json=post_body)
            url_replace = url[0].replace('_detected_face', 'detected_kairos')

            # save received json data, explicity remove .type extensions, ensure json format
            with open(dir_json + url_replace + ".json", "w", encoding='utf-8') as outfile:
                json.dump(r.json(), outfile, ensure_ascii=False, indent=2)
        else:
            #print(url_img, "already exists")
            pass
    except:
        print("error", url_replace)

def wrap_get_kairos(list_url, dir_json):
    # your access .csv may have a different name
    with open('C:\\Users\\John\\Desktop\\AIScooter\\credentials\\credentials_kairos.csv', 'r') as input:
        next(input)
        rd = csv.reader(input)
        for line in rd:
            app_id = line[0]
            app_key = line[1]

    # make dir_json folder for kairos json responses
    if(os.path.isdir(dir_json) == False):
        os.mkdir(dir_json)

    # parallelized implementation (fast)
    Parallel(n_jobs = -1)(delayed(get_kairos)
            (c, app_id, app_key, url, dir_json) for c, url in enumerate(list_url))

    # single thread implementation (slow but used for debugging)
    #for url in list_url:
    #    get_kairos(app_id, app_key, url, dir_json)

def read_s3():
    # your access .csv may have a different name
    with open('C:\\Users\\John\\Desktop\\AIScooter\\credentials\\credentials_rekog.csv', 'r') as input:
        next(input)
        rd = csv.reader(input)
        for line in rd:
            id_access_key = line[0]
            key_secret_access = line[1]

    client = boto3.client('s3', 
        region_name = 'us-west-1',
        aws_access_key_id = id_access_key,
        aws_secret_access_key = key_secret_access)
    
    urls = []


    paginator = client.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket='scooterfaces')

    for page in page_iterator:
        for key in page['Contents']:
            # https://bucket-name.s3.region-code.amazonaws.com/key-name
            str_url = 'https://' + 'scooterfaces' + '.s3' + '.us-west-1' + '.amazonaws.com/' + key['Key']
            name = key['Key']
            str_url = str_url.replace('+', '%2B')
            #print(name, str_url)
            urls.append((name, str_url))

    return urls


# MAIN METHOD
if __name__ == "__main__":
    # function call for testing image links in filenames
    #dir_img = 'C:\\Users\\John\\Desktop\\AIScooter\\imagesS2\\'
    #wrap_is_img_url(dir_img)



    dir_img = 'C:\\Users\\John\\Desktop\\AIScooter\\datasets\\img\\img_exact_hamming_rekog_bbox\\'

    # json kairos results location
    dir_json = 'C:\\Users\\John\\Desktop\\AIScooter\\datasets\\json\\json_exact_hamming_rekog_kairos_bbox\\'
    
    list_url = read_s3()
    wrap_get_kairos(list_url, dir_json)

