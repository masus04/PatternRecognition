'''
Created on 23.02.2016

@author: Masus04
'''

import csv
import numpy
from scipy.spatial import distance

def buildClusters(k):
    """ use this method to perform the clustering algorithm """
    trainingList = readCSV('train.csv')
    means = initMeans(k, trainingList)
    clusters = growClusters(means, trainingList)

    # print clusters
    for i in range(len(clusters)):
        print("size of cluster%s: %s" %(i, len(clusters[i])))
        
    means = recalculateMeans(clusters)
    clusters = growClusters(means, trainingList)

    # print clusters
    for i in range(len(clusters)):
        print("size of cluster%s: %s" %(i, len(clusters[i])))

    return clusters

def readCSV(file):
    """ read input, store each vector in a row """
    print('reading ' + file)
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        readList = []
        for row in reader:
            readList.append(numpy.array([float(x) for x in row[1:]]))
    print("reading complete")
    return readList

def initMeans(k, lst):
    """ find the initial k mean vectors for clustering """
    # first mean in the middle
    means = [numpy.mean(numpy.array(lst), axis=0)]
    print("initialising mean vectors. middle mean vector length: %s" % len(means[0]))
    for i in range(k-1):
        distances = [ (sum((distance.cdist([candidate], means))[0]))/len(means) for candidate in lst]
        maxDistance = max(distances)
        print("distance to other means: %s" %maxDistance)
        index = distances.index(maxDistance)
        candidate = list(lst)[index]
        means.append(candidate)
    print("initialisation complete. number of mean vectors: %s" %(len(means)))
    return means

def growClusters(means, trainingList):
    print("populating clusters")
    clusters = [[mean] for mean in means]
    for candidate in trainingList:
        distances = [distance.euclidean(candidate, mean) for mean in means]
        mindistance = min(distances)
        clusters[distances.index(mindistance)].append(candidate)
    return clusters

def recalculateMeans(clusters):
    return [numpy.mean(numpy.array(cluster)) for cluster in clusters]