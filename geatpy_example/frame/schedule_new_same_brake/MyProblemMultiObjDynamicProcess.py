# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
# from geatpy_example.frame.schedule_new_same_brake.quick_sort_multi_brakes import quick_sort_multi_brakes
# from geatpy_example.frame.schedule_new_same_brake.quick_sort_multi_brakes_complete import quick_sort_multi_brakes
from geatpy_example.frame.schedule_new_same_brake.quick_sort_multi_dynamic_brakes_complete import quick_sort_multi_brakes
##遗传算法解决问题分为两种，一种是将问题转为规划类问题求解；一种是直接对原问题进行求解
from geatpy_example.frame.schedule_new_same_brake.quick_sort_multi_brakes import one_brake_area_ratio
from multiprocessing import Pool as ProcessPool

def subAimFunc(args):
    Vars_i=args[0]
    wait_list=args[1]
    brakes=args[2]

    def get_sqare_rate(in_brake_sort, brakes):
        # print(f'in_brake_sort={in_brake_sort}')
        all_brake_boat,brakes = quick_sort_multi_brakes(in_brake_sort, brakes)
        sqare_rate = 0
        for brake_num, e_brake_boat in all_brake_boat.items():
            L, W = brakes[brake_num]
            area_ratio = one_brake_area_ratio(e_brake_boat['brake_boat'], L, W)
            sqare_rate += area_ratio
        return sqare_rate,sqare_rate/len(brakes)

    in_brake_sort = wait_list[Vars_i]
    sqare_rate_all_brake,sqare_rate_avg_brake = get_sqare_rate(in_brake_sort, brakes)
    return sqare_rate_all_brake,sqare_rate_avg_brake


class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self,wait_list,brakes):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        self.wait_list = wait_list
        self.brakes=brakes
        N=len(wait_list)
        ##这里是选排列，范围是0-11，但是每次只选其中的6个数字排列
        #维度是Dim,范围是0~N-1；例如Dim=18，N=28，即选取18个数字进行排列，范围是从0-27当中选
        Dim = min(len(brakes)*6,N)  # 初始化Dim（决策变量维数）
        varTypes = [1]*Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0]*Dim  # 决策变量下界
        ub = [N-1]*Dim    # 决策变量上界
        lbin = [1]*Dim # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1]*Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）

        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        num_cores = 4
        self.pool = ProcessPool(num_cores)  # 设置池的大小

    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen  # 得到决策变量矩阵(6000, 6)
        args = list(zip(Vars, [self.wait_list] * pop.sizes, [self.brakes] * pop.sizes))
        result = self.pool.map_async(subAimFunc, args)
        result.wait()
        res_sqare_rate_all_brake ,res_sqare_rate_avg_brake= result.get()
        obj1 = np.array(res_sqare_rate_all_brake).reshape(-1, 1)  # (4000,)#此处改为闸次最小
        obj2 = np.array(res_sqare_rate_avg_brake).reshape(-1, 1)
        pop.ObjV = np.hstack([obj1,obj2])  # 计算目标函数值，赋值给pop种群对象的ObjV属性,求矩阵列和，即变量之和
