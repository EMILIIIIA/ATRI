import numpy as np
from matplotlib import pyplot as plt

#最小二乘法线性回归
class OLS(object):

    def __init__(self,X,Y):
        # self.X=np.array(X)
        # if self.X.ndim==1:
        #     self.X.reshape(1,np.size(self.X,axis=0))
        # self.Y=np.array(Y)
        # if self.Y.ndim==1:
        #     self.Y.reshape(1,np.size(self.Y,axis=0))
        self.X=np.mat(X)
        self.Y=np.mat(Y)
        if np.size(self.X,axis=0)==1:
            self.X=self.X.T
        if np.size(self.Y,axis=0)==1:
            self.Y=self.Y.T
        self.res=[]

    def cal(self):
        self.res= np.dot(np.dot(np.linalg.inv(np.array(np.dot(self.X.T, self.X))), self.X.T), self.Y)
    
    def plot(self):
        print(self.res)