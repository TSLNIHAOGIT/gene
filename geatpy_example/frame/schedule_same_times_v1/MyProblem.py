# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
from geatpy_example.frame.schedule_same_times_v1.quick_sort_brake import quick_sort_brake
from sklearn.cluster import KMeans
##遗传算法解决问题分为两种，一种是将问题转为规划类问题求解；一种是直接对原问题进行求解

##增加多进程处理
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
import multiprocessing as mp
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool


# def subAimFunc(data):



class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self,wait_list,L,W):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        self.wait_list = wait_list
        self.L=L
        self.W=W
        N=len(wait_list)


        # 把上面数据点分为两组（非监督学习）
        clf = KMeans(n_clusters=N)
        clf.fit(self.wait_list)  # 分组

        # centers = clf.cluster_centers_  # 两组数据点的中心点
        self.labels = clf.labels_  # 每个数据点所属分组
        ##这里是选排列，范围是0-11，但是每次只选其中的6个数字排列
        # Dim = min(18,N)  # 初始化Dim（决策变量维数）
        Dim=N
       
        varTypes = [1]*Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
               
        lb = [0]*Dim  # 决策变量下界
        ub = [N-1]*Dim    # 决策变量上界
        lbin = [1]*Dim # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1]*Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）

        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        # num_cores = int(mp.cpu_count())  # 获得计算机的核心数
        # self.pool = ProcessPool(num_cores)  # 设置池的大小


    def aimFunc(self, pop):  # 目标函数
        
        

        #brake_boat = quick_sort_brake(wait_list_new, L, W)

        Vars_brake_boat=[]
        Vars = pop.Phen  # 得到决策变量矩阵(6000, 6)

        def get_sqare_rate(in_brake_sort, L,W):
            brake_boat=quick_sort_brake(in_brake_sort, L, W)
            s=0
            for k,v in brake_boat.items():
                s=s+v[1][0]*v[1][1]
        
            sqare_rate=s/(L*W)            
            return sqare_rate,brake_boat



      

        for each in Vars:
            #in_brake_sort={ i:self.wait_list[i] for i in each}
            sqare_rate_all_brake=0
            all_brake_times = 0
            in_brake_sort = self.wait_list[each]
            weight={0:0.4,1:0.3,2:0.3}
            while True:

                if len(in_brake_sort)>0 :
                    sqare_rate,brake_boat=get_sqare_rate(in_brake_sort, self.L,self.W)
                    brake_num=list(brake_boat.keys())

                    #更新in_brake_sort
                    ##each2=np.delete(each,brake_num,axis=0)
                    in_brake_sort=np.delete(in_brake_sort,brake_num,axis=0)

                    sqare_rate_all_brake=sqare_rate_all_brake+sqare_rate#*weight[all_brake_times]
                    all_brake_times=all_brake_times+1
                else:
                    break





            Vars_brake_boat.append((sqare_rate_all_brake-sqare_rate)/(all_brake_times-1))
            # Vars_brake_boat.append((sqare_rate_all_brake ) / (all_brake_times))
            # Vars_brake_boat.append(all_brake_times)



            ##可以加一些约束条件：
            # 例如公平性：顺序在前的尽量排在闸室中；
            #当船只数量不够时，一刀切之后尽量使得剩余的面积最大（暂时不需要，其它场景需要）

        # result = self.pool.map_async(subAimFunc, args)

        obj1=np.array(Vars_brake_boat).reshape(-1,1) # (4000,)#此处改为闸次最小
       
        pop.ObjV = obj1#计算目标函数值，赋值给pop种群对象的ObjV属性,求矩阵列和，即变量之和
       