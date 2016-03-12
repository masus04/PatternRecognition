'''
Created on 23.02.2016

@author: Masus04
'''
import time
import KMeansClustering

# timer
startTime = time.time()
blackThreshold = 0

KMeansClustering.buildClusters(10)

# timer
print('Execution time: ' + str(int(time.time() - startTime)) + 's')