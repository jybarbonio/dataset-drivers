import os
import time
import dhash

from PIL import Image, ImageFilter, ImageFile, ImageOps
ImageFile.LOAD_TRUNCATED_IMAGES = True

'''
Program Purpose:
    to truncate scooter rider images into simple hash values that can be compared
    to filter out duplicates. A file path can be specified where images within will
    be iterated through

To-Do:
    GUI and saving tuples of filepaths w/ associated generated hash values
    hash lookup for faster deletion/marking of duplicates
    integrating quicksort to be called for every new hash added or alternative sort such as a heap
    parallel computing
    
Pipeline is currently:
    open_directory, open_image -> quicksort -> partition -> return runtime and list
'''

# performance timer decorator measuring from initial file parsing, to hashing and sorting 
def runtimer(func):
    def wrapper(dir):
        t1 = time.time()
        list = func(dir)
        t2 = time.time() - t1
        print(f'{func.__name__} took {t2} seconds to complete')
        return list
    return wrapper

# quicksort the algorithm so duplicate testing is near index
def quicksort(list_hash, start, end):
    if start >= end:
        return
    
    p = partition(list_hash, start, end)
    quicksort(list_hash, start, p - 1)
    quicksort(list_hash, p + 1, end)

    return list_hash

# pivot subfunction for quick sort, moving list edge elems towards pivots and repeating until sorted
def partition(list_hash, start, end):
    pivot = list_hash[start][1]
    low = start + 1
    high = end

    while True:
        while low <= high and list_hash[high][1] >= pivot[1]:
            high -= 1
        while low <= high and list_hash[low][1] <= pivot[1]:
            low += 1

        if low <= high:
            list_hash[low][1], list_hash[high][1] = list_hash[high][1], list_hash[low][1]
        else:
            break

    list_hash[start], list_hash[high] = list_hash[high], list_hash[start]

    return high

# For the image param, filter to grayscale
# Downsize to 9x9 square
# Calculate simple row hash for each row, move from left to right
    # output a bit if the next gray value is greater than or equal to the previous one
    # or a 0 bit if it’s less (each 9-pixel row produces 8 bits of output)
# Calculate column hash for each column, move top to bottom
# Concatenate the two 64-bit values together to get the final 128-bit hash
def hashify(img):
    img = ImageOps.grayscale(img)
    img = img.resize((9, 9))

    # passed downsized and greyscaled img to dhash generator
    row, col = dhash.dhash_row_col(img)
    
    # print(dhash.format_hex(row, col))
    return (dhash.format_hex(row, col))

# hash comparison of a sorted list, via dhash using hamming distance
# linear search but list is sorted so only immediate neighbors are checked
# bit difference of 1 or 2 are confidently duplicates, 4-5 creates false positives
def comparehash(fpath, list_hash):
    list_duplicates = []

    # since list is sorted, check 5 spots ahead if current index has a hash duplicate, mark for ignore/delete
    for c, h in enumerate(list_hash):
        # proximity checks the 4 hashes ahead of h for similarity
        print(c, h)
        lkh = c + 1     # look aheadof index for duplicates

        # first conditional avoids hash list overflow, second conditional compares bit diffs
        # second conditional checks if diff bits between current hash and +1 ahead
        #   if different bits < 2 then they're effectively duplicates, so delete
        while(lkh < len(list_hash) 
              and os.path.isfile(fpath + "\\" + list_hash[lkh][0]) 
              and diffhash(int(h[1], 16), int(list_hash[lkh][1], 16)) < 2):
            print("adding to delete list: ", list_hash[lkh][0])
            list_duplicates.append(list_hash[lkh])
            os.remove(fpath + "\\" + list_hash[lkh][0])
            lkh += 1

    return list_duplicates

# returns the amount of bit differences, finds how many 1s there are vs the other
def diffhash(hash1, hash2):
    return bin(hash1 ^ hash2).count('1')

def open_image(file):
    # import and create image
    return Image.open(file)
    # show the image
    # img.show()

@runtimer
def open_directory(dir):
    list_hashfile = []

    # for count, file in enumerate(os.listdir(dir)):
    for file in os.listdir(dir):
        f = os.path.join(dir, file)
        # checking if it is a file
        if os.path.isfile(f):
            # print(count, " " + f)
            img = open_image(f)
            # print(file, hashify(img))
            # elem tuple joins a file directory and its generated hash
            list_hashfile.append((file, hashify(img)))
        else:
            f = os.path.join(dir, file)
            print("Failed to load file: ", f)

    return list_hashfile

if __name__ == "__main__":
    fpath = 'C:\\Users\\John\\Desktop\\AIScooter\\imagesT\\imagesT'
    list_hashfile = open_directory(fpath)
    
    # for hf in list_hashfile:
        # print(hf)
        # print(hf[0], " ", hf[1])

    dct_dups = comparehash(fpath, list_hashfile)

    for d in dct_dups:
        print("deleted: ", d[0])