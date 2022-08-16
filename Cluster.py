import numpy as np
from matplotlib import pyplot as plt
import random
import csv
import operator
import sys
sys.path.append("..")
from Statistics import PCA

class KMEANS(object):
    color=['green','red','blue','yellow','purple']
    def __init__(self,data,num):
        self.num=num
        if type(data)==str:
            self.readcsv(data)
        else:
            self.dataMatrix=np.array(data)
        self.elements=[]
        self.names=[]
        self.n=np.size(self.dataMatrix,axis=0)
        self.m=np.size(self.dataMatrix,axis=1)
        self.belong=[0 for col in range(self.n)]
        
    def readcsv(self,path):
        temMatrix=[]
        with open(path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            self.elements = next(reader)[1:]

            for row in reader:
                self.names.append(row[0])
                temMatrix.append(list(map(lambda x: float(x), row[1:])))
        
        self.dataMatrix=np.array(temMatrix)


    def initCenter(self):
        n=np.size(self.dataMatrix,axis=0)
        self.center=[self.dataMatrix[i].tolist() for i in random.sample(range(0,n), self.num)]

    def selectCneter(self,point):
        selectedDis,selectedNum=2147483647,0
        for i,center in enumerate(self.center):
            dis=0
            for j in range(self.m):
                dis+=(center[j]-point[j])**2
            if selectedDis>dis:
                selectedNum=i
                selectedDis=dis
        return selectedNum

    def getNewCenter(self):
        newCenter=[[0 for row in range(self.m)] for col in range(self.num)]
        pointNum=[0 for col in range(self.num)]
        for i in range(self.n):
            for j in range(self.m):
                newCenter[self.belong[i]][j]+=self.dataMatrix[i][j]
            pointNum[self.belong[i]]+=1
        self.center=[[row/pointNum[i] for row in col] for i,col in enumerate(newCenter)]
            
    def startIter(self):
        self.initCenter()
        lastCenter=[]
        while not operator.eq(lastCenter,self.center):
            
            lastCenter=self.center
            for i,point in enumerate(self.dataMatrix):
                self.belong[i]=self.selectCneter(point)
            self.getNewCenter()

    def plot(self):
        plt.figure(figsize=(10, 10), dpi=100)
        if self.m>2:
            temPCA=PCA(self.dataMatrix,2,1)
            point=temPCA.startCal()[1]
        else:
            point=self.dataMatrix.tolist()
        for i in range(len(point)):
                plt.scatter(point[i][0],point[i][1], marker = 'o',color = KMEANS.color[self.belong[i]], s = 40)
        plt.show()