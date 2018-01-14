from gensim import corpora, models, similarities, matutils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument 
from six import iteritems
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import numpy as np

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import os
import tempfile

thing = open('datasets/rapz')
texts = [[word for word in line.lower().split()[1:]] for line in thing]
print(texts[2039])
print("avg text length: " + str(float(sum([len(' '.join(i)) for i in
                                       texts])/len(texts))))

query = ' '.join(texts[2039])
query = query.lower().split()

thing = open('datasets/rapz')
model = Doc2Vec(size=1000, window=4, min_count=0, workers=4)
docs = [TaggedDocument(line.lower().split()[1:], [line.lower().split()[0]]) for line in thing]
model.build_vocab(docs)
model.train(docs, total_examples=model.corpus_count, epochs=model.iter)

vec_query = model.infer_vector(query)
sims = model.docvecs.most_similar([vec_query])
print(sims)
dv_arr = StandardScaler().fit_transform(np.asarray(model.docvecs))
db = DBSCAN(eps=0.3, min_samples=10).fit(dv_arr)

core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)

import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = dv_arr[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = dv_arr[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.show()

