import os
import io
import json
import csv
from joblib import Parallel, delayed

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import requests
from PIL import Image, ImageDraw, ImageFont

def get_azure(file, dir_json, face_client):
    url_azure = 'https://westus.api.cognitive.microsoft.com'

    # convert filename back to url
    url_img = file.replace("http!++", "http://")
    url_img = url_img.replace("+", "/")

    try:
        if os.path.exists(dir_json + file + "_detected_azure" + ".json") == False:
            response = face_client.face.detect_with_url(
                url_img,
                detection_model = 'detection_01',
                recognition_model = 'recognition_04',
                # returnFaceAttributes = 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
            )

            print('Number of faces: {0}'.format(len(response)))
    except:
        print("error getting face json or empty")



def wrap_get_azure(api_key, api_endpoint, dir_img, dir_json):

    face_client = FaceClient(api_endpoint, CognitiveServicesCredentials(api_key))

    url_img = 'https://pbs.twimg.com/media/D--WPvsUcAgP7v2.jpg'
    response = face_client.face.detect_with_url(
        url_img,
        detection_model = 'detection_01',
        recognition_model = 'recognition_04',
    )
    # make dir_json folder for kairos json responses
    if(os.path.isdir(dir_json) == False):
        os.mkdir(dir_json)
    '''
    # parallelized implementation (fast)
    Parallel(n_jobs = -1)(delayed(get_azure)
            (file, dir_json, face_client) for file in os.listdir(dir_img))
    '''

    for file in os.listdir(dir_img):
        get_azure(file, dir_json, face_client)

dir_img = 'C:\\Users\\John\\Desktop\\AIScooter\\imagesS2\\'
dir_json = 'C:\\Users\\John\\Desktop\\AIScooter\\imagesS2_azure\\'

# your access .csv may have a different name
with open('credentials_azure.csv', 'r') as input:
    next(input)
    rd = csv.reader(input)
    for line in rd:
        api_key = line[0]
        api_endpoint = line[1]

wrap_get_azure(api_key, api_endpoint, dir_img, dir_json)