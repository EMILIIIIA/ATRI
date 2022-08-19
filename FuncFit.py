import numpy as np
from matplotlib import pyplot as plt
from Statistics import PCA

class OLS(object):
    """
    多元线性回归的最小二乘法，接收两个参数，X为自变量矩阵，Y为因变量向量。
    The ordinary least squares method of multiple linear regression.
    Receives two parameters, X is the matrix of independent variables, Y is the vector of dependent variables.
    """
    def __init__(self,X,Y):
        self.X=np.mat(X)
        self.Y=np.mat(Y)
        if np.size(self.X,axis=0)==1:
            self.X=self.X.T
        if np.size(self.Y,axis=0)==1:
            self.Y=self.Y.T
        self.res=np.array([])

    def cal(self):
        self.res= np.dot(np.dot(np.linalg.inv(np.array(np.dot(self.X.T, self.X))), self.X.T), self.Y)
        return self.res

    def plot(self):
        if np.size(self.X,axis=1)>=2:
            myPCA=PCA(self.X,2,0)
            myPCA.cal()

        minX,maxX=np.min(self.X),np.max(self.X)
        #fitX=np.arange(minX,maxX,np.size(self.X)/100)
        fitX=np.linspace(minX,maxX,100)
        fitY=np.array([self.res.tolist()[0][0]*i for i in fitX])
        plt.plot(self.X, self.Y, 'o',label='original values')
        plt.plot(fitX, fitY, 'r',label='polyfit values')

        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend(loc=2, bbox_to_anchor=(1.05,1.0),borderaxespad = 0.)
        #plt.title('polyfitting')
        plt.show()

class PloyFit(object):
    """
    多项式函数拟合，使用numpy的ployfit函数。
    
    """
    def __init__(self,x,y,deg=1):
        self.x=x
        self.y=y
        self.deg=deg

    def cal(self):
        poly = np.polyfit(self.x,self.y,deg=self.deg)
        minX,maxX=np.min(self.x),np.max(self.x)
        self.fitX=np.linspace(minX,maxX,100)
        self.fitY = np.polyval(poly, self.fitX)
        return poly

    def plot(self):
        plt.plot(self.x, self.y, 'o')
        plt.plot(self.fitX, self.fitY)
        plt.show()