
from Cluster import KMEANS
from TSP import ACO
import random
import numpy as np
from Tools import readcsv

A=[[random.uniform(-100,100),random.uniform(-100,100)] for i in range(400)]
k=KMEANS(A,6)
k.cal()
k.plot()

X=random.sample(range(10,600),50) 
Y=random.sample(range(10,600),50)
a = ACO(X, Y, 1, 3, 0.5, 100, 75, 100)
a.cal()