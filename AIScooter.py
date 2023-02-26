import os
import json
import re

# gcloud_Share_Bird_Lime_Spin_Bolt_gruv_Lyft_Sherpa_VeoRide_Wheels_Taxify_Jump_RazorUSA_Scoot Networks_Skip_all
path_metadata = r'C:\Users\John\Desktop\AIScooter\gcloud\gcloud'
path_img = r'C:\Users\John\Desktop\AIScooter\images\images'

list_metadata = os.listdir(path_metadata)

# load directory, also verifies json files are valid
def load_directory():
    count_pass = 0
    count_fail = 0
    list_fail = []

    # for file in enumerate(list_metadata):
    for count, file in enumerate(list_metadata):
        # print(count)
        file = "gcloud/gcloud/" + file
        value = validate(file)

        if(value == None):
            count_fail += 1
            list_fail.append(file)
        else:
            count_pass += 1
            # f_contents = f.load()
            # print(f_contents,"\n")        

    print("Passes: ", count_pass, " Fails: ", count_fail)
    print("Failed files:", list_fail)

# validates if json loads, if not then returns none
def validate(file):
    with open(file) as f:
        try:
            return json.load(f)  # open the json file
        except ValueError as e:
            return None

if __name__ == "__main__":
    load_directory()