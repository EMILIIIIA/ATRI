from traceback import print_tb
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
    data=np.mat(data).astype(float)
    if np.size(data,axis=0)==1:
        data=data.T
    n = np.size(data, axis=0)
    m = np.size(data, axis=1)
    for i in range(m):
        maxValue = np.max(data[:,i])
        minValue = np.min(data[:,i])
        for j in range(n):
            data[j,i] = (data[j,i]-minValue)/(maxValue-minValue)
    return data

def rmsmap(data):
    data=np.array(data).astype(float)
    n = np.size(data, axis=0)
    m = np.size(data, axis=1)
    rms=np.array([])
    for i in range(m):
        sumsquare=0
        for j in range(n):
            sumsquare+=data[j][i]**2
        sumsquare=sumsquare**0.5
        rms=np.append(rms,sumsquare)
    for i in range(m):
        for j in range(n):
            data[j][i] /= rms[i]
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


def smallerBest2largerBest(data):
    data=np.array(data).astype(float)
    n = np.size(data, axis=0)
    m = np.size(data, axis=1)
    for i in range(m):
        maxNum = np.max(data[:, i])
        for j in range(n):
            data[j, i] = maxNum-data[j, i]
    return data

def terminalBest2largerBest(data, value):
    data=np.array(data).astype(float)
    n = np.size(data, axis=0)
    m = np.size(data, axis=1)
    for i in range(m):
        temValue = []
        for j in range(n):
            temValue.append(abs(data[j, i]-value))
        maxNum = max(temValue)
        for j in range(n):
            data[j, i] = float(temValue[j])/maxNum
    return data