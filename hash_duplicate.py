import os
import time
import dhash
import cv2
import numpy as np
from PIL import Image

from skimage.metrics import structural_similarity as ssim
from joblib import Parallel, delayed

from PIL import Image, ImageFile, ImageOps
ImageFile.LOAD_TRUNCATED_IMAGES = True



'''
Program Purpose:
    to truncate scooter rider images into simple hash values that can be compared
    to filter out duplicates. A file path can be specified where images within will
    be iterated through
'''

# given a file, hashes that file and returns the hash value
def open_directory_as_hash(dir, file):
    f = os.path.join(dir, file)
    # checking if it is a file, otherwise ignore
    if os.path.isfile(f):
        img = Image.open(f)
        # elem tuple joins a file directory and its generated hash
        return ([file, hash_img(img)])
    
# hash comparison of a sorted list, via dhash deleting duplicates
def compare_exacthash(list_hash, dir_img, dir_gcloud):
    list_duplicates = []

    # since list is sorted, check 5 spots ahead if current index has a hash duplicate, mark for ignore/delete
    for c in range(0, len(list_hash)):
        # first conditional avoids hash list overflow
        # second conditional checks if diff bits between current hash and +1 ahead
        #   if different bits < 3 then they're effectively duplicates, so delete
        lookahead = c + 1
        while(lookahead < len(list_hash) and int(list_hash[c][1], 16) == int(list_hash[lookahead][1], 16)):
            # append the duplicate filename
            list_duplicates.append(os.path.join(dir_img, list_hash[lookahead][0]))
            lookahead += 1

    for f in list_duplicates:
        if os.path.exists(f):
            print("deleting: ", f)
            os.remove(f)

            #os.remove(dir_gcloud + os.path.basename(f) + "_detected_label.json")
            #os.remove(dir_gcloud + os.path.basename(f) + "_detected_logo.json")
            #os.remove(dir_gcloud + os.path.basename(f) + "_detected_text.json")
        else:
            print("Already deleted")

# hash comparison for hamming distance
# bit difference of 1 to 3 are confidently duplicates, 4-5 creates false positives
def compare_hamming_hash(list_hash, dir_img, dir_gcloud):
    list_nearduplicates = []

    for c in range(0, len(list_hash)):
        lookahead = c + 1
        while(lookahead < len(list_hash)):
            # if differing hash bits b/w images is < 4, they're effectively duplicates
            if (diffhash(int(list_hash[c][1], 16), int(list_hash[lookahead][1], 16)) < 4):
                # append the duplicate filename
                list_nearduplicates.append(os.path.join(dir_img, list_hash[lookahead][0]))
            lookahead += 1

    for f in list_nearduplicates:
        if os.path.exists(f):
            print("deleting: ", f)
            os.remove(f)

            #os.remove(dir_gcloud + os.path.basename(f) + "_detected_label.json")
            #os.remove(dir_gcloud + os.path.basename(f) + "_detected_logo.json")
            #os.remove(dir_gcloud + os.path.basename(f) + "_detected_text.json")
        else:
            print("Already deleted")

def compare_mse_ssim(list_files, dir_img, dir_gcloud):
    list_nearduplicates = []

    for c in range(0, len(list_files)):
        print("Index: ", c)
        f1 = os.path.join(dir_img, list_files[c][0])
        if os.path.isfile(f1):
            img1 = cv2.imread(f1)
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        for lookahead in range(c + 1, len(list_files)):
            f2 = os.path.join(dir_img, list_files[lookahead][0])
            if os.path.isfile(f2):
                img2 = cv2.imread(f2)
                img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            # resize image-to-be-compared to match orig image dimensions for mse
            h, w = img1.shape
            img2 = cv2.resize(img2, (w, h), cv2.INTER_LINEAR)

            m = mse(img1, img2)
            s = ssim(img1, img2, multichannel=True)
            if(s > 0.78):
                list_nearduplicates.append(f2)

    for f in list_nearduplicates:
        if os.path.exists(f):
            os.remove(f)
        else:
            print("already deleted")

def mse(imgA, imgB):
	# Mean Squared Error between the images is the sum of squared difference b/w the two images
	#   the two images must have the same dimensions (obligatory resizing needed)
	err = np.sum((imgA.astype("float") - imgB.astype("float")) ** 2)
	err /= float(imgA.shape[0] * imgA.shape[1])
	
	# return the MSE, the lower the error/deviation, the more "similar"
	#   the two images are
	return err

# performance timer decorator measuring from initial file parsing, to hashing and sorting 
def runtimer(func):
    def wrapper(dir_img):
        t1 = time.time()
        list = func(dir_img, dir_gcloud)
        t2 = time.time() - t1
        print(f'{func.__name__} took {t2} seconds to complete')
        return list
    return wrapper

# wrapper for open_directory to easily time function performance
@runtimer
def open_dir_as_hash_wrap(dir_img, dir_gcloud):
    # parallelization of image hashing
    list_h = Parallel(n_jobs = -1)(delayed(open_directory_as_hash)(dir_img, file) for file in os.listdir(dir_img))
    # sorts the hash strings

    # sort list by hashes, deleting similarities ahead of each index
    list_h.sort(key = lambda x: x[1])
    return list_h

# pivot subfunction for quick sort, moving list edge elems towards pivots and repeating until sorted
# note since this compares numerical values while hash is a string, this is deprecated unless needed later
def partition(list_h, start, end):
    pivot = list_h[end][1]
    i = start - 1

    for j in range(start, end):
        if list_h[j] <= pivot:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (list_h[i], list_h[j]) = (list_h[j], list_h[i])
 
    # Swap the pivot element with the greater element specified by i
    (list_h[i + 1], list_h[end]) = (list_h[end], list_h[i + 1])
 
    # Return the position from where partition is done
    return i + 1

# For the image param, filter to grayscale
# Downsize to 9x9 square
# Calculate simple row hash for each row, move from left to right
    # output a bit if the next gray value is greater than or equal to the previous one
    # or a 0 bit if it’s less (each 9-pixel row produces 8 bits of output)
# Calculate column hash for each column, move top to bottom
# Concatenate the two 64-bit values together to get the final 128-bit hash
def hash_img(img):
    ImageFile.LOAD_TRUNCATED_IMAGES = True      # explicit, joblib will not consider global scope arg (pre-compile?)
    img = ImageOps.grayscale(img)    
    img = img.resize((9, 9))

    # passed downsized and greyscaled img to dhash generator
    row, col = dhash.dhash_row_col(img, size=8)
    return (dhash.format_hex(row, col))

# returns the amount of bit differences, finds how many 1s there are vs the other
def diffhash(hash1, hash2):
    return bin(hash1 ^ hash2).count('1')

# MAIN METHOD
if __name__ == "__main__":
    dir_img = 'C:\\Users\\John\\Desktop\\AIScooter\\images\\'
    dir_gcloud = 'C:\\Users\\John\\Desktop\\AIScooter\\gcloud\\'
    list_hash = []


    # exact hash duplicate deletion
    list_hash = open_dir_as_hash_wrap(dir_img)
    compare_exacthash(list_hash, dir_img, dir_gcloud)

    # hamming distance hash duplicate deletion
    list_hash = open_dir_as_hash_wrap(dir_img)
    compare_hamming_hash(list_hash, dir_img, dir_gcloud)


    list_files = open_dir_as_hash_wrap(dir_img)
    list_files.sort(key = lambda x: x[0])
    compare_mse_ssim(list_files, dir_img, dir_gcloud)