import hdbscan

import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score

def get_hdbscan_cluster_index(gdf, min_cluster_size=5, min_samples=None, metric=None):
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples, metric='haversine')
    X = np.array(list(map(list, np.array(gdf.loc[:, ['latitude', 'longitude']]))))
    clusterer.fit(X)
    return clusterer.labels_, X


def get_partial_silhouette_score(labels, X):
    silhouette_filter = np.random.randint(0, X[labels != -1].shape[0], 10000)
    result = silhouette_score(
        X[labels != -1][silhouette_filter],
        labels[labels != -1][silhouette_filter]
    )
    return result