# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea # import geatpy
import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..')))
from geatpy_example.frame.schedule.MyProblem import MyProblem,N,li,wi,L,W # 导入自定义问题接口
from geatpy_example.frame.schedule.plot_example import plot_example


if __name__ == '__main__':
    """===============================实例化问题对象==========================="""
    problem = MyProblem() # 生成问题对象
    """=================================种群设置==============================="""
    Encoding = 'RI'       # 编码方式
    NIND = 6000            # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND) # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    # myAlgorithm = ea.soea_SEGA_templet(problem, population) # 实例化一个算法模板对象，单目标模板
    myAlgorithm=ea.moea_NSGA2_templet(problem, population)  #多目模板
    myAlgorithm.MAXGEN = 50 # 最大进化代数
    """==========================调用算法模板进行种群进化======================="""
    [population, obj_trace, var_trace] = myAlgorithm.run() # 执行算法模板
    #population.save() # 把最后一代种群的信息保存到文件中
    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1]) # 记录最优种群个体是在哪一代
    best_ObjV = obj_trace[best_gen, 1]
    print('最优的目标函数值为：%s'%(best_ObjV))
    print('最优的控制变量值为：')
    
    
    for i in range(var_trace.shape[1]):#(MAXGEN,Dim),进化的总代数和决策变量的维度
        print(var_trace[best_gen, i])
        
        
    X=var_trace[best_gen, 0:N]#(4000, 12)
    Y=var_trace[best_gen,N:2*N]#(4000, 12)
    E=var_trace[best_gen,2*N:3*N]#(4000, 12)
    S=var_trace[best_gen,3*N:3*N+N**2].reshape(-1,N,N)#(4000, 12, 12)
    U=var_trace[best_gen,3*N+N**2:].reshape(-1,N,N    )#(4000, 12, 12)
    plot_example(X/L, Y/W, li/L, wi/W,N)
        
    print('有效进化代数：%s'%(obj_trace.shape[0]))
    print('最优的一代是第 %s 代'%(best_gen + 1))
    print('评价次数：%s'%(myAlgorithm.evalsNum))
    print('时间已过 %s 秒'%(myAlgorithm.passTime))