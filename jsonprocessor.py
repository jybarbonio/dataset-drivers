import os
import json
import re


'''
given a directory such as the gcloud or image files, will load all json elements in file
'''
def load_directory(dir_path):
    pass

'''
takes a json file path and loads it, subfunction for load_directory
'''
def load_json(file_path):
    file = validate(file_path)

    if(file == None):
        print("fail")
    else:
        print("pass")
        print(json.dumps(file, indent=2))

'''
validates if a json file is valid, if not then returns a None value to prevent its addition to the pool
'''
def validate(file):
    with open(file) as f:
        try:
            return json.load(f)  # open the json file
        except ValueError as e:
            return None

if __name__ == "__main__":
    load_json("gcloud/gcloud/http!++pbs.twimg.com+media+D0yx7u2U8AAJr4d.jpg_detected_text.json")