from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import numpy as np
import math
import json
import matplotlib.pyplot as plt

data = json.load(open('../datasets/songData.json'))

combineData = []
order = []

for i in data:
  combineData.append(i.get('annotations', '') + i['lyrics'])
  order.append(i['id'])

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
])   

X = pipeline.fit_transform(combineData).todense()

pca = PCA(n_components=2).fit(X)
data2D = pca.transform(X)
plt.scatter(data2D[:,0], data2D[:,1])
plt.show()


#KNN
best = {}
test = 6969 # Set this to your desired song id
lowest = np.inf

def euclideanDist(x, xi):
    d = 0.0
    for i in range(len(x)-1):
        d += pow((float(x[i])-float(xi[i])),2)  #euclidean distance
    d = math.sqrt(d)
    return d

for i in range(len(data2D)):
  dist = euclideanDist(data2D[i],data2D[test])
  best[i] = dist
sorted_x = sorted(best, key=best.get)[:5]

for x in sorted_x:
  print(order[x])