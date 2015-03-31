import numpy as np
import scipy.spatial

X = np.array([[1,2], [1,2], [3,4],[6,7],[6,7]])
dist_matrix = scipy.spatial.distance.pdist(X)
a=scipy.spatial.distance.squareform(dist_matrix)
np.fill_diagonal(a, np.inf)
b = a.argmin(axis=0)

#mymin = np.min(a)

print a
min_positions = np.where(a == a.min())

print min_positions
#print b
