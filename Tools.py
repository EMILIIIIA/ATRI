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
    return {"names":names,"elements":elements,"data":data}

def minmaxmap(data):
    data=np.array(data).astype(float)
    n = np.size(data, axis=0)
    m = np.size(data, axis=1)
    for i in range(m):
        maxValue = np.max(data[:, i])
        minValue = np.min(data[:, i])
        for j in range(n):
            data[j][i] = (data[j][i]-minValue)/(maxValue-minValue)
    return data


def pointBest2largerBest(data, value):
    data=np.array(data).astype(float)
    n = np.size(data, axis=0)
    m = np.size(data, axis=1)

    for i in range(m):
        temValue = []
        for j in range(n):
            temValue.append(abs(data[j, i]-value))
        maxNum = max(temValue)
        for j in range(n):
            data[j, i] = 1-float(temValue[j])/maxNum
    return data


def smallerBest2largerBest(data, col):
    data=np.array(data).astype(float)
    n = np.max(data[:, col])
    size = np.size(data, axis=0)
    for i in range(size):
        data[i, col] = n-data[i, col]
    return data

def terminalBest2largerBest(data, col, value):
    data=np.array(data).astype(float)
    size = np.size(data, axis=0)
    temValue = []
    for i in range(size):
        temValue.append(abs(data[i, col]-value))
    n = max(temValue)
    for i in range(size):
        data[i, col] = float(temValue[i])/n
    return data