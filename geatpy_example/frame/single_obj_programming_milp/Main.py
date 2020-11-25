# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea # import geatpy
from geatpy_example.frame.single_obj_programming_milp.MyProblem import MyProblem # 导入自定义问题接口
import pandas as pd
import os
path='./Result'
Chrom_res=pd.read_csv(os.path.join(path,'Chrom.csv'),header=None).to_numpy()
CV_res=pd.read_csv(os.path.join(path,'CV.csv'),header=None).to_numpy()
FitnV_res=pd.read_csv(os.path.join(path,'FitnV.csv'),header=None).to_numpy()
ObjV_res=pd.read_csv(os.path.join(path,'ObjV.csv'),header=None).to_numpy()
Phen_res=pd.read_csv(os.path.join(path,'Phen.csv'),header=None).to_numpy()



if __name__ == '__main__':
    # print(help(ea.crtfld))
    # print(help((ea.Population)))
    # print(help(ea.soea_SEGA_templet))
    """===============================实例化问题对象==========================="""
    problem = MyProblem() # 生成问题对象
    """=================================种群设置==============================="""
    Encoding = 'RI'       # 编码方式
    NIND = 4000            # 种群规模，即4000个个体
    precisions = [6, 6,6]#决策变量的编码精度，表示解码后能表示的决策变量的精度可达到小数点后6位
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) # 创建区域描述器

    #觉得保存下来的最后一代的染色体，可以在这里初始化种群，直接使用，应该是可以的，待会试一下


    # __init__(self, Encoding, Field, NIND, Chrom=None, ObjV=None, FitnV=None, CV=None, Phen=None)
    population = ea.Population(Encoding, Field, NIND,
                               Chrom=Chrom_res, ObjV=ObjV_res, FitnV=FitnV_res, CV=CV_res, Phen=Phen_res
                               ) # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population) # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 10 # 最大进化代数
    """==========================调用算法模板进行种群进化======================="""
    [population, obj_trace, var_trace] = myAlgorithm.run() # 执行算法模板
    population.save() # 把最后一代种群的信息保存到文件中
    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1]) # 记录最优种群个体是在哪一代
    best_ObjV = obj_trace[best_gen, 1]
    print('最优的目标函数值为：%s'%(best_ObjV))
    print('最优的控制变量值为：')
    for i in range(var_trace.shape[1]):
        print(var_trace[best_gen, i])
    print('有效进化代数：%s'%(obj_trace.shape[0]))
    print('最优的一代是第 %s 代'%(best_gen + 1))
    print('评价次数：%s'%(myAlgorithm.evalsNum))
    print('时间已过 %s 秒'%(myAlgorithm.passTime))