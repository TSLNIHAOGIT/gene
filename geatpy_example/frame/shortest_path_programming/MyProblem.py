# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
##遗传算法解决问题分为两种，一种是将问题转为规划类问题求解；一种是直接对原问题进行求解


###对于之前的车辆路径问题目前也是两个思路：
'''
1.直接转为规划类问题
2.直接对原问题进行求解
'''



"""
该案例展示了一个简单的离散型决策变量最大化目标的单目标优化问题。
整数规划求解最短路径问题
令o,d为起点，终点
xij:每条边是否出现在最短路径上
cij:每条边权重，如果有向边不存在，则cij为无穷

min (sum(Cij.xij))
s.t.
除去起点和终点：满足出边和等于入边和
出边和《=1；入边和《=1
起点出边和为1，入边和为0
终点出边和为0，入边和为1
Xij in [0,1]



"""


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 100  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0]*Dim  # 决策变量下界
        ub = [1]*Dim # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        # 设置有向图中各条边的权重
        self.weights = {'(1, 2)': 36, '(1, 3)': 27, '(2, 4)': 18, '(2, 5)': 20, '(2, 3)': 13, '(3, 5)': 12,
                        '(3, 6)': 23,
                        '(4, 7)': 11, '(4, 8)': 32, '(5, 4)': 16, '(5, 6)': 30, '(6, 7)': 12, '(6, 9)': 38,
                        '(7, 8)': 20,
                        '(7, 9)': 32, '(8, 9)': 15, '(8, 10)': 24, '(9, 10)': 13}

    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen  # 得到决策变量矩阵
        Vars=Vars.reshape((pop.sizes,10,10))
        obj=np.zeros((pop.sizes, 1))
        for i in range(10):
            for j in range(10):
                xij = Vars[:, i, j].reshape((pop.sizes, 1))
                value=self.weights.get('({}, {})'.format(i+1,j+1),0)
                obj = obj + value * xij


        # for key ,value in self.weights.items():
        #             key=eval(key)
        #
        #             i=key[0]-1
        #             j=key[1]-1
        #             # print('key', key,i,j)
        #             xij=Vars[:,i,j].reshape((pop.sizes, 1))
        #             # print('xij',np.array(xij))
        #
        #             obj=obj+ value*xij

        pop.ObjV = obj # 计算目标函数值，赋值给pop种群对象的ObjV属性
        #开始计算约束条件
        constraint=[]
        # 出边之和等于入边之和；要修改
        constraint.append(np.abs(np.sum(Vars,axis=1)[:,1:-1]-np.sum(Vars,axis=2)[:,1:-1]))
        #出边和或者入边和都小于等于1
        constraint.append(np.sum(Vars, axis=1)-1)
        constraint.append(np.sum(Vars, axis=2)-1)

        ##起点出边和为1，入边和为0
        constraint.append(np.abs(np.sum(Vars[:, 0,:, None],axis=1)-1))
        constraint.append(np.abs(np.sum(Vars[:, :, 0, None], axis=1) ))

        ##出边和为0，终点入边和为1
        constraint.append(np.abs(np.sum(Vars[:,: , -1, None], axis=1) - 1))
        constraint.append(np.abs(np.sum(Vars[:, -1, :, None], axis=1)))

        pop.CV = np.hstack(constraint)
        #