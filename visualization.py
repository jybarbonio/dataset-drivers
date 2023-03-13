from sklearn import datasets
import cv2 as cv
import numpy as np

iris = datasets.load_iris()
# split it in features and labels
X = iris.data
Y = iris.target

print(X, Y)

