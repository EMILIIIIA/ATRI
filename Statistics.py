import numpy as np

class PCA(object):
    def __init__(self,A,k,ddof=1):
        self.matrix=A
        self.k=k
        self.ddof=ddof

    def cal(self):
        self.matrix=self.matrix-self.matrix.mean(axis=0)
        cov=np.cov(self.matrix.T,ddof=self.ddof)
        D,V=np.linalg.eig(cov)
        kmaxEValues=D.argsort()[-self.k:][::-1]
        kmaxEVectors=V[kmaxEValues]
        contributionRate=[i/np.sum(kmaxEValues) for i in kmaxEValues]
        return contributionRate,np.dot(self.matrix, kmaxEVectors.T)