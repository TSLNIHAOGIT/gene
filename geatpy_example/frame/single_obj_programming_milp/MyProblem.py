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
该案例展示了一个简单的混合整数决策变量最大化目标的单目标优化问题。
max f =3*x1+x2+3*x3
s.t.
-x1+2*x2+x3<=4
4*x2-3*x3<=2
x1-3*x2+2*x3<=3
x1>=0
x2>=0
x3>=0
且x1,x3为正数

最优解为：
x1=5,x2=11/4,x3=3

问题，明确写出决策变量上界，应该可以写一个很大的数字
#但是变量的上下界范围越小，求解就越准确，写太大时，每次运行时，差异也较大
"""


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 3  # 初始化Dim（决策变量维数）
        varTypes = [1,0,1]  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0,0,0]  # 决策变量下界
        ub = [10,10,10]  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen  # 得到决策变量矩阵
        x1=Vars[:, [0]]
        x2=Vars[:, [1]]
        x3 = Vars[:, [2]]
        pop.ObjV = 3*x1+x2+3*x3 # 计算目标函数值，赋值给pop种群对象的ObjV属性
        pop.CV = np.hstack([-x1+2*x2+x3-4,  # 第一个约束
                            4*x2-3*x3-2,  # 第二个约束
                            x1 - 3 * x2 + 2 * x3 -3 #第三个约束
                            ])