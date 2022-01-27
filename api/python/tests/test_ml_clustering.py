import pytest
from sklearn.cluster import KMeans  # type: ignore

from indigo.ml.clustering import (
    clustering,
    kmeans_clustering,
    split_coords_by_clusters,
)


@pytest.mark.parametrize(
    "args, kwargs, expecting",
    [
        (
            [[[1, 1], [2, 1], [1, 0], [4, 7], [3, 5]]],
            {
                "n_clusters": 2,
                "assign_labels": "discretize",
                "random_state": 0,
            },
            [0, 0, 0, 1, 1],
        ),
        (
            [[[1], [2], [1], [4], [3]]],
            {
                "n_clusters": 2,
                "assign_labels": "discretize",
                "random_state": 0,
            },
            [0, 0, 0, 1, 1],
        ),
    ],
)
def test_clustering_spectral(args, kwargs, expecting):
    assert clustering(*args, **kwargs) == expecting


@pytest.mark.parametrize(
    "args, kwargs, expecting",
    [
        (
            [[[1, 1], [2, 1], [4, 7], [3, 5]]],
            {"n_clusters": 2, "random_state": 0},
            ([0, 0, 1, 1], [[1.5, 1.0], [3.5, 6.0]]),
        ),
    ],
)
def test_kmeans_clustering(args, kwargs, expecting):
    assert kmeans_clustering(*args, **kwargs) == expecting


@pytest.mark.parametrize(
    "coords, clusters, n_clusters, expected",
    [
        (
            [[1, 1], [4, 7], [2, 1], [3, 5]],
            [0, 1, 0, 1],
            2,
            [[[1, 1], [2, 1]], [[4, 7], [3, 5]]],
        )
    ],
)
def test_split_coords_by_clusters(coords, clusters, n_clusters, expected):
    assert split_coords_by_clusters(coords, clusters, n_clusters) == expected
