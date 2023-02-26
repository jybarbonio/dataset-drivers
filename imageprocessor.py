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

@runtimer
def quicksort(list_hash, start, end):
    if start >= end:
        return
    
    p = partition(list_hash, start, end)
    quicksort(list_hash, start, p - 1)
    quicksort(list_hash, p + 1, end)

    return list_hash

# pivot subfunction for quick sort, moving list edge elems towards pivots and repeating until sorted
def partition(list_hash, start, end):
    pivot = list_hash[start]
    low = start + 1
    high = end

    while True:
        while low <= high and list_hash[high] >= pivot:
            high -= 1
        while low <= high and list_hash[low] <= pivot:
            low += 1

        if low <= high:
            list_hash[low], list_hash[high] = list_hash[high], list_hash[low]
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


def open_image(file):
    # import and create image
    return Image.open(file)
    # show the image
    # img.show()

@runtimer
def open_directory(dir):
    count_pass = 0
    count_fail = 0
    list_fail = []
    list_hashes = []

    for count, file in enumerate(os.listdir(dir)):
    # for file in os.listdir(dir):
    
        # checking if it is a file
        if os.path.isfile((dir, file)):
            # print(count, " " + f)
            img = open_image(f)
            # print(hashify(img))
            list_hashes.append(hashify(img))
        else:
            list_fail.append((dir, file))
            f = os.path.join(dir, file)

    return list_hashes

if __name__ == "__main__":
    # open_image("images/images/http!++pbs.twimg.com+media+D0yx7u2U8AAJr4d.jpg")
    imghashes = open_directory('C:\\Users\\John\\Desktop\\AIScooter\\images\\images')
    imghashes = quicksort(imghashes, 0, len(imghashes) - 1)
    print(imghashes)