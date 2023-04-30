import os
import json
import time
import glob
import re

import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# read face data in all jsons
def read_ethnicity_kairos(dir_json, dir_figures):
    faces = 0
    face_files = 0
    no_face_files = 0

    list_category = [ 0, 0, 0, 0, 0 ]

    for file in os.listdir(dir_json):
        try:
            #print(file)

            f = open(dir_json + file, "r")
            face_dict = json.loads(f.read())

            if 'images' in face_dict:
                face_files += 1
                # unfortunately it has to be coded like this because of the json layout including non-ethnic data keys
                for person in face_dict['images']:
                    faces += 1
                    list_ethnicity = []

                    list_ethnicity.append(('white', float(json.dumps(person['attributes']['white'], indent=2))))
                    list_ethnicity.append(('asian', float(json.dumps(person['attributes']['asian'], indent=2))))
                    list_ethnicity.append(('black', float(json.dumps(person['attributes']['black'], indent=2))))
                    list_ethnicity.append(('hispanic', float(json.dumps(person['attributes']['hispanic'], indent=2))))
                    list_ethnicity.append(('other', float(json.dumps(person['attributes']['other'], indent=2))))

                    highest = ('', 0)

                    for trait in list_ethnicity:
                        if trait[1] > highest[1] and trait[1] != None:
                            highest = trait
                        
                    if highest[0] == 'white':
                        list_category[0] += 1
                    elif highest[0] == 'asian':
                        list_category[1] += 1
                    elif highest[0] == 'black':
                        list_category[2] += 1
                    elif highest[0] == 'hispanic':
                        list_category[3] += 1
                    elif highest[0] == 'other':
                        list_category[4] += 1
                
            else:
                #print(file, "no faces")
                no_face_files += 1
        except:
            #print("file error or empty")
            no_face_files += 1

    #print("Face Files:", face_files, "No Face Files:", no_face_files, "Total Faces:", faces)

    #for i in list_category:
    #    print(i)

    print("Faces", faces)
    for i in list_category:
        print(i)

    data =  {   
            'Ethnicity' : ['White', 'Asian', 'Black', 'Hispanic', 'Other'],
            'Percentage' : [float(i / 3013.0) for i in list_category]
            }
    bar_colors = ['tab:green', 'tab:red', 'tab:blue', 'orange', 'tab:purple']

    df = pd.DataFrame(data = data, index = data['Ethnicity'], columns = data['Ethnicity'])
    ax = df.plot(kind = 'barh', color = bar_colors)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax = 1.0))
    ax.set_axisbelow(True)
    ax.grid(color='gray', linestyle='dashed')
    barlist = plt.barh(data['Ethnicity'], data['Percentage'])
    i = 0
    for i, p in enumerate(barlist):
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        plt.text((x + width) + 0.045,
                (y + height) - 0.475,
                str("{:.1%}".format(data['Percentage'][i])),
                ha = 'right',
                size = 14
                )


    # color the barsl by carouseling
    for i, bar in enumerate(barlist):
        bar.set_color(bar_colors[i])
        # print(i % len(bar_colors))

    #print([float(i / 3013.0) for i in list_category])

    #plt.ylabel('Ethnicity', fontsize = 24)
    plt.xlabel('Percentage (%)', fontsize = 24)
    plt.xticks(fontsize = 16)   
    plt.yticks(fontsize = 16)

    figure = plt.gcf()
    figure.set_size_inches(12, 7)

    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles[::-1], labels[::-1], loc = "upper right", fontsize = 16)
    plt.margins(x = 0.125, y = 1)
    plt.savefig(dir_figures + 'Demographic Distribution via Kairos.png', dpi = 100, bbox_inches='tight')
    plt.show()

# read face data in all jsons
def read_age_kairos(dir_json, dir_figures):
    faces = 0
    list_age = []

    for c, age in enumerate(range(0, 75)):
        list_age.append(0)

    for file in os.listdir(dir_json):
        try:
            #print(file)

            f = open(dir_json + file, "r")
            face_dict = json.loads(f.read())

            if 'images' in face_dict:
                # unfortunately it has to be coded like this because of the json layout including non-ethnic data keys
                for person in face_dict['images']:
                    faces += 1
                    list_age[person['attributes']['age']] += 1
                
            else:
                pass
                #print(file, "error missing age param")
        except:
            pass
            #print("empty")

    #for c, age in enumerate(list_age):
    #    print(c, " ", age)

    data = {
        'Age Index' : [c for c in range(0, len(list_age))][5:71],
        'Age Percentage' : [float(i / sum(list_age)) for i in list_age][5:71]
    }

    df = pd.DataFrame(data = data, index = data['Age Index'])
    ax = df['Age Percentage'].plot(x = data['Age Index'], y = data['Age Percentage'], kind = 'bar', width = 0.8)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax = 1.0))
    plt.xticks(rotation = 60)
    ax.set_axisbelow(True)
    ax.grid(color='gray', linestyle='dashed')

    #plt.bar(data['Ages'], data['Percentage'], color = 'orange', width = 0.4)
    plt.xlabel("Age Distribution")
    plt.ylabel("Number of Individuals")
    plt.title("Age Distribution Among Ride App Social Media Activity")

    figure = plt.gcf()
    figure.set_size_inches(12, 7)
    plt.legend(loc = "upper right", fontsize = 16)
    plt.savefig(dir_figures + 'Age Distribution via Kairos.png', dpi = 100, bbox_inches='tight')
    plt.show()

def pie_chart(list_data, list_label, dir_figures, name):
    data = np.array(list_data)

    figure = plt.gcf()
    figure.set_size_inches(12, 7)
    plt.pie(data, startangle = 90, labels=list_label, autopct='%1.2f%%', textprops={'fontsize': 16})
    plt.legend(loc = 'lower left', fontsize = 12)
    plt.savefig(dir_figures + name, dpi = 100, bbox_inches='tight')
    plt.show()

def read_kairos_gender(dir_json):
    male = 0
    female = 0
    total = 0
    faces = 0
    c = 0
    
    for f in os.listdir(dir_json):
        if re.match(r'.+detected_kairos.+', f):
            #print(f)
            jf = open(dir_json + f, "r")
            try:
                face_dict = json.loads(jf.read())
                if 'images' in face_dict:
                    # unfortunately it has to be coded like this because of the json layout including non-ethnic data keys
                    for person in face_dict['images']:
                        #print(person['attributes'])
                        if person['attributes']['gender']['type'] == 'F':
                            female += 1
                            faces += 1
                        else:
                            male += 1
                            faces += 1
            except:
                #print("Error: blank or missing category")
                pass
            jf.close()

    print("M:", male, "F:", female, "Faces:", faces, "Total:", total)
    return [male, female]

# reads only the karios detected faces among the 3,195 rekog faces, i.e. 3103 faces present in ~2000 of the images
def read_kairos_rekog_emotion(dir_json, dir_json2):
    list_kairos = []
    list_emotions = [0, 0, 0, 0, 0, 0, 0, 0]
    people = 0


    for f in os.listdir(dir_json):
        result = re.search(r'detected_kairos[0-9]', f)
        if result:
            result_str = '{}'.format(result.group(0))
            result_str = result_str.replace('detected_kairos', '')
            result_index = int(result_str)
            #print(result_str)
        try:
            jf = open(dir_json + f)
            face_dict = json.loads(jf.read())

            if face_dict['images'][0]['attributes'] != None:
                str_t = f.replace('detected_kairos' + result_str, '')
                str_t = str_t.replace('.json', '_detected_face.json')
                list_kairos.append((str_t, int(result_str)))
        except:
            pass

    for i in list_kairos:
        try:
            jf = open(dir_json2 + i[0])
            face_dict = json.loads(jf.read())

            print(face_dict['FaceDetails'][i[1]]['AgeRange'])

        except:
            pass

    print(len(list_kairos))
    for e in list_emotions:
        print(e)

dir_json = 'C:\\Users\\John\\Desktop\\AIScooter\\datasets\\json\\json_exact_hamming_rekog_kairos_bbox\\'
dir_json2 = 'C:\\Users\\John\\Desktop\\AIScooter\\datasets\\json\\json_exact_hamming_rekog_faces\\'
dir_figures = 'C:\\Users\\John\\Desktop\\AIScooter\\datasets\\figures\\'

# setup pie chart kairos quality
p1_data = [3195, 452, 6625, 7423]
p1_labels = ['Unique Face Images', 'Near-Duplicates', 'Non-Faces', 'Duplicates']
p1_savename = 'Dataset Filtering.png'


# setup pie chart gender ratio pie
p2_data = read_kairos_gender(dir_json)
p2_labels = ['Male', 'Female']
p2_savename = 'Gender Ratio.png'

read_ethnicity_kairos(dir_json, dir_figures)

pie_chart(p1_data, p1_labels, dir_figures, p1_savename)
pie_chart(p2_data, p2_labels, dir_figures, p2_savename)

read_age_kairos(dir_json, dir_figures)

read_kairos_rekog_emotion(dir_json, dir_json2)

