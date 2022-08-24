import numpy as np

class DP01(object):

    def __init__(self,num,capacity,size,price):
        self.num=num
        self.size=size
        self.price=price
        self.capacity=capacity
        self.show=True
        self.dp=[0 for _ in range(0,self.capacity+1)]

    
    def cal(self):
        for i in range(self.num):
            for j in range(self.capacity,0,-1):
                if j>=self.size[i]:
                    self.dp[j]=max(self.dp[j],self.dp[j-self.size[i]]+self.price[i])
        if self.show==True:
            print("最好的结果为: ",self.dp[self.capacity])
        return self.dp[self.capacity]