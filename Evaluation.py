import numpy as np
import matplotlib.pyplot as plt
import csv
import Tools
from math import log

class AHP(object):

    RI = np.array([0, 0 , 0.52, 0.89, 1.12, 1.26, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59])
    def __init__(self,inputMatrix):
        self.matrix=np.array(inputMatrix)
        self.show=True

    def isReciprocalMatrix(self,matrix):
        n=np.size(self.matrix,axis=1)
        for i in range(n):
            for j in range(i):
                if self.matrix[i][j]*self.matrix[j][i]!=1:
                    return False
        return True
        

    def cal(self):

        if not self.isReciprocalMatrix(self.matrix):
            if self.show==True:
                print("评价矩阵有误！")
            return

        n=np.size(self.matrix,axis=1)
        D,V = np.linalg.eig(self.matrix)
        maxEig = max(D).real
        CI = (maxEig-n) / (n-1)
        RI = AHP.RI[n-1]
        CR = CI / RI
        if CR > 0.1:
            if self.show==True:
                print("一致性检验未通过! CR=",CR)
            return
        if self.show==True:
            print("一致性检验通过! CR=",CR)
        
        maxEigVector = V[:, np.argmax(D)].real
        weight = maxEigVector / np.sum(maxEigVector)
        if self.show==True:
            print(weight)
        return weight


class EWM(object):
    def __init__(self,data):
        if type(data)==str:
            self.dataMatrix=Tools.readcsv(data)["data"]
        else:
            self.dataMatrix=np.array(data)
        self.show=True


    def calWeight(self):
        entropy=[]
        matrixSum=np.sum(self.dataMatrix,axis=0)
        n=np.size(self.dataMatrix,axis=1)
        m=np.size(self.dataMatrix,axis=0)
        for i in range(n):
            p=[self.dataMatrix[col][i]/matrixSum[i]+1e-11 for col in range(m)]
            tem=[p[col]*log(p[col]) for col in range(m)]
            
            entropy.append(1-(-1/log(m))*sum(tem))
        entropySum=sum(entropy)
        weight=[(entropy[col])/entropySum for col in range(n)]
        return np.array(weight)

    def cal(self):
        weight=self.calWeight()
        if self.show==True:
            print("权重：",weight)

        res=np.sum(np.multiply(self.dataMatrix,weight),axis=1)
        if self.show==True:
            for i in range(np.size(self.dataMatrix,axis=0)):
                print("结果：",res[i])
        return {"result":res,"weight":weight}



class TOPSIS(object):
    def __init__(self,data):
        if type(data)==str:
            self.data=Tools.readcsv(data)["data"]
        else:
            self.data=np.array(data)

        self.n=np.size(self.data,axis=0)
        self.m=np.size(self.data,axis=1)
        self.show=True
    
    def cal(self):
        self.data=Tools.rmsmap(self.data)
        self.res=np.array([0.0 for col in range(self.n)])
        maxVec=np.max(self.data,axis=0)
        minVec=np.min(self.data,axis=0)
        for i in range(self.n):
            Dimax,Dimin=0,0
            for j in range(self.m):
                Dimax+=(maxVec[j]-self.data[i][j])**2
                Dimin+=(minVec[j]-self.data[i][j])**2
            Dimax**=0.5
            Dimin**=0.5
            self.res[i]=Dimin/(Dimin+Dimax)
        self.res=Tools.minmaxmap(self.res)
        if self.show==True:
            print(self.res)
        return self.res


class EWMTOPSIS(TOPSIS):
    '''论文 Combining Entropy Weight and TOPSIS Method for Information System Selection 中算法的python实现'''

    def cal(self):
        self.data=Tools.rmsmap(self.data)
        self.res=np.array([0.0 for col in range(self.n)])
        maxVec=np.max(self.data,axis=0)
        minVec=np.min(self.data,axis=0)
        ewm=EWM(self.data)
        weight=ewm.calWeight()
        for i in range(self.n):
            Dimax,Dimin=0,0
            for j in range(self.m):
                #print(self.data,j,i)
                Dimax+=weight[j]*(maxVec[j]-self.data[i][j])**2
                Dimin+=weight[j]*(minVec[j]-self.data[i][j])**2
            Dimax**=0.5
            Dimin**=0.5
            self.res[i]=Dimin/(Dimin+Dimax)
        self.res=Tools.minmaxmap(self.res)
        if self.show==True:
            print(self.res)
        return self.res