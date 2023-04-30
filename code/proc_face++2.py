import base64
import requests
import json

def facedetect():
    facepp_url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
    facepp_url2 = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    facepp_url3 = 'https://api-cn.faceplusplus.com/facepp/v3/face/analyze'
    imagepp_url = 'https://api-cn.faceplusplus.com/imagepp/beta/detectsceneandobject'

    api_key = 'cS4u_sfmqFjxII6YO_tFsBoT7ghPhZC4'
    api_secret = 'srxlweTo1sWccWEIEZZfXgDaK8isfloO'
    img64 = 'https://i.postimg.cc/3ww2WHBT/crop.jpg'

    body = {
            'api_key': 'cS4u_sfmqFjxII6YO_tFsBoT7ghPhZC4',
            'api_secret': 'srxlweTo1sWccWEIEZZfXgDaK8isfloO',
            'image_url' : 'https://i.postimg.cc/tJqwXnH9/1dd4f4cc5083ecdc9a64f7bff2e86264.jpg',
            'return_attributes' : 'gender,age,ethnicity,smiling,headpose,facequality,blur,eyestatus,emotion,beauty,mouthstatus,eyegaze,skinstatus,nose_occlusion,chin_occlusion,face_occlusion'
    }

    r = requests.post(facepp_url2, body)
    pretty_data = json.dumps(r.json(), indent=2)
    print(pretty_data)

def faceanalyze():
    facepp_url = 'https://api-cn.faceplusplus.com/facepp/v3/face/analyze'

    api_key = 'cS4u_sfmqFjxII6YO_tFsBoT7ghPhZC4'
    api_secret = 'srxlweTo1sWccWEIEZZfXgDaK8isfloO'
    img64 = 'https://i.postimg.cc/3ww2WHBT/crop.jpg'
    img642 = 'https://i.postimg.cc/tJqwXnH9/1dd4f4cc5083ecdc9a64f7bff2e86264.jpg'

    body = {
            'api_key': 'cS4u_sfmqFjxII6YO_tFsBoT7ghPhZC4',
            'api_secret': 'srxlweTo1sWccWEIEZZfXgDaK8isfloO',
            'face_tokens' : 'ee6425d212f47955ebddfeaacbb7ef3c',
            'return_landmark' : '2',
            'image_url' : 'https://i.postimg.cc/tJqwXnH9/1dd4f4cc5083ecdc9a64f7bff2e86264.jpg',
            'attributes' : 'ethnicity'
    }

    r = requests.post(facepp_url, body)
    pretty_data = json.dumps(r.json(), indent=2)
    print(pretty_data)

facedetect()
faceanalyze()