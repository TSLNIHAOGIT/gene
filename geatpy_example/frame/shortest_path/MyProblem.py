# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'Shortest_Path'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 10  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim  # 决策变量下界
        ub = [9] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界
        ubin = [1] * Dim  # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        # 设置每一个结点下一步可达的结点（结点从1开始数，因此列表nodes的第0号元素设为空列表表示无意义）
        self.nodes = [[], [2, 3], [3, 4, 5], [5, 6], [7, 8], [4, 6], [7, 9], [8, 9], [9, 10], [10]]
        # 设置有向图中各条边的权重
        self.weights = {'(1, 2)': 36, '(1, 3)': 27, '(2, 4)': 18, '(2, 5)': 20, '(2, 3)': 13, '(3, 5)': 12,
                        '(3, 6)': 23,
                        '(4, 7)': 11, '(4, 8)': 32, '(5, 4)': 16, '(5, 6)': 30, '(6, 7)': 12, '(6, 9)': 38,
                        '(7, 8)': 20,
                        '(7, 9)': 32, '(8, 9)': 15, '(8, 10)': 24, '(9, 10)': 13}

    def decode(self, priority):  # 将优先级编码的染色体解码得到一条从节点1到节点10的可行路径
        #priority就是一个排列组成的列表
        edges = []  # 存储边
        path = [1]  # 结点1是路径起点
        ###经过固定点的感觉可以，必须在可行路径上固定该点，然后可以
        ###或者可以经过固定点且路径短系数就大，否则就小
        while not path[-1] == 10:  # 开始从起点走到终点
            currentNode = path[-1]  # 得到当前所在的结点编号
            nextNodes = self.nodes[currentNode]  # 获取下一步可达的结点组成的列表
            if len(nextNodes) == 0:
                raise RuntimeError("Error in decode: No way to go. (当前结点出度为0，无路可走。)")
            chooseNode = nextNodes[np.argmax(
                priority[np.array(nextNodes) - 1])]  # 从NextNodes中选择优先级更高的结点作为下一步要访问的结点，因为结点从1数起，而下标从0数起，因此要减去1
            path.append(chooseNode)
            edges.append((currentNode, chooseNode))
        return path, edges

    def aimFunc(self, pop):  # 目标函数
        pop.ObjV = np.zeros((pop.sizes, 1))  # 初始化ObjV
        for i in range(pop.sizes):
            priority = pop.Phen[i, :]
            ##这里也是P编码，解码是对于返回的染色体值，自己又重新写了解码方式
            ##而tsp问题的是直接使用的，直到赋值给pop.objV

            path, edges = self.decode(priority)  # 将优先级编码的染色体解码得到访问路径及经过的边
            pathLen = 0
            for edge in edges:
                key = str(edge)  # 根据路径得到键值，以便根据键值找到路径对应的长度
                if not key in self.weights:
                    raise RuntimeError("Error in aimFunc: The path is invalid. (当前路径是无效的。)", path)
                pathLen += self.weights[key]  # 将该段路径长度加入
            pop.ObjV[i] = pathLen  # 计算目标函数值，赋值给pop种群对象的ObjV属性


if __name__ == "__main__":
    problem = MyProblem()  # 生成问题对象
    """=================================种群设置================================="""
    Encoding = 'P'  # 编码方式
    NIND = 4  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置==============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 10  # 最大进化代数
    myAlgorithm.recOper = ea.Xovox(XOVR=0.8)  # 设置交叉算子
    myAlgorithm.mutOper = ea.Mutinv(Pm=0.1)  # 设置变异算子
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制过程动画）
    """==========================调用算法模板进行种群进化=========================="""
    [population, obj_trace, var_trace] = myAlgorithm.run()  # 执行算法模板，得到最后一代种群以及进化记录器
    population.save()  # 把最后一代种群的信息保存到文件中
    # 输出结果
    best_gen = np.argmin(obj_trace[:, 1])  # 记录最优种群是在哪一代
    best_ObjV = np.min(obj_trace[:, 1])
    print('最短路程为：%s' % (best_ObjV))
    print('最佳路线为：')
    best_journey, edges = problem.decode(var_trace[best_gen, :])
    for i in range(len(best_journey)):
        print(int(best_journey[i]), end=' ')
    print()
    print('有效进化代数：%s' % (obj_trace.shape[0]))
    print('最优的一代是第 %s 代' % (best_gen + 1))
    print('评价次数：%s' % (myAlgorithm.evalsNum))
    print('时间已过 %s 秒' % (myAlgorithm.passTime))
