# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
from geatpy_example.frame.schedule_new.quick_sort_brake import quick_sort_brake
##遗传算法解决问题分为两种，一种是将问题转为规划类问题求解；一种是直接对原问题进行求解

L_r=list(np.random.uniform(70,130,20))*10

W_r=list(np.random.uniform(13,23,20))*10


size_dict = {'1': (85.5, 16.3), '2': (99.3, 16.92), '3': (119.53, 22.5), '4': (110, 19.22), '5': (110, 17.2)}
wait_list = np.array(list(size_dict.values()) * 10)

#新增随机造的船舶
wait_list=np.vstack([wait_list,[[round(ll,2),round(ww,2)] for ll,ww in zip(L_r,W_r)]])

# wait_list=wait_list[6:12]
# 按照宽度排序，宽的在前么
# wait_list=sorted(wait_list,key =lambda x:x[1],reverse=True)
W = 34
L = 280
N = len(wait_list)

NIND = 6000
print('N',N)







class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        
        ##这里是选排列，范围是0-11，但是每次只选其中的6个数字排列
        Dim = min(6,N)  # 初始化Dim（决策变量维数）
        varTypes = [1]*Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0]*Dim  # 决策变量下界
        ub = [N-1]*Dim    # 决策变量上界
        lbin = [1]*Dim # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1]*Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        
        

        #brake_boat = quick_sort_brake(wait_list_new, L, W)

        Vars_brake_boat=[]
        Vars = pop.Phen  # 得到决策变量矩阵(6000, 6)
        
        for each in Vars:
            brake_boat=quick_sort_brake(wait_list[each], L, W)
            s=0
            for k,v in brake_boat.items():
                s=s+v[1][0]*v[1][1]
        
            sqare_rate=s/(L*W)
            
        
            print('面积利用率',sqare_rate)
            Vars_brake_boat.append(sqare_rate)
            
        
        
        
 
        obj1=np.array(Vars_brake_boat).reshape(-1,1) # (4000,)#面积最大
       
        pop.ObjV = obj1#计算目标函数值，赋值给pop种群对象的ObjV属性,求矩阵列和，即变量之和
       