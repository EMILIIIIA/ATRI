import numpy as np
from matplotlib import pyplot as plt
import random
import csv
import operator
import sys
sys.path.append("..")
from Statistics import PCA

class KMEANS(object):
    color=['green','red','blue','yellow','purple','orange','deeppink','aliceblue', 'aqua', 'aquamarine', 'azure', 
    'beige', 'bisque', 'black', 'blanchedalmond', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate',
     'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 
     'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue',
      'darkslategray', 'darkturquoise', 'darkviolet', 'deepskyblue', 'dimgray', 'dodgerblue', 'firebrick', 'floralwhite', 
      'forestgreen', 'fuchsia', 'gainsboro', 'gold', 'goldenrod', 'gray', 'greenyellow', 'honeydew', 'hotpink', 
      'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 
      'lightcyan', 'lightgoldenrodyellow', 'lightgreen', 'lightgray', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 
      'lightslategray', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 
      'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 
      'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 
      'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 
      'pink', 'plum', 'powderblue', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 
      'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle',
      'tomato', 'turquoise', 'violet', 'wheat', 'yellowgreen']
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
            
    def cal(self):
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
            point=temPCA.cal()[1]
        else:
            point=self.dataMatrix.tolist()
        for i in range(len(point)):
                plt.scatter(point[i][0],point[i][1], marker = 'o',color = KMEANS.color[self.belong[i]], s = 40)
        plt.show()