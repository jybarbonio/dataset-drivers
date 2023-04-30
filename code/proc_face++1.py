from __future__ import print_function, unicode_literals
from facepplib import FacePP, exceptions
import emoji
import json



def face_detection(app):
    """
    Detect and analyze human faces within the image that you provided.
    """
    print('[Face Detection]')

    img_url = 'https://i.postimg.cc/ZKn2gqG8/http-pbs-twimg-com-media-D-21-Tzx-Xk-AUy-Lek.jpg'
    img_url2 = 'https://i.postimg.cc/TYL4d0vk/1669938770761.jpg'

    img = app.image.get(image_url=img_url2,
                        return_attributes=['ethnicity'])

    print('image', '=', img)
    print('faces_count', '=', len(img.faces))

    for (idx, face_) in enumerate(img.faces):
        print('-', ''.join(['[', str(idx), ']']))
        print('face', '=', face_)
        print('gender', '=', face_.gender['value'])
        print('age', '=', face_.age['value'])
        print('face_rectangle', '=', json.dumps(face_.face_rectangle, indent=4))
        print('ethnicity', '=', face_.ethnicity)
        print('race', '=', face_.race)

if __name__ == "__main__":
    api_key = 'cS4u_sfmqFjxII6YO_tFsBoT7ghPhZC4'
    api_secret = 'srxlweTo1sWccWEIEZZfXgDaK8isfloO'
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    img64 = 'http!++pbs.twimg.com+media+D_21TzxXkAUyLek.jpg'


    try:
        app_ = FacePP(api_key=api_key, api_secret=api_secret, url = 'https://api-cn.faceplusplus.com')

        funcs = [
            face_detection
        ]

        for func in funcs:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            func(app_)

    except exceptions.BaseFacePPError as e:
        print('Error:', e)