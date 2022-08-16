import numpy as np
import csv


def readcsv(path):
    temMatrix = []
    with open(path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        elements = next(reader)[1:]
        names=[]
        for row in reader:
            names.append(row[0])
            temMatrix.append(list(map(lambda x: float(x), row[1:])))

    data = np.array(temMatrix)
    return names,elements,data

def minmaxmap(data):
    n = np.size(data, axis=0)
    m = np.size(data, axis=1)
    for i in range(m):
        maxValue = np.max(data[:, i])
        minValue = np.min(data[:, i])
        for j in range(n):
            data[j][i] = (data[j][i]-minValue)/(maxValue-minValue)
    return data


def pointBest2largerBest(data, value):
    n = np.size(data, axis=0)
    m = np.size(data, axis=1)
    temValue = []
    for i in range():
        for j in range(n):
            temValue.append(abs(data[j, i]-value))
        maxNum = max(temValue)
        for j in range(n):
            data[j, i] = 1-float(temValue[i])/maxNum
    return data


def smallerBest2largerBest(self, col):
    n = np.max(self.dataMatrix[:, col])
    size = np.size(self.dataMatrix, axis=0)
    for i in range(size):
        self.dataMatrix[i, col] = n-self.dataMatrix[i, col]


def terminalBest2largerBest(self, col, value):
    size = np.size(self.dataMatrix, axis=0)
    temValue = []
    for i in range(size):
        temValue.append(abs(self.dataMatrix[i, col]-value))
    n = max(temValue)
    for i in range(size):
        self.dataMatrix[i, col] = float(temValue[i])/n
