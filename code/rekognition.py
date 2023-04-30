import os
import time
import csv
import boto3
from boto3 import client
import json
import base64
import cv2
from PIL import Image, ImageDraw
import io
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
# @runtimer
def send_image(dir_img, dir_json, file):
    # first ensure json folder for images is created
    # note mkdir only makes 1 new level of sub-directory
    if(os.path.isdir(dir_json) == False):
        os.mkdir(dir_json)

    # your access .csv may have a different name
    with open('credentials_rekog.csv', 'r') as input:
        next(input)
        rd = csv.reader(input)
        for line in rd:
            id_access_key = line[0]
            key_secret_access = line[1]

    client = boto3.client('rekognition', 
        region_name = 'us-west-1',
        aws_access_key_id = id_access_key,
        aws_secret_access_key = key_secret_access)

    f = os.path.join(dir_img, file)
    # checking if it is a file, otherwise ignore
    if os.path.isfile(f):
        try:
            # send off local file imgpath to AWS Rekognition with face detect results returned
            # IMPORTANT: explicit base64 format of images is needed
            with open(f, 'rb') as image:
                img_b64 = base64.b64encode(image.read())
                img_b64_binary = base64.decodebytes(img_b64)

            # print("Sending: ", file)
            # obtain ALL derive-able attributes from faces in images
            dict_rkg = client.detect_faces(Image = {'Bytes': img_b64_binary}, Attributes=['ALL'])

            # save received json data, explicity remove .type extensions, ensure json format
            with open(dir_json + file + "_detected_face" + ".json", "w", encoding='utf-8') as outfile:
                json.dump(dict_rkg, outfile, indent = 2)
        except:
            print("An error occured: ", file)

# we are assuming all images contain a boundingbox since we filtered already
# save bounding boxes to new images in new file
def bbox_faces(dir_json, dir_img, dir_bbox):
    if(os.path.isdir(dir_bbox) == False):
        os.mkdir(dir_bbox)

    for file in os.listdir(dir_json):
        # print("opening", file)
        f = open(dir_json + file, "r")      # r is read only
        face_dict = json.loads(f.read())
        #print(file.replace("_detected_face.json", ""))

        #img = Image.open(dir_img + (file.replace("_detected_face.json", "")))
        print("opening:", str(dir_img + file.replace("_detected_face.json", "")))
        img = cv2.imread(str(dir_img + file.replace("_detected_face.json", "")), cv2.IMREAD_COLOR)
        file_extension = pathlib.Path((dir_img + file.replace("_detected_face.json", ""))).suffix
        #print("suffix: ", file_extension)
        h, w, _ = img.shape
        print("faces in img:", len(face_dict["FaceDetails"]))

        for c, bb in enumerate(face_dict["FaceDetails"]):
            # coordinates
            left = bb["BoundingBox"]["Left"] * w
            top = bb["BoundingBox"]["Top"] * h
            width = bb["BoundingBox"]["Width"] * w
            height = bb["BoundingBox"]["Height"] * h

            # rekog creates bbox parameters outside, pic dimensions, so revert to 0 instead of negative
            if(left < 0):
                left = 0.0
            if(top < 0):
                top = 0.0

            #print("w/h:", w, h)
            #print("bbox:", int(left), int(top), int(left + width), int(top + height))
            #cv2.rectangle(img, (int(left), int(top)), (int(left + width), int(top + height)), (0, 255, 0), 0)
            #cv2.imshow("image", img)
            #cv2.waitKey(0)

            roi = img[int(top):int(top+height), int(left): int(left+width)]
            str_new = str(dir_bbox + file.replace(file_extension + "_detected_face.json", "")
                         + "_detected_face" + str(c) + file_extension)
            cv2.imwrite(str_new, roi)

            #cv2.waitKey(0)


def print_ratio(dir_json):
    # func to count male/female ratio
    male = 0.00
    female = 0.00
    average = 0.00
    failures = 0

    for n, file in enumerate(os.listdir(dir_json)):
        f = open(dir_json + file, "r")  # r is read only
        face_dict = json.loads(f.read())

        # bb are the boundingboxes, i.e. however many faces found in an image
        for bb in face_dict["FaceDetails"]:
            try:
                print(n, bb["Gender"]["Value"])
                if bb["Gender"]["Value"] == "Male":
                    male += 1
                else:
                    female += 1
            except:
                print("error not found")
                failures += 1

    print(male, "males", female, "females")
    # (total - females) / total = male percentage and vice versa
    print("Male/Female ratio:\n",
        ((male+female)-female)/(male+female), "% Male\n",
        ((male+female)-male)/(male+female), "% female\n"
        "Total:", ((male+female)-female)/(male+female) + ((male+female)-male)/(male+female),
        "Failures:", failures)

dir_three = 'C:\\Users\\John\\Desktop\\AIScooter\\datasets\\json\\json_exact_hamming\\'
dir_faces = 'C:\\Users\\John\\Desktop\\AIScooter\\datasets\\json\\json_exact_hamming_rekog_faces\\'
dir_new = 'C:\\Users\\John\\Desktop\\AIScooter\\datasets\\json\\json_exact_hamming_rekog_faces_merge\\'
'''
# This loop orders AWS face recognition results for all images in a given directory
# this task has been completed and the dataset uploaded
# dictionary of AI results is returned
for n, file in enumerate(os.listdir(dir_img)):
    #send_image(dir_img, dir_json, file)
    print(n, " " + file)
'''

for file in os.listdir(dir_faces):
    tf = file.replace('_detected_face.json', '')

    if(os.path.isdir(dir_new) == False):
        os.mkdir(dir_new)

    if(os.path.exists(dir_three + tf + '_detected_label.json')):
        with open(dir_new + tf + "_detected_label.json", "w", encoding='utf-8') as create:
            pass

        #with open(dir_json + file + "_detected_face" + ".json", "w", encoding='utf-8') as outfile:
            #json.dump(dict_rkg, outfile, indent = 2)

        with open(dir_three + tf + '_detected_label.json', "r") as old:
            to_copy = json.load(old)
        with open(dir_new + tf + "_detected_label.json", "w") as new:
            json.dump(to_copy, new, indent=2)
    else:
        print(dir_three + tf + '_detected_label.json', 'does not exist')

    if(os.path.exists(dir_three + tf + '_detected_logo.json')):
        with open(dir_new + tf + '_detected_logo.json', "w", encoding='utf-8') as create:
            pass

        #with open(dir_json + file + "_detected_face" + ".json", "w", encoding='utf-8') as outfile:
            #json.dump(dict_rkg, outfile, indent = 2)

        with open(dir_three + tf + '_detected_logo.json', "r") as old:
            to_copy = json.load(old)
        with open(dir_new + tf + '_detected_logo.json', "w") as new:
            json.dump(to_copy, new, indent=2)
    else:
        print(dir_three + tf + '_detected_logo.json', 'does not exist')

    if(os.path.exists(dir_three + tf + '_detected_text.json')):
        with open(dir_new + tf + '_detected_text.json', "w", encoding='utf-8') as create:
            pass

        #with open(dir_json + file + "_detected_face" + ".json", "w", encoding='utf-8') as outfile:
            #json.dump(dict_rkg, outfile, indent = 2)

        with open(dir_three + tf + '_detected_text.json', "r") as old:
            to_copy = json.load(old)
        with open(dir_new + tf + '_detected_text.json', "w") as new:
            json.dump(to_copy, new, indent=2)
    else:
        print(dir_three + tf + '_detected_text.json', 'does not exist')

# bbox_faces(dir_json, dir_img, dir_bbox)