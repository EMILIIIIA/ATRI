import random
import tkinter
import copy
import sys


class ACO:
    # 懒得给内部类传参了，所以开成了静态变量，反正大概率没人同时给这个类创建多个实例
    alpha, beta, rho, q = 0, 0, 0, 0 #信息素权重常数、启发函数权重常数、信息素挥发常数、信息素常数
    cityNum, antNum, maxIter = 0, 100, 100 # 城市数量 蚂蚁数量 最大迭代次数
    distanceX, distanceY, dis, pheromone = [], [], [], [] #城市横坐标 城市纵坐标 城市间距离 信息素矩阵

    def __init__(self, inputX, inputY, inputAlpha=4, inputBeta=4, inputRho=0.3, inputQ=100, inputAnts=50,
                 inputIter=100):
        self.__init_data(inputX, inputY, inputAlpha, inputBeta, inputRho, inputQ, inputAnts, inputIter)# 初始化数据
        self.__init_ants()#初始化蚁群

    def runTSP(self):
        # 初始化画布
        self.__init_canvas()
        # 进入迭代循环
        for lp in range(ACO.maxIter):
            for ant in self.ants:
                ant.search_path()# 搜索一条路径并与当前最优蚂蚁比较
                if ant.totalDis < self.bestAnt.totalDis:
                    self.bestAnt = copy.deepcopy(ant)# 更新最优解

            self.__update_pheromone()# 蚁周算法更新信息素
            print(u"迭代次数：", self.iterTimes, u"最佳路径总距离：", int(self.bestAnt.totalDis))
            self.__line(self.bestAnt.path)# 连线
            self.canvas.update()# 更新画布
            self.iterTimes += 1
        self.__draw_text()# 防止文字被覆盖
        self.TSPGUI.mainloop()


    def __init_data(self, inputX, inputY, inputAlpha, inputBeta, inputRho, inputQ, inputAnts, inputIter):
        #参数赋值
        ACO.alpha, ACO.beta, ACO.rho, ACO.q = inputAlpha, inputBeta, inputRho, inputQ
        ACO.distanceX, ACO.distanceY = copy.deepcopy(inputX), copy.deepcopy(inputY)
        #判断横纵坐标是否数量相同
        if len(ACO.distanceX) != len(ACO.distanceY):
            print(u"坐标输入错误!")
            sys.exit()
        ACO.cityNum,ACO.antNum ,ACO.maxIter= len(ACO.distanceX), inputAnts,inputIter
        ACO.dis = copy.deepcopy([[0.0 for col in range(ACO.cityNum)] for row in range(ACO.cityNum)])
        ACO.pheromone = copy.deepcopy([[1.0 for col in range(ACO.cityNum)] for row in range(ACO.cityNum)])
        self.nodes = []  # 节点画布上坐标
        # 初始化城市间距离
        for i in range(self.cityNum):
            for j in range(self.cityNum):
                tempDistance = pow((self.distanceX[i] - self.distanceX[j]), 2) + pow(
                    (self.distanceY[i] - self.distanceY[j]), 2)
                tempDistance = pow(tempDistance, 0.5)
                self.dis[i][j] = int(tempDistance)
        # 初始城市之间信息素
        for i in range(self.cityNum):
            for j in range(self.cityNum):
                self.pheromone[i][j] = 1.0
        # 初始化显示相关参数
        self.__circleRadius, self.__lineWidth, self.__circleWidth = 5, 2, 1
        self.__displayWidth, self.__displayHeight = 800, 600
        self.__outlineColor, self.__fillColor, self.__textColor, self.__bgColor, self.__lineColor = "#000000", "#ff0000", "#000000", "#ffffff", "#000000"

    def __init_canvas(self):
        # 创建窗口
        self.TSPGUI = tkinter.Tk()
        self.TSPGUI.title("蚁群算法解TSP问题")
        self.canvas = tkinter.Canvas(
            self.TSPGUI,
            width=self.__displayWidth,
            height=self.__displayHeight,
            bg=self.__bgColor)
        self.canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH)

        # 清空画布
        for item in self.canvas.find_all():
            self.canvas.delete(item)

        # 初始化城市节点
        maxX, maxY = max(ACO.distanceX), max(ACO.distanceY)
        for i in range(len(self.distanceX)):
            # 计算画布上坐标
            x, y = int(float(self.__displayWidth) / maxX * self.distanceX[i]), int(
                float(self.__displayHeight) / maxY * self.distanceY[i])
            self.nodes.append((x, y))
            # 生成节点圆
            node = self.canvas.create_oval(x - self.__circleRadius, y - self.__circleRadius, x + self.__circleRadius,
                                           y + self.__circleRadius,
                                           fill=self.__fillColor,  # 填充颜色
                                           outline=self.__outlineColor,  # 轮廓颜色
                                           width=self.__circleWidth,)
        # 显示坐标文字
        self.__draw_text()

    def __draw_text(self):
        for i in range(len(self.nodes)):
            self.canvas.create_text(self.nodes[i][0], self.nodes[i][1] - 2 * self.__circleRadius,
                                    # 使用create_text方法在坐标处绘制文字
                                    text='(' + str(self.distanceX[i]) + ',' + str(self.distanceY[i]) + ')',  # 所绘制文字的内容
                                    fill=self.__textColor  # 文字颜色
                                    )

    def __init_ants(self):
        self.ants = [self.Ant(i1) for i1 in range(self.antNum)]  # 初始化蚁群
        self.bestAnt = self.Ant(-1)  # 初始化最优解
        self.bestAnt.totalDis = 2147483647  # 初始最大距离，直接访问数据成员不是好习惯，小孩子不要学坏
        self.iterTimes = 1  # 初始化迭代次数

    def __update_pheromone(self):
        tempPheromone = [[0.0 for col in range(self.cityNum)] for row in range(self.cityNum)]
        for ant in self.ants:
            for i in range(1, self.cityNum):
                start, end = ant.path[i - 1], ant.path[i]
                # 根据公式在路径上的每两个相邻城市间留下信息素
                tempPheromone[start][end] += self.q / ant.totalDis
                tempPheromone[end][start] = tempPheromone[start][end]

        # 更新所有城市之间的信息素，旧信息素衰减加上新信息素
        for i in range(self.cityNum):
            for j in range(self.cityNum):
                self.pheromone[i][j] = self.pheromone[i][j] * ACO.rho + tempPheromone[i][j]

    def __line(self, path):
        self.canvas.delete("lines")  # 删除原线
        for i in path:
            p1, p2 = self.nodes[path[i]], self.nodes[path[i - 1]]
            self.canvas.create_line(p1, p2, fill=self.__lineColor, tags="lines", width=self.__lineWidth)

    def setColor(self, **inputColor):
        for i in inputColor.keys():
            if i == 'fillColor':
                self.__fillColor = inputColor[i]
            if i == 'bgColor':
                self.__bgColor = inputColor[i]
            if i == 'textColor':
                self.__textColor = inputColor[i]
            if i == 'outlineColor':
                self.__outlineColor = inputColor[i]
            if i == 'lineColor':
                self.__lineColor = inputColor[i]

    def setLine(self, **inputLine):
        for i in inputLine.keys():
            if i == 'circleRadius':
                self.__circleRadius = inputLine[i]
            if i == 'lineWidth':
                self.__lineWidth = inputLine[i]
            if i == 'circleWidth':
                self.__circleWidth = inputLine[i]

    def setScreen(self, inX, inY):
        self.__displayWidth, self.__displayHeight = inX, inY

    class Ant:
        def __init__(self, ID):  # 初始化变量
            self.ID = ID  # 蚂蚁的id
            self.__init_data()

        def search_path(self):  # 外部调用需要的函数
            # 初始化数据
            self.__init_data()
            # 搜素路径，遍历完所有城市为止
            while self.cnt < ACO.cityNum:
                # 移动到下一个城市
                nextCity = self.__choose_next()
                self.__move(nextCity)
            # 计算路径总长度
            self.__cal_total_distance()

        def __init_data(self):
            self.path = []  # 已经走过的路径
            self.totalDis = 0.0  # 已经走过的距离
            self.currentCity = -1  # 初始化当前的城市
            self.canVis = [True for i in range(ACO.cityNum)]  # 可以访问的城市列表
            self.cnt = 1  # 已经访问过的城市数量

            tempCity = random.randint(0, ACO.cityNum - 1)  # 随机初始点
            self.currentCity = tempCity  # 更新当前蚂蚁所在城市
            self.path.append(tempCity)  # 将初始点加入路径
            self.canVis[tempCity] = False  # 给初始点打标记

        def __choose_next(self):
            nextCity = -1
            selectProb = [0.0 for i in range(ACO.cityNum)]  # 定义一个存储去下个城市的概率的表
            totalProb = 0.0

            for i in range(ACO.cityNum):  # 获取去下一个城市的概率
                if self.canVis[i]:  # 如果这个城市不可以访问那么直接不用算了，好耶
                    # 通过公式计算概率
                    selectProb[i] = pow(ACO.pheromone[self.currentCity][i], ACO.alpha) * pow((1.0 / ACO.dis[self.currentCity][i]),ACO.beta)
                    totalProb += selectProb[i]

            if totalProb > 0.0:  # 选择城市代码
                tempProb = random.uniform(0.0, totalProb)  # 产生一个0~totalProb之间的随机概率
                for i in range(ACO.cityNum):
                    if self.canVis[i]:
                        tempProb -= selectProb[i]  # 轮次相减
                        if tempProb < 0.0:
                            nextCity = i
                            break

            if (nextCity == -1):  # 保险起见，如果没有产生，则顺序选择一个城市
                nextCity = random.randint(0, ACO.cityNum - 1)
                while self.canVis[nextCity] == False:  # if==False,说明已经遍历过了
                    nextCity = random.randint(0, ACO.cityNum - 1)
            return nextCity

        def __cal_total_distance(self):  # 计算路径的总距离

            tempDistance = 0.0
            start, end = 0, 0
            for i in range(1, ACO.cityNum):
                start, end = self.path[i], self.path[i - 1]
                tempDistance += ACO.dis[start][end]
            # 最后加上末尾城市回到初始城市的距离，构成回路
            end = self.path[0]
            tempDistance += ACO.dis[start][end]
            self.totalDis = tempDistance

        def __move(self, nextCity):  # 移动函数

            self.path.append(nextCity)
            self.canVis[nextCity] = False
            self.totalDis += ACO.dis[self.currentCity][nextCity]
            self.currentCity = nextCity
            self.cnt += 1
