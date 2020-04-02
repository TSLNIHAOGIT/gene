# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea


class TestProblem(ea.Problem):  # 继承Problem父类
    def __init__(self, testName):  # testName为测试集名称
        name = testName  # 初始化name
        # 读取城市坐标数据
        path=r'E:\tsl_file\python_project\gene\geatpy_example\frame\tsp_path'
        self.places = np.loadtxt(path +'\\'+ testName + ".csv", delimiter=",", usecols=(0, 1))
        M = 1  # 初始化M（目标维数）
        #(48, 2)
        Dim = self.places.shape[0]  # 初始化Dim（决策变量维数）
        maxormins = [1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        varTypes = [0] * Dim  # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = [0] * Dim  # 决策变量下界#[0,0,0,0,...,0]共48个0
        ub = [Dim - 1] * Dim  # 决策变量上界[47,47,47,47,...,47]共48个47#这里一共有48个节点编号从0-47
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        #P编码是一个排序这里是0-37共38个
        x = pop.Phen  # 得到决策变量矩阵
        x = x.copy()
        # 添加最后回到出发地
        #一行代表一个个体，一列代表一个决策变量，第一列是起始节点，依次是第二个，第三个，等等经过的节点
        X = np.hstack([x, x[:, [0]]])
        X = X.astype(int)
        ObjV = []  # 存储所有种群个体对应的总路程
        for i in range(X.shape[0]):
            #X[i]第i个个体的所有决策变量，对应是一个完整的路径
            journey = self.places[X[i], :]  # 按既定顺序到达的地点坐标
            distance = np.sum(np.sqrt(np.sum(np.diff(journey.T) ** 2, 0)))  # 计算总路程
            ObjV.append(distance)
        pop.ObjV = np.array([ObjV]).T