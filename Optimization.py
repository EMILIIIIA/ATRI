import random
from copy import deepcopy
from math import exp
from sys import float_info

import matplotlib.pyplot as plt
import numpy as np


class SAA(object):

    def __init__(self, function, T, Tmin, delta, lowBound: list, upBound: list, iter):
        self.func = function
        self.T = T
        self.num = len(lowBound)
        self.delta = delta
        self.lowBound = lowBound
        self.upBound = upBound
        self.maxIter = iter
        self.iter = 1
        self.bestRes = float_info.max
        self.bestX = 0
        self.resList = []
        self.Tmin = Tmin

    def initArg(self):
        res = []
        for i in range(self.num):
            res.append(
                (np.random.uniform(low=self.lowBound, high=self.upBound).tolist())[0])
        return res

    def calNext(self, arg):
        res = list()
        for i in range(len(arg)):
            res.append(arg[i] + np.random.uniform(low=-
                       0.055, high=0.055) * self.T)

            if res[i] > self.upBound[i]:
                res[i] = self.upBound[i]
            elif res[i] < self.lowBound[i]:
                res[i] = self.lowBound[i]
        return res

    def calPosibility(self, arg, newArg):
        return (exp(-(newArg - arg) / self.T))

    def cal(self):
        x = self.initArg()
        self.bestX = x
        while self.T > self.Tmin:
            y = self.func(x)
            nextX = self.calNext(x)
            nextY = self.func(nextX)

            if nextY - y < 0:
                x = nextX
            else:
                # metropolis principle
                p = self.calPosibility(y, nextY)
                r = np.random.uniform(low=0, high=1)
                if r < p:
                    x = nextX

            if self.func(x) < self.func(self.bestX):
                self.bestRes = self.func(self.bestX)
                self.bestX = x
            print("迭代次数：", self.iter, "当前最佳：", self.bestRes)
            self.iter += 1
            if self.iter > self.maxIter:
                break
            #降温
            self.T *= self.delta

        return {"x":self.bestX, "result":self.bestRes}


class GA(object):

    class GAunit(object):
        def __init__(self, gene, aMax, lowBound, upBound):
            self.gene = gene
            self.aMax = aMax  # 变异时最大改变数值
            self.length = len(self.gene)
            self.lowBound = lowBound
            self.upBound = upBound

        def variation(self):
            pos = random.randint(0, self.length-1)
            self.gene[pos] += random.uniform(-self.aMax, self.aMax)
            if self.gene[pos] > self.upBound[pos]:
                self.gene[pos] = float(self.upBound[pos])
            if self.gene[pos] < self.lowBound[pos]:
                self.gene[pos] = float(self.lowBound[pos])
            return self

        def cross(self):
            pos = [random.randint(0, self.length-1),
                   random.randint(0, self.length-1)]
            if self.lowBound[pos[0]] <= self.gene[pos[1]] <= self.upBound[pos[0]] and self.lowBound[pos[1]] <= self.gene[pos[0]] <= self.upBound[pos[1]]:
                self.gene[pos[0]], self.gene[pos[1]] = self.gene[pos[1]], self.gene[pos[0]]
            return self

    def __init__(self, population, size, lowBound, upBound, function, maxiter, aRate, aMax, cRate):
        self.population = population
        self.geneSize = size
        self.units = []
        for i in range(population):
            tem = []
            for i in range(len(lowBound)):
                tem.append(random.uniform(lowBound[i], upBound[i]))
            self.units.append(GA.GAunit(tem, aMax, lowBound, upBound))
        self.bestUnit = self.units[0]
        self.resultList = []
        self.maxiter = maxiter
        self.iter = 1
        self.func = function
        self.aRate = aRate
        self.cRate = cRate

    def findBest(self):

        for i in range(len(self.units)):
            if self.func(self.units[i].gene) > self.func(self.bestUnit.gene):
                self.bestUnit = deepcopy(self.units[i])

    def calWeight(self):
        weight = []
        minWeight = 2147483647
        for i in range(len(self.units)):
            tem = self.func(self.units[i].gene)
            minWeight = min(minWeight, tem)
            weight.append(tem)
        if(minWeight <= 0):
            for i in range(len(weight)):
                weight[i] += (-minWeight+1)
        return weight

    def generateNext(self):

        weight = self.calWeight()
        totalWeight = sum(weight)
        nextUnits = []
        #轮盘选择
        for i in range(self.population):
            randWeight = random.uniform(0, totalWeight)
            for j in range(self.population-1):
                #print(j)
                randWeight -= weight[j]
                if randWeight <= 0:
                    #选出一个，判断是否变异，执行对应操作后加入下一代
                    tem = deepcopy(self.units[j])
                    if random.random() < self.aRate:
                        tem.variation()
                    if random.random() < self.cRate:
                        tem.cross()
                    nextUnits.append(tem)
                    break
        self.findBest()
        nextUnits.append(self.bestUnit)
        self.units[:] = nextUnits[:]

    def plot(self, results):
        X = []
        Y = []

        for i in range(len(results)):
            X.append(i)
            Y.append(results[i][0])

        plt.plot(X, Y)
        plt.show()

    def cal(self):

        while self.iter <= self.maxiter:
            self.generateNext()
            self.findBest()
            print("迭代次数：", self.iter, "最佳个体基因：", self.bestUnit.gene)
            self.resultList.append([self.func(self.bestUnit.gene)])
            self.iter += 1

        self.findBest()
        self.plot(self.resultList)
        return self.bestUnit.gene

class ENUM(object):
    FINDMAX=0
    FINDMIN=1
    def __init__(self,func,num,mode):
        self.func=func
        self.num=num
        self.mode=mode
        self.enumList=[]
        self.index=[]
        self.ans=0


    def generateOrder(self,nowList:list,size:int):
        if nowList==None:
            nowList = []
        if size>self.num:
            self.enumList.append(nowList)
            return
        tem=nowList+[0]
        self.generateOrder(tem,size+1)
        tem=nowList+[1]
        self.generateOrder(tem,size+1)

    def cal(self):
        self.generateOrder([],1)
        n=len(self.enumList)
        if self.mode==ENUM.FINDMAX:
            self.ans=-2147483647
            for i in range(n):
                if self.ans<self.func(self.enumList[i]):
                    self.index.clear()
                    self.index.append(self.enumList[i])
                    self.ans=self.func(self.enumList[i])
                elif self.ans==self.func(self.enumList[i]):
                    self.index.append(self.enumList[i])
                
        else:
            self.ans=2147483647
            for i in range(n):
                if self.ans>self.func(self.enumList[i]):
                    self.index.clear()
                    self.index.append(self.enumList[i])
                    self.ans=self.func(self.enumList[i])
                elif self.ans==self.func(self.enumList[i]):
                    self.index.append(self.enumList[i])

        return {"result":self.ans,"index":self.index}
