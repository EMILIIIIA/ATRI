
from Cluster import KMEANS
from TSP import ACO
import random
import numpy as np
from Tools import readcsv
import Tools
import FuncFit
from Evaluation import EWM
# A=[[random.uniform(-100,100),random.uniform(-100,100),random.uniform(-100,100),random.uniform(-100,100)] for i in range(400)]
# k=KMEANS(A,6)
# k.cal()
# k.plot()

# X=random.sample(range(10,600),50) 
# Y=random.sample(range(10,600),50)
# a = ACO(X, Y, 1, 3, 0.5, 100, 75, 100)
# a.cal()

# data=readcsv("./data.csv")["data"]
# data=np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
# print(np.array([[1,3,4,6,19]]).T,'\n\n',Tools.terminalBest2largerBest(np.array([[1,3,4,6,19],[5,1,3,2,6],[1,1,4,5,1]]).T,5))
#data=np.hstack((Tools.pointBest2largerBest(data[:,[0,2]],7),Tools.pointBest2largerBest(data[:,[1,3]],5)))
#print(data)
#print(Tools.minmaxmap(data))


# X=np.mat([i for i in range(10)])
# Y=np.mat([5*i+random.random()*10 for i in range(10)])
# o=FuncFit.OLS(X,Y)
# print(o.cal())
# o.plot()

# X=np.array([i for i in range(-10,10)])
# Y=np.array([i**3-10*i**2+3*i+random.random()*10 for i in range(-10,10)])
# f=FuncFit.PloyFit(X,Y,10)
# print(f.cal())
# f.plot()


e=EWM("./data.csv",[1,2])
e.cal()