# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea # import geatpy
import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..')))
from geatpy_example.frame.schedule_new.MyProblem import MyProblem # 导入自定义问题接口
from geatpy_example.frame.schedule_new.plot_example import plot_example
from geatpy_example.frame.schedule_new.quick_sort_brake import quick_sort_brake



def each_brake(each_wait_list,L,W,brake_num,wait_list_num):
    wait_list=each_wait_list
    """===============================实例化问题对象==========================="""
    problem = MyProblem(wait_list, L, W)  # 生成问题对象
    """=================================种群设置==============================="""
    Encoding = 'P'  # 编码方式
    NIND = 6000  # 种群规模
    # ranges还是原来的，Field会在最后一行加上1
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象，单目标模板
    # myAlgorithm=ea.moea_NSGA2_templet(problem, population)  #多目模板
    myAlgorithm.MAXGEN = 13  # 13 # 最大进化代数
    """==========================调用算法模板进行种群进化======================="""
    [population, obj_trace, var_trace] = myAlgorithm.run()  # 执行算法模板
    population.save()  # 把最后一代种群的信息保存到文件中

    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1])  # 记录最优种群个体是在哪一代
    best_ObjV = obj_trace[best_gen, 1]
    print('最优的目标函数值为：%s' % (best_ObjV))
    print('最优的控制变量值为：')

    for i in range(var_trace.shape[1]):  # (MAXGEN,Dim),进化的总代数和决策变量的维度
        print(var_trace[best_gen, i])

    best_sort_sequence = [int(each) for each in var_trace[best_gen]]  # (4000, 12)
    #best_brake_seq={i:wait_list[i] for i in best_sort_sequence}
    best_brake_seq=wait_list[best_sort_sequence]
    brake_boat = quick_sort_brake(best_brake_seq, L, W)
    brake_boat={wait_list_num[k]:v for k,v in brake_boat.items()}

    X = []
    Y = []
    li_e = []
    wi_e = []
    s = 0
    for k, v in brake_boat.items():
        s = s + v[1][0] * v[1][1]

        X.append(v[0][0] / L)
        Y.append(v[0][1] / W)
        li_e.append(v[1][0] / L)
        wi_e.append(v[1][1] / W)
    best_use_rate=s / (L * W)
    print('最优面积利用率',best_use_rate )

    N_e = len(brake_boat)
    plot_example(X, Y, li_e, wi_e, N_e,brake_num=brake_num)
    print('plot finished')

    print('有效进化代数：%s' % (obj_trace.shape[0]))
    print('最优的一代是第 %s 代' % (best_gen + 1))
    print('评价次数：%s' % (myAlgorithm.evalsNum))
    print('时间已过 %s 秒' % (myAlgorithm.passTime))
    return {'brake_boat':brake_boat,'best_use_rate':best_use_rate}

def main(wait_list,L,W):
    wait_list_num=[i for i in range(len(wait_list))]
    all_brake_boat={}
    for brake_num in range(2):
        each_wait_list=wait_list
        best_each_brake=each_brake(each_wait_list,L,W,brake_num,wait_list_num)
        all_brake_boat[brake_num]=best_each_brake
        
        ##去除前面闸次的船只
        #根据索引去除内容
        #wait_list=np.delete(wait_list,list(best_each_brake['brake_boat'].keys()))
        for i in best_each_brake['brake_boat']:
            wait_list=list(wait_list)
            wait_list.pop(i)
            #移除索引
            wait_list_num.remove(i)
        wait_list=np.array(wait_list)
        
    return all_brake_boat




if __name__ == '__main__':
    repeat = 10

    L_r = list(np.random.uniform(85, 130, 20)) * repeat

    W_r = list(np.random.uniform(16, 23, 20)) * repeat

    size_dict = {'1': (85.5, 16.3), '2': (99.3, 16.92), '3': (119.53, 22.5), '4': (110, 19.22), '5': (110, 17.2)}
    wait_list = np.array(list(size_dict.values()) * repeat)

    # 新增随机造的船舶
    wait_list = np.vstack([wait_list, [[round(ll, 2), round(ww, 2)] for ll, ww in zip(L_r, W_r)]])

    # wait_list=wait_list[6:12]
    # 按照宽度排序，宽的在前么
    # wait_list=sorted(wait_list,key =lambda x:x[1],reverse=True)
    
    #wait_list={index:each for index, each in enumerate(wait_list)}
    W = 34
    L = 280
    # W=82
    # L=430
    N = len(wait_list)

    print('N', N)
    all_brake_boat=main(wait_list, L, W)
    print('all_brake_boat',all_brake_boat)

