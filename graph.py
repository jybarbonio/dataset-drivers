from sklearn import datasets
import numpy as np

iris = datasets.load_iris()
# split it in features and labels
X = iris.data
Y = iris.target

print(X, Y)

