'''
Created on 23.02.2016

@author: Masus04
'''
import csv
import math
import time

# timer
startTime = time.time()
blackThreshold = 0

""" X the List of images:
X[i]: the image i
X[i][j]: the row j of image i
X[i][j][k]: the pixel k of row j of image i
"""
def getImages(lst):
    X = []
    for row in [x[1:] for x in lst]:
        matrix = []
        for i in range(28):
            matrix.append([int(x) for x in row[i * 28:(i + 1) * 28]])
        X.append(matrix)
    return X


# returns the ratio of non white pixels in left vs in right half of the image
def leftRight(image):
    leftScore = 0
    rightScore = 0

    for row in image:
        for pixel in row[:14]:
            if pixel > blackThreshold:
                leftScore += 1

        for pixel in row[14:]:
            if pixel > blackThreshold:
                rightScore += 1

    return float(leftScore) / float(rightScore)


# returns the ratio of non white pixels in top vs bottom half of the image
def upDown(image):
    upScore = 0
    downScore = 0

    for row in image[:14]:
        for pixel in row:
            if pixel > blackThreshold:
                upScore += 1

    for row in image[14:]:
        for pixel in row:
            if pixel > blackThreshold:
                downScore += 1

    return float(upScore) / float(downScore)


def notWhite(image):
    total = 0

    for row in image:
        for pixel in row:
            if pixel > blackThreshold:
                total += 1

    return total


def upRight_DownLeft(image):
    upperRightScore = 0
    lowerLeftScore = 0

    for i in range(len(image[0])):
        for pixel in image[i][i:]:
            if pixel > blackThreshold:
                upperRightScore += 1

        for pixel in image[i][:i]:
            if pixel > blackThreshold:
                lowerLeftScore += 1

    """ TODO: Test this method & call it"""
    return float(upperRightScore) / float(lowerLeftScore)


def upLeft_DownRight(image):
    upperLeftScore = 0
    lowerRightScore = 0

    l = len(image[0])

    for i in range(l):
        for pixel in image[i][l - i:]:
            if pixel > blackThreshold:
                upperLeftScore += 1

        for pixel in image[i][:l - i]:
            if pixel > blackThreshold:
                lowerRightScore += 1

    """ TODO: Test this method & call it"""
    return float(upperLeftScore) / float(lowerRightScore)


def predict(value, neighbours, distanceFunction):
    # the list of k nearest neighbours, ordered by distance (linked list?)
    nearest = [[100000, i] for i in range(neighbours)]

    # calculate nearest neighbours
    for candidate in trainingData:
        nearest = sorted(nearest)
        distance = distanceFunction(value, candidate[1])
        if (distance < nearest[neighbours - 1][0]):
            nearest.pop()  # [nearest = :neighbours-1]
            nearest.append([distance, candidate])

    # determine class
    occ = [0 for i in range(10)]
    for n in nearest:
        occ[n[1][0]] += 1

    # return nearest neighbour of majority
    # get indices for all majority classes
    maxValues = [i for i, x in enumerate(occ) if x == max(occ)]

    # choose the nearest class that is part of the majority
    for n in nearest:
        if n[1][0] in maxValues:
            return n[1][0]

    return occ.index(max(occ))


# returns the euclidean distance between two points (lists)
def euclidean(a, b):
    result = 0
    for i in range(min(len(a), len(b))):
        result += (a[i] - b[i]) ** 2
    return math.sqrt(result)


def manhattan(a, b):
    result = 0
    for i in range(min(len(a), len(b))):
        result += a[i] - b[i]
    return result


# read input
print('reading input')
with open('train.csv') as csvfile:
    reader = csv.reader(csvfile)
    trainingList = []
    for row in reader:
        trainingList.append(row)

""" Y the class labels for the training set """
Y = [int(x[0]) for x in trainingList]

X = getImages(trainingList)

""" print image X[0]
for x in X[0]:
	print(x)
"""

""" trainingData the list of vectors containing y, x1, x2 """
print('computing training data')
trainingData = [[Y[t], [leftRight(X[t]), upDown(X[t]), upLeft_DownRight(X[t]), upRight_DownLeft(X[t])]] for t in
                range(len(X))]

""" \\\ END OF TRAINING /// """

""" optimise training data """
# does not make any sense with an accuracy of about 50%..

""" make a prediction """


def testAcuracy(neighbours, testSize, distanceFunction):
    # read input
    with open('test.csv') as csvfile:
        reader = csv.reader(csvfile)
        testList = []
        for row in reader:
            testList.append([int(r) for r in row])

    testImages = getImages(testList)
    testY = [t[0] for t in testList]
    testData = [[testY[t], [leftRight(testImages[t]), upDown(testImages[t]), upLeft_DownRight(testImages[t]),
                            upRight_DownLeft(testImages[t])]] for t in range(testSize)]

    predictions = [predict(d[1], neighbours, distanceFunction) for d in testData[:testSize]]

    """ DEBUGGING """

    accuracyScore = 0
    for i in range(testSize):
        if testY[i] == predictions[i]:
            accuracyScore += 1
        # print(str(testY[i]) + ' || ' + str(predictions[i]))

    return float(accuracyScore) / float(testSize)


# calculate accuracy
eucAccuracies = []
manAccuracies = []
for i in range(1, 16, 2):
    # test the first 100 test values each to speed up computation.
    eucAcc = testAcuracy(i, 100, euclidean)
    manAcc = testAcuracy(i, 100, manhattan)
    print('Euclidean Accuracy: %s for %s neighbours' % (eucAcc, i))
    print('Manhattan Accuracy: %s for %s neighbours' % (manAcc, i))

    eucAccuracies.append([eucAcc, i])
    manAccuracies.append([manAcc, i])

print('max accuracy: %s with %s neighbours' % (max(eucAccuracies)[0], max(eucAccuracies)[1]))
print('max accuracy: %s with %s neighbours' % (max(manAccuracies)[0], max(manAccuracies)[1]))

# timer
print('Execution time: ' + str(int(time.time() - startTime)) + 's')
