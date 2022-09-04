from operator import inv
import numpy as np
from numpy import linalg
from math import exp


class GreyForecast(object):

    def __init__(self,X,Y):
        self.X=np.array(X).astype(float)
        self.Y=np.array(Y).astype(float)
        self.n=np.size(self.X,axis=0)
    
    def check(self):
        minn=exp(-2/(self.n+1))
        maxn=exp(2/(self.n+1))
        ans=[0]
        for i in range(1,self.n):
            ans.append(self.Y[i-1]/self.Y[i])
        for i in range(1,self.n):
            if not minn<ans[i]<maxn:
                print("第{id}个指标不在区间内".format(id=i))


    def cal(self):
        self.check()
        #计算累加数列
        B=np.cumsum(self.Y)
        #紧邻均值生成
        C=[0]
        for i in range(2,self.n):
            C.append(-(B[i]+B[i-1])/2)
        #构造数据矩阵
        B=[C,[1 for i in range(self.n-1)]]
        Y=self.Y
        Y[0]=0
        Y=np.mat(Y)
        Y=linalg.inv(Y).tolist()

# %构造数据矩阵 
# B = [-C;ones(1,n-1)];
# Y = A; Y(1) = []; Y = Y';

g=GreyForecast([174, 179, 183, 189, 207, 234, 220.5, 256, 270, 285],[174, 179, 183, 189, 207, 2340, 220.5, 256, 270, 285])
g.cal()