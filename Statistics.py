import numpy as np

class PCA(object):
    def __init__(self,A,k,ddof=1):
        self.matrix=A
        self.k=k
        self.ddof=ddof
        self.show=True

    def cal(self):
        self.matrix=self.matrix-self.matrix.mean(axis=0)
        cov=np.cov(self.matrix.T,ddof=self.ddof)
        D,V=np.linalg.eig(cov)
        kmaxEValues=D.argsort()[-self.k:][::-1]
        kmaxEVectors=V[kmaxEValues]
        contributionRate=[i/np.sum(kmaxEValues) for i in kmaxEValues]
        res=np.dot(self.matrix, kmaxEVectors.T)
        if self.show==True:
            print("贡献率: ",contributionRate,"结果: ",res)
        return {"crate":contributionRate,"result":res}