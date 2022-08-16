import numpy as np

class DP(object):

    def __init__(self,num,capacity,size,price):
        self.num=num
        self.size=size
        self.price=price
        self.capacity=capacity
        self.dp=[0 for col in range(0,self.capacity+1)]

    
    def cal(self):
        for i in range(self.num):
            for j in range(self.capacity,0,-1):
                if j>=self.size[i]:
                    self.dp[j]=max(self.dp[j],self.dp[j-self.size[i]]+self.price[i])
        print(self.dp[self.capacity])