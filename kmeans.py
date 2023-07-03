import random
from collections import namedtuple
from math import sqrt


Point = namedtuple("Point", ("coords", "n", "ct"))
Cluster = namedtuple("Cluster", ("points", "center", "n"))


def kmeans(points: list[Point], k: int, min_diff: float = 1e-6) -> list[Cluster]:
    """Assign points to k clusters"""

    clusters = [Cluster([point], point, point.n) for point in random.sample(points, k)]

    while True:
        point_lists = _redistribute_points(points, clusters, k)
        diff = _calculate_diff(clusters, point_lists, k)

        if diff < min_diff:
            break

    return clusters


def _euclidean_distance(p1: Point, p2: Point) -> float:
    return sqrt(sum((p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)))


def _redistribute_points(points: list[Point], clusters: list[Cluster], k: int) -> list[list[Point]]:
    point_lists: list[list[Point]] = [[] for i in range(k)]

    for point in points:
        smallest_distance = float("Inf")
        for i in range(k):
            distance = _euclidean_distance(point, clusters[i].center)
            if distance < smallest_distance:
                smallest_distance = distance
                index = i
        point_lists[index].append(point)
    return point_lists


def _calculate_diff(clusters: list[Cluster], point_lists: list[list[Point]], k: int) -> float:
    diff: float = 0

    for i in range(k):
        old = clusters[i]
        center = _calculate_center(point_lists[i], old.n)
        new = Cluster(point_lists[i], center, old.n)
        clusters[i] = new
        diff = max(diff, _euclidean_distance(old.center, new.center))

    return diff


def _calculate_center(points: list[Point], n: int) -> Point:
    vals = [0.0] * n
    plen = 0
    for point in points:
        plen += point.ct
        for i in range(n):
            vals[i] += point.coords[i] * point.ct
    return Point([(v / plen) for v in vals], n, 1)
