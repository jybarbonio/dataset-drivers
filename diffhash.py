import dhash

def diffhash():
'''
Convert the image to grayscale
Downsize to a 9x9 square of gray values (or 17x17 for a larger, 512-bit hash)
Calculate the “row hash”: for each row, move from left to right, and output a 1 bit if the next gray value is greater than or equal to the previous one, or a 0 bit if it’s less (each 9-pixel row produces 8 bits of output)
Calculate the “column hash”: same as above, but for each column, move top to bottom
Concatenate the two 64-bit values together to get the final 128-bit hash
'''