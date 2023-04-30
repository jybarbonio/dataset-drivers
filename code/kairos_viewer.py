import os
import json
import cv2
import matplotlib.pyplot as plt
import numpy as np

def get_list(dir_json):
    json_bbox = []

    for file in os.listdir(dir_json):
        try:
            print(file)

            f = open(dir_json + file, "r")
            face_dict = json.loads(f.read())

            if 'images' in face_dict:
                # unfortunately it has to be coded like this because of the json layout including non-ethnic data keys
                for face in face_dict['images']:
                    print(face["transaction"]["topLeftX"])
                    print(face["transaction"]["topLeftY"])
                    print(face["transaction"]["width"])
                    print(face["transaction"]["height"])

                    json_bbox.append([file.replace("_detected_kairos.json", ""),
                                    face["transaction"]["topLeftX"],
                                    face["transaction"]["topLeftY"],
                                    face["transaction"]["width"],
                                    face["transaction"]["height"]
                                    ])
                    
        except:
            print("empty")

    return json_bbox

def open_image(dir_img, list_kairos):
    for i in list_kairos:
        print(i)
        img = cv2.imread(dir_img + i[0])

        # y : y-offset, x : x-offset
        crop_img = img[i[2]:i[2]+i[4], i[1]:i[1]+i[3]]

        # plt.imshow(crop_img)
        cv2.imshow("full", img)
        cv2.imshow("crop", crop_img)
        cv2.destroyAllWindows()

dir_json = 'C:\\Users\\John\\Desktop\\AIScooter\\datasets\\json\\json_exact_hamming_rekog_kairos_FULL\\'
dir_img = 'C:\\Users\\John\\Desktop\\AIScooter\\datasets\\img\\img_exact_hamming_rekog\\'
list_kairos = get_list(dir_json)
open_image(dir_img, list_kairos)
