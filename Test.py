
from Cluster import KMEANS
from TSP import ACO
import random
import numpy as np
from Tools import readcsv
import Tools

# A=[[random.uniform(-100,100),random.uniform(-100,100)] for i in range(400)]
# k=KMEANS(A,6)
# k.cal()
# k.plot()

# X=random.sample(range(10,600),50) 
# Y=random.sample(range(10,600),50)
# a = ACO(X, Y, 1, 3, 0.5, 100, 75, 100)
# a.cal()
data=readcsv("./data.csv")["data"]
data=np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
print(data[:,[0,2]],'\n',Tools.pointBest2largerBest(data[:,[0,2]],7))
#data=np.hstack((Tools.pointBest2largerBest(data[:,[0,2]],7),Tools.pointBest2largerBest(data[:,[1,3]],5)))
#print(data)
#print(Tools.minmaxmap(data))