# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea # import geatpy
import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..')))
from geatpy_example.frame.schedule_new_same_brake.MyProblemMultiProcess import MyProblem # 导入自定义问题接口
from geatpy_example.frame.schedule_new_same_brake.plot_example import plot_example
from geatpy_example.frame.schedule_new_same_brake.quick_sort_multi_brakes import quick_sort_multi_brakes
from geatpy_example.frame.schedule_new_same_brake.quick_sort_multi_brakes import build_plot_para,one_brake_area_ratio
import json



def plot_save(brake_boat,brake_num):


    X = []
    Y = []
    li_e = []
    wi_e = []
    s = 0
    for k, v in brake_boat.items():
        s = s + v[1][0] * v[1][1]

        X.append(v[0][0] )
        Y.append(v[0][1] )
        li_e.append(v[1][0] )
        wi_e.append(v[1][1])
    best_use_rate=s / (L * W)
    print('最优面积利用率',best_use_rate )

    N_e = len(brake_boat)
    plot_example(X, Y, li_e, wi_e, N_e,brake_num=brake_num)
    print('plot finished')


def batch_brakes(each_wait_list,L,W):
    # def get_sqare_rate(in_brake_sort, L,W):
    #     brake_boat=quick_sort_brake(in_brake_sort, L, W)
    #     s=0
    #     for k,v in brake_boat.items():
    #         s=s+v[1][0]*v[1][1]
    #
    #     sqare_rate=s/(L*W)
    #     return sqare_rate,brake_boat

    #每个闸次对应的闸室的长宽
    # brakes = {'0': [L, W], '1': [L, W], '2': [L, W],'3': [L, W],'4': [L, W]}
    brakes = {'0': [L, W], '1': [L, W], '2': [L, W]}
    
    wait_list=each_wait_list
    """===============================实例化问题对象==========================="""
    problem = MyProblem(wait_list, brakes=brakes)  # 生成问题对象
    """=================================种群设置==============================="""
    Encoding = 'P'  # 编码方式
    NIND = 5000  # 种群规模
    # ranges还是原来的Field会在最后一行加上1
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象，单目标模板
    # myAlgorithm=ea.moea_NSGA2_templet(problem, population)  #多目模板
    myAlgorithm.MAXGEN = 30# 13 # 最大进化代数
    # myAlgorithm.recOper = ea.Xovox(XOVR=0.8)  # 设置交叉算子 __init__(self, XOVR=0.7, Half=False)
    # myAlgorithm.mutOper = ea.Mutinv(Pm=0.2)  # 设置变异算子
    myAlgorithm.logTras = 1  # 设置每多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）

    """==========================调用算法模板进行种群进化======================="""
    [population, obj_trace, var_trace] = myAlgorithm.run()  # 执行算法模板
    # population.save()  # 把最后一代种群的信息保存到文件中

    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1])  # 记录最优种群个体是在哪一代
    best_ObjV = obj_trace[best_gen, 1]
    print('最优的目标函数值为：%s' % (best_ObjV))
    print('最优的控制变量值为：')

    for i in range(var_trace.shape[1]):  # (MAXGEN,Dim),进化的总代数和决策变量的维度
        print(var_trace[best_gen, i])

    best_sort_sequence = [int(each) for each in var_trace[best_gen]]  # (4000, 12)
    #

    best_brake_seq = wait_list[best_sort_sequence]
    all_brake_boat=quick_sort_multi_brakes(best_brake_seq,brakes)

    for brake_num,e_brake_boat in all_brake_boat.items():
        brake_boat=e_brake_boat['brake_boat']

        # 将快速入闸的顺序，对应到最优选择的顺序
        brake_boat = {best_sort_sequence[k]: v for k, v in brake_boat.items()}
        # 将最优选择的顺序，对应到最原始的队列中的序号
        wait_list_num = np.array([i for i in range(len(wait_list))])
        brake_boat = {wait_list_num[k]: v for k, v in brake_boat.items()}
        e_brake_boat['brake_boat']=brake_boat


    print(' all_brake_boat11', all_brake_boat)
    

    print('有效进化代数：%s' % (obj_trace.shape[0]))
    print('最优的一代是第 %s 代' % (best_gen + 1))
    print('评价次数：%s' % (myAlgorithm.evalsNum))
    print('时间已过 %s 秒' % (myAlgorithm.passTime))
    return all_brake_boat

def main(wait_list,L,W):
    all_brake_boat=batch_brakes(wait_list, L, W)
    return all_brake_boat




if __name__ == '__main__':
    # repeat = 1
    #
    # L_r = list(np.random.uniform(85, 130, 20)) * repeat
    #
    # W_r = list(np.random.uniform(16, 23, 20)) * repeat
    #
    # size_dict = {'1': (85.5, 16.3), '2': (99.3, 16.92), '3': (119.53, 22.5), '4': (110, 19.22), '5': (110, 17.2)}
    # wait_list = np.array(list(size_dict.values()) * repeat)
    #
    # # 新增随机造的船舶
    # wait_list = np.vstack([wait_list, [[round(ll, 2), round(ww, 2)] for ll, ww in zip(L_r, W_r)]])
    # with open('wait_list.json', 'w') as f:
    #     json.dump(wait_list.tolist(), f)
    # wait_list=np.array([[85.5, 16.3], [99.3, 16.92], [119.53, 22.5], [110.0, 19.22], [110.0, 17.2], [91.07, 18.68], [113.97, 22.33], [92.96, 21.72], [110.52, 16.93], [109.07, 19.81], [92.92, 22.13], [94.3, 22.16], [111.22, 20.09], [129.81, 21.48], [124.6, 20.91], [126.09, 19.62], [93.87, 16.06], [118.79, 17.75], [91.66, 17.91], [115.73, 17.95], [110.82, 22.75], [121.55, 18.56], [111.28, 19.54], [96.35, 19.25], [129.97, 21.96]])
 #    wait_list=np.array([(85.5, 16.3),
 # (110.0, 19.22),
 # (119.53, 22.5),
 # (99.0, 17.0),
 # (107.0, 17.0),
 # (108.0, 17.0),
 # (105.0, 16.0),
 # (110.0, 17.0),
 # (109.0, 17.0),
 # (130.0, 16.0),
 # (100.0, 16.0),
 # (106.0, 17.0),
 # (105.0, 17.0),
 # (100.0, 17.0),
 # (99.0, 16.0),
 # (124.3, 16.2),
 # (110.0, 19.0),
 # (107.0, 16.0),
 # (106.0, 16.0),
 # (112.0, 17.0),
 # (110.0, 16.0),
 # (103.0, 16.0),
 # (102.0, 17.0),
 # (158.0, 19.0),
 # (158.0, 17.0),
 # (200.0, 17.0),
 # (104.0, 17.0),
 # (110.0, 17.2)])
    wait_list = np.array(
        [[105.0, 16.0], [110.0, 18.0], [100.0, 17.0], [106.0, 18.0], [109.0, 18.0], [130.0, 17.0],
         [108.0, 18.0], [92.0, 15.0], [110.0, 18.0], [100.0, 18.0], [95.0, 16.0], [110.0, 20.0], [105.0, 17.0],
         [110.0, 18.0], [110.0, 18.0], [108.0, 18.0], [100.0, 17.0], [92.0, 15.0], [105.0, 16.0], [85.0, 15.0],
         [85.0, 14.0], [130.0, 17.0], [87.0, 15.0], [92.0, 15.0], [87.0, 14.0], [85.0, 14.0], [75.0, 14.0],
         [100.0, 18.0], [80.0, 14.0], [80.0, 14.0], [92.0, 15.0], [95.0, 16.0], [80.0, 14.0], [107.0, 17.0],
         [92.0, 17.0], [87.0, 14.0], [106.0, 17.0], [130.0, 16.0], [93.0, 14.0], [100.0, 17.0], [80.0, 14.0],
         [95.0, 17.0], [75.0, 14.0], [79.0, 13.0], [80.0, 14.0], [77.0, 14.0], [89.0, 15.0], [88.0, 17.0],
         [87.0, 15.0], [92.0, 17.0], [105.0, 16.0], [110.0, 18.0], [100.0, 16.0], [130.0, 17.0], [110.0, 17.0],
         [87.0, 15.0], [110.0, 18.0], [105.0, 17.0], [85.0, 14.0], [78.0, 14.0], [100.0, 17.0], [107.0, 17.0],
         [92.0, 15.0], [75.0, 13.0], [80.0, 14.0], [90.0, 17.0]])

    # wait_list=wait_list[6:12]
    # 按照宽度排序，宽的在前么
    # wait_list=sorted(wait_list,key =lambda x:x[1],reverse=True)
    
    #wait_list={index:each for index, each in enumerate(wait_list)}
    # W = 34
    # L = 280

    W = 32.8  # 34
    L = 264  # 280

    # W=82
    # L=430
    N = len(wait_list)

    print('N', N)
    all_brake_boat=main(wait_list, L, W)
    print('all_brake_boat',all_brake_boat)

    # # # #绘图
    all_area_ratio=0
    all_num=0
    for brake_num,e_brake_boat in all_brake_boat.items():
        area_ratio=one_brake_area_ratio(e_brake_boat['brake_boat'], L, W)
        brake_num=len(e_brake_boat['brake_boat'])
        all_area_ratio = all_area_ratio+area_ratio
        all_num = all_num +brake_num
        print(f'brake_num area_ratio={area_ratio},brake_num={brake_num}')

        # X, Y, li_e, wi_e, N_e=build_plot_para(e_brake_boat['brake_boat'])
        # print('绘图')
        # plot_example(X, Y, li_e, wi_e,N_e)
    print(f'总面积使用率为：{all_area_ratio},总船数为：{all_num}')

