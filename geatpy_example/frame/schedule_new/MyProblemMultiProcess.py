# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
from geatpy_example.frame.schedule_new.quick_sort_brake import quick_sort_brake
from multiprocessing import Pool as ProcessPool

##遗传算法解决问题分为两种，一种是将问题转为规划类问题求解；一种是直接对原问题进行求解
def subAimFunc(args):
    Vars_i=args[0]
    wait_list=args[1]
    L=args[2]
    W=args[3]
    # Vars_brake_boat = []
    # Vars = pop.Phen  # 得到决策变量矩阵(6000, 6)

    def get_sqare_rate(in_brake_sort, L, W):
        brake_boat = quick_sort_brake(in_brake_sort, L, W)
        s = 0
        for k, v in brake_boat.items():
            s = s + v[1][0] * v[1][1]

        sqare_rate = s / (L * W)
        return sqare_rate, brake_boat
    in_brake_sort = wait_list[Vars_i]
    sqare_rate, brake_boat = get_sqare_rate(in_brake_sort, L, W)
    return sqare_rate


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self,wait_list,L,W):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        self.wait_list = wait_list
        self.L=L
        self.W=W
        N=len(wait_list)
        ##这里是选排列，范围是0-11，但是每次只选其中的6个数字排列
        Dim = min(6,N)  # 初始化Dim（决策变量维数）
        varTypes = [1]*Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0]*Dim  # 决策变量下界
        ub = [N-1]*Dim    # 决策变量上界
        lbin = [1]*Dim # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1]*Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）

        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        num_cores = 8
        self.pool = ProcessPool(num_cores)  # 设置池的大小

    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen  # 得到决策变量矩阵
        args = list(zip(Vars, [self.wait_list] * pop.sizes, [self.L] * pop.sizes, [self.W] * pop.sizes))
        result = self.pool.map_async(subAimFunc, args)
        result.wait()
        res = result.get()
        obj1 = np.array(res).reshape(-1, 1)  # (4000,)#此处改为闸次最小
        pop.ObjV = obj1  # 计算目标函数值，赋值给pop种群对象的ObjV属性,求矩阵列和，即变量之和
