import os
import time
import csv
import boto3
import json
import base64

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
            with open(dir_json + file + ".json", "w", encoding='utf-8') as outfile:
                json.dump(dict_rkg, outfile, indent = 2)
        except:
            print("An error occured: ", file)
            
dir_img = 'C:\\Users\\John\\Desktop\\AIScooter\\images_faces\\'
dir_json = 'C:\\Users\\John\\Desktop\\AIScooter\\jsons_faces\\'


# This loop orders AWS face recognition results for all images in a given directory
# this task has been completed and the dataset uploaded
# dictionary of AI results is returned
for n, file in enumerate(os.listdir(dir_img)):
    send_image(dir_img, dir_json, file)
    print(n, " " + file)


'''
# This loop searches returned jsons for high confidence face recognition results
# Rekognition jsons order found faces confidence from highest to lowest, descending order down
for n, file in enumerate(os.listdir(dir_jsons)):
    f = open(dir_jsons + file, "r")  # r is read only
    face_dict = json.loads(f.read())
    # if FaceDetails obj has Confidence, then a face is detected, otherwise scrap the img
    # Assuming stable struct for each generated face, print the embedded confidence
    # if list is empty, skip
    # Rekognition minimum confidence threshold is 60%
    try:
        # if a Confidence parameter is detected, there is a face at at least 60% confidence
        # else if there is no confidence keyword, there will be an error meaning file should be deleted
        if(face_dict["FaceDetails"][0]["Confidence"] > 0):
            pass
    except:
        # close before deletion
        f.close()
        # delete non-face image
        os.remove(dir_imgs + file.replace(".json", ""))
        # delete non-face json
        os.remove(dir_jsons + file)
        #pass    # instead of nested ifs, just skip if error since "Confidence" keyword doesn't exist
'''