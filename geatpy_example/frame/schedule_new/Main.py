# -*- coding: utf-8 -*-
import time
import numpy as np
import geatpy as ea # import geatpy
import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..')))
from geatpy_example.frame.schedule_new.MyProblem import MyProblem # 导入自定义问题接口
from geatpy_example.frame.schedule_new.plot_example import plot_example
from geatpy_example.frame.schedule_new.quick_sort_brake import quick_sort_brake
import json
#geatpy version 2.4.0
np.random.seed(1)###设置随机种子使得每次结果一样

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
    # best_use_rate=s / (L * W)
    best_use_rate = s / (280 * 34 )
    print('最优面积利用率',best_use_rate )

    N_e = len(brake_boat)
    # plot_example(X, Y, li_e, wi_e, N_e,brake_num=brake_num)
    # print('plot finished')
    return best_use_rate



def each_brake(each_wait_list,L,W,brake_num,wait_list_num):
    wait_list=each_wait_list
    """===============================实例化问题对象==========================="""
    problem = MyProblem(wait_list, L, W)  # 生成问题对象
    """=================================种群设置==============================="""
    Encoding = 'P'  # 编码方式
    NIND = 1000  #4000,6000 种群规模3000,3（40左右）
    # ranges还是原来的，Field会在最后一行加上1
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象，单目标模板
    # myAlgorithm=ea.moea_NSGA2_templet(problem, population)  #多目模板
    myAlgorithm.MAXGEN = 20#10# 13 # 最大进化代数#3
    # myAlgorithm.recOper = ea.Xovox(XOVR=0.8)  # 设置交叉算子 __init__(self, XOVR=0.7, Half=False)
    # myAlgorithm.mutOper = ea.Mutinv(Pm=0.2)  # 设置变异算子
    myAlgorithm.logTras = 1  # 设置每多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = False  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 0  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）

    """==========================调用算法模板进行种群进化======================="""
    [population, obj_trace, var_trace] = myAlgorithm.run()  # 执行算法模板
    # population.save()  # 把最后一代种群的信息保存到文件中

    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1])  # 记录最优种群个体是在哪一代
    best_ObjV = obj_trace[best_gen, 1]
    # print('最优的目标函数值为：%s' % (best_ObjV))
    # print('最优的控制变量值为：')

    for i in range(var_trace.shape[1]):  # (MAXGEN,Dim),进化的总代数和决策变量的维度
        print(var_trace[best_gen, i])

    best_sort_sequence = [int(each) for each in var_trace[best_gen]]  # (4000, 12)
    #best_brake_seq={i:wait_list[i] for i in best_sort_sequence}
    best_brake_seq=wait_list[best_sort_sequence]
    #闸次原始顺序
    brake_boat = quick_sort_brake(best_brake_seq, L, W)
    
    # #将快速入闸的顺序，对应到最优选择的顺序
    # brake_boat={best_sort_sequence[k]:v for k,v in brake_boat.items()}
    #
    # #将最优选择的顺序，对应到最原始的队列中的序号
    # brake_boat={wait_list_num[k]:v for k,v in brake_boat.items()}
    
    



    # N_e = len(brake_boat)
    # plot_example(X, Y, li_e, wi_e, N_e,brake_num=brake_num)
    best_use_rate=plot_save(brake_boat, brake_num)
    print('plot finished')

    # print('有效进化代数：%s' % (obj_trace.shape[0]))
    # print('最优的一代是第 %s 代' % (best_gen + 1))
    # print('评价次数：%s' % (myAlgorithm.evalsNum))
    # print('时间已过 %s 秒' % (myAlgorithm.passTime))
    return {'brake_boat':brake_boat,'best_sort_sequence':best_sort_sequence,'best_use_rate':best_use_rate}

def main(wait_list,L,W):
    all_record={}

    wait_list_num=np.array([i for i in range(len(wait_list))])
    all_brake_boat={}

    #贪婪的获取多闸次最优组合：即先获取第一闸的最优组合，然后去掉已经组合的内容，将剩下的内容继续进行最优组合以此类推

    #三闸有问题待会调试（后面两闸数据重合）
    all_break_times=30
    for brake_num in range(all_break_times):
        # print('brake_num={} \n wait_list shape={}'.format(brake_num,wait_list.shape))
        each_wait_list=wait_list
        # print('len={},each_wait_list={}'.format(len(each_wait_list),each_wait_list))
        if len(each_wait_list)<1:
            break
        #每个闸次的原始顺序（每次从零开始排）

        best_each_brake=each_brake(each_wait_list,L,W,brake_num,wait_list_num)

        brake_boat=best_each_brake['brake_boat']
        best_sort_sequence=best_each_brake['best_sort_sequence']

        #将快速入闸的顺序，对应到最优选择的顺序
        brake_boat={best_sort_sequence[k]:v for k,v in brake_boat.items()}

        #将最优选择的顺序，对应到最原始的队列中的序号
        brake_boat={wait_list_num[k]:v for k,v in brake_boat.items()}


        all_brake_boat[brake_num]={'brake_boat':brake_boat,'best_use_rate':best_each_brake['best_use_rate']}#
        
        all_record['each_wait_list_{}'.format(brake_num)]=each_wait_list.tolist()

        #这里相当于一个指针指向wait_list_num的内容，随着他的内容改变，那么all_record的内容也改变,所有要copy
        all_record['wait_list_num_{}'.format(brake_num)]=wait_list_num.copy()
        all_record['best_each_brake_{}'.format(brake_num)]=all_brake_boat[brake_num]
        
        
        ##去除前面闸次的船只
        #根据索引去除内容
        #wait_list=np.delete(wait_list,list(best_each_brake['brake_boat'].keys()))
        #print('wait_list={}\n wait_list_num={} \n all_brake_boat={}'.format(wait_list,wait_list_num,all_brake_boat))
        
        #wait_list=wait_list.tolist()
        #原始闸次序号
        each_brake_num_list=list(best_each_brake['brake_boat'].keys())
        #原始闸次序号对应到最优序列序号
        each_brake_num_list=[best_sort_sequence[k] for k in each_brake_num_list]

        #根据索引序号删除相应的内容
        #这里有问题，wait_list每删除一次索引就会变一次，而这里用的是最原始的wait_list的索引
        #通过最优序列序号进行删除
        wait_list=np.delete(wait_list,each_brake_num_list,axis=0)
        wait_list_num=np.delete(wait_list_num,each_brake_num_list,axis=0)


        all_record['each_brake_num_list_{}'.format(brake_num)] = each_brake_num_list
        all_record['each_wait_list_delete_{}'.format(brake_num)] = wait_list.tolist()


        
    print('all_record',all_record)
    # with open('record.json','w') as f:
    #     json.dump(all_record,f,indent=4,ensure_ascii=False)

    
        
    return all_brake_boat




if __name__ == '__main__':
    W = 32.8#33.5#32.8  # 34
    L = 264  # 280
    s = time.time()
    num_len=10
    # with open('data_label.txt','a+') as f:
    if True:
        for _ in range(1):
            # repeat = 4

            # L_r = list(np.random.uniform(85, 130, num_len)) * repeat
            #
            # W_r = list(np.random.uniform(15, 21, num_len)) * repeat
            # wait_list_generate=[[round(ll, 2), round(ww, 2)] for ll, ww in zip(L_r, W_r)]
            # wait_list=np.array( wait_list_generate)

            # wait_list= np.array([[85.5, 16.3], [85.5, 16.3], [110.0, 19.22], [110.0, 17.0], [110.0, 17.0], [107.0, 17.0], [110.0, 17.0],
            #  [103.0, 16.0], [110.0, 19.22]])
            # wait_list=np.array([ [110.0, 17.0], [110.0, 17.0],[110.0, 17.0], [110.0, 17.0],
            #                      [103.0, 16.0],[103.0, 16.0],[103.0, 16.0],[103.0, 16.0]])

            # wait_list = np.array([(85.5, 16.3),
            #                       (110.0, 19.22),
            #                       (119.53, 22.5),
            #                       (99.0, 17.0),
            #                       (107.0, 17.0),
            #                       (108.0, 17.0),
            #                       (105.0, 16.0),
            #                       (110.0, 17.0),
            #                       (109.0, 17.0),
            #                       (130.0, 16.0),
            #                       (100.0, 16.0),
            #                       (106.0, 17.0),
            #                       (105.0, 17.0),
            #                       (100.0, 17.0),
            #                       (99.0, 16.0),
            #                       (124.3, 16.2),
            #                       (110.0, 19.0),
            #                       (107.0, 16.0),
            #                       (106.0, 16.0),
            #                       (112.0, 17.0),
            #                       (110.0, 16.0),
            #                       (103.0, 16.0),
            #                       (102.0, 17.0),
            #                       (158.0, 19.0),
            #                       (158.0, 17.0),
            #                       (200.0, 17.0),
            #                       (104.0, 17.0),
            #                       (110.0, 17.2),
            #                       (119.53, 22.5),
            #                       (99.0, 17.0),
            #                       (107.0, 17.0),
            #                       (108.0, 17.0),
            #                       (105.0, 16.0),
            #                       (110.0, 17.0),
            #                       (109.0, 17.0),
            #                       (130.0, 16.0),
            #                       (100.0, 16.0),
            #                       (106.0, 17.0),
            #                       (105.0, 17.0),
            #                       (100.0, 17.0),
            #                       (99.0, 16.0),
            #                       (124.3, 16.2),
            #                       ])
            ##
            # wait_list=np.array([[110.0, 16.0], [110.0, 17.0], [105.0, 17.0], [105.0, 16.0], [116.0, 18.0], [85.0, 14.0], [100.0, 17.0], [98.0, 17.0], [87.0, 14.0], [87.0, 14.0], [87.0, 14.0], [87.0, 15.0], [87.0, 14.0], [86.0, 14.0], [90.0, 16.0], [100.0, 17.0], [100.0, 17.0], [87.0, 15.0], [87.0, 15.0], [105.0, 16.0], [105.0, 16.0], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [92.0, 15.0], [92.0, 16.0], [92.0, 16.0], [110.0, 19.0], [83.0, 14.0], [110.0, 19.0], [110.0, 19.0], [99.0, 16.0], [99.0, 16.0], [87.0, 14.0], [79.0, 13.0], [85.0, 15.0], [88.0, 14.0], [80.0, 14.0], [80.0, 14.0], [79.0, 13.0], [80.0, 13.0], [105.0, 17.0], [105.0, 16.0], [100.0, 17.0], [92.0, 14.0], [92.0, 15.0], [78.0, 14.0], [80.0, 14.0], [57.0, 10.0], [80.0, 13.0], [105.0, 17.0], [105.0, 16.0], [87.0, 14.0], [110.0, 19.0], [106.0, 18.0], [79.0, 14.0], [99.0, 16.0], [92.0, 15.0], [107.0, 14.0], [108.0, 17.0], [105.0, 17.0], [111.0, 20.0], [80.0, 14.0], [65.0, 12.0], [108.0, 17.0], [90.0, 14.0], [78.0, 14.0], [110.0, 19.0], [99.0, 16.0], [103.0, 16.0], [86.0, 14.0], [100.0, 16.0], [100.0, 16.0], [100.0, 17.0], [105.0, 16.0], [100.0, 16.0], [98.0, 16.0], [92.0, 16.0], [80.0, 14.0], [105.0, 16.0], [77.0, 13.0], [87.0, 15.0], [105.0, 16.0], [86.0, 15.0], [80.0, 13.0], [90.0, 16.0], [102.0, 16.0], [90.0, 15.0], [100.0, 16.0], [87.0, 17.0], [90.0, 15.0], [110.0, 19.0], [92.0, 15.0], [86.0, 16.0], [79.0, 13.0], [108.0, 17.0], [92.0, 16.0], [85.0, 14.0], [80.0, 15.0], [86.0, 14.0], [100.0, 16.0], [84.0, 14.0], [110.0, 19.0], [110.0, 19.0], [100.0, 16.0], [80.0, 14.0], [100.0, 16.0], [110.0, 19.0], [94.0, 16.0], [110.0, 19.0], [80.0, 14.0], [110.0, 17.0], [92.0, 16.0], [80.0, 14.0], [91.0, 15.0], [90.0, 15.0], [86.0, 14.0], [110.0, 19.0], [80.0, 14.0], [110.0, 19.0], [106.0, 17.0], [106.0, 17.0], [108.0, 17.0], [105.0, 16.0], [61.0, 14.0], [100.0, 16.0]])
            # total
            wait_list=np.array([[100.0, 16.0], [92.0, 16.2], [104.8, 16.24], [110.0, 17.2], [109.7, 16.24], [108.0, 17.25], [100.0, 16.0], [86.48, 14.24], [89.9, 15.0], [102.0, 16.24], [104.98, 16.23], [99.9, 16.24], [129.98, 16.23], [129.9, 16.24], [86.8, 16.2], [100.02, 17.63], [99.8, 16.24], [86.8, 14.83], [82.0, 14.03], [92.0, 14.83], [98.8, 16.2], [93.82, 16.2], [86.8, 16.23], [87.0, 14.83], [100.0, 17.23], [109.9, 17.24], [108.0, 17.25], [89.8, 14.8], [89.8, 16.04], [110.0, 19.25], [100.0, 16.0], [99.8, 16.23], [111.0, 18.0], [129.92, 16.24], [110.0, 19.25], [130.0, 16.0], [130.0, 16.0], [130.0, 16.0], [80.0, 13.63], [129.98, 16.26], [105.0, 16.0], [104.98, 16.23], [91.0, 15.0], [86.8, 16.23], [129.98, 16.23], [56.8, 10.0], [108.0, 17.25], [110.0, 16.0], [105.0, 16.23], [100.0, 17.23], [95.0, 16.23], [110.0, 19.2], [99.8, 16.05], [129.9, 16.25], [99.8, 16.05], [79.6, 13.63], [100.0, 16.0], [130.0, 16.0], [130.0, 16.0], [108.0, 17.0], [80.0, 14.0], [86.8, 15.04], [99.8, 16.25], [61.0, 14.0], [86.86, 13.64], [99.8, 16.21], [76.7, 12.0], [110.0, 19.25], [92.0, 16.24], [92.0, 16.24], [99.8, 16.25], [90.0, 16.2], [99.8, 16.25], [106.0, 17.25], [92.0, 14.84], [99.8, 16.25], [91.3, 14.8], [92.0, 16.2], [99.8, 16.25], [105.0, 17.24], [95.0, 16.2], [105.0, 16.23], [92.0, 16.23], [110.0, 19.25], [105.0, 17.2], [79.6, 13.6], [110.0, 19.2], [79.6, 13.62], [108.0, 17.2], [65.5, 10.83], [87.0, 14.83], [68.0, 11.15], [92.0, 14.83], [98.9, 16.28], [78.0, 13.6], [92.0, 14.85], [110.0, 19.26], [86.48, 14.24], [110.0, 19.0], [88.0, 14.0], [105.0, 16.0], [79.8, 13.6], [129.97, 16.2], [130.0, 16.0], [109.8, 19.25], [90.0, 15.0], [99.8, 16.23], [105.0, 16.0], [108.0, 17.25], [107.0, 17.24], [78.0, 13.64], [110.0, 17.2], [107.0, 17.24], [99.6, 16.24], [112.0, 17.2], [110.0, 16.0], [104.81, 16.23], [85.28, 14.23], [80.0, 13.63], [80.0, 13.63], [105.0, 16.0], [104.81, 16.23], [99.6, 16.2], [105.0, 17.2], [99.8, 16.24], [110.0, 19.25], [78.0, 14.0], [99.6, 16.23], [89.8, 14.84], [110.0, 19.2], [129.97, 16.24], [129.97, 16.2], [110.0, 19.25], [57.6, 11.9], [80.0, 14.0], [87.0, 14.83], [100.2, 17.23], [86.48, 14.24], [110.0, 19.25], [65.5, 10.83], [79.6, 13.63], [80.0, 13.0], [85.32, 14.16], [79.58, 13.8], [90.45, 14.83], [106.0, 17.25], [106.0, 17.25], [109.88, 19.25], [104.9, 16.23], [84.9, 14.03], [90.8, 14.84], [90.8, 14.84], [82.0, 14.24], [92.0, 16.24], [92.0, 14.8], [110.0, 19.28], [79.6, 13.63], [104.88, 16.23], [107.0, 14.0], [99.8, 16.3], [80.0, 13.22], [79.78, 13.22], [87.0, 13.6], [87.0, 13.62], [87.0, 14.83], [87.0, 14.8], [109.42, 17.2], [79.0, 13.0], [105.0, 16.0], [110.0, 19.26], [110.0, 19.24], [110.0, 19.2], [110.0, 19.2], [82.3, 14.32], [87.8, 14.82], [104.8, 16.23], [105.0, 16.25], [99.8, 16.25], [88.0, 16.23], [105.0, 16.25], [86.0, 14.0], [86.8, 14.04], [104.88, 16.24], [80.0, 14.0], [92.0, 14.83], [64.9, 11.5], [99.8, 16.25], [100.0, 16.0], [86.8, 14.24], [86.0, 14.0], [78.0, 13.63], [82.0, 14.0], [87.0, 14.0], [88.0, 14.0], [108.8, 17.25], [130.0, 16.0], [86.0, 15.0], [106.8, 16.25], [105.0, 16.24], [106.0, 17.28], [106.0, 17.25], [99.8, 16.25], [90.8, 14.84], [110.0, 19.2], [110.0, 19.2], [86.8, 16.3], [79.6, 13.6], [79.6, 13.6], [79.6, 13.62], [79.6, 13.6], [92.0, 16.23], [99.8, 16.24], [105.0, 16.24], [105.0, 16.2], [79.6, 13.6], [79.6, 13.6], [99.0, 16.0], [79.0, 13.0], [110.0, 17.0], [105.0, 17.0], [92.0, 16.0], [92.0, 16.0], [110.0, 17.0], [110.0, 17.0], [80.0, 14.0], [89.0, 15.0], [105.02, 16.23], [92.0, 14.84], [88.0, 14.0], [100.0, 17.23], [100.0, 17.2], [100.0, 17.23], [100.0, 17.23], [75.7, 13.12], [74.3, 13.64], [87.0, 14.0], [85.0, 14.03], [82.0, 14.04], [107.0, 17.24], [110.0, 17.0], [90.0, 15.0], [105.0, 17.2], [104.81, 16.23], [129.98, 16.26], [129.98, 16.26], [84.0, 14.0], [92.0, 14.8], [99.6, 16.7], [104.98, 16.24], [110.0, 19.2], [92.0, 16.2], [99.8, 16.2], [87.0, 15.0], [79.6, 13.63], [83.0, 14.0]])
            # scheduled_total
            wait_list=np.array([[110.0, 19.25], [110.0, 19.24], [99.0, 16.0], [99.8, 16.25], [106.0, 17.28], [110.0, 19.25], [87.0, 14.83], [105.0, 16.0], [79.6, 13.6], [105.0, 17.0], [110.0, 19.2], [110.0, 19.28], [109.7, 16.24], [130.0, 16.0], [87.3, 13.23], [83.0, 13.84], [84.9, 14.03], [90.45, 14.83], [79.0, 13.0], [80.0, 13.0], [87.0, 15.0], [105.02, 16.23], [80.0, 13.22], [78.0, 13.64], [76.7, 12.0], [109.8, 19.25], [92.0, 16.0], [129.97, 16.24], [92.0, 16.23], [105.0, 17.2], [92.0, 14.83], [92.0, 14.8], [79.6, 13.62], [105.0, 16.2], [87.0, 14.82], [87.0, 13.62], [78.0, 14.0], [107.0, 14.0], [108.0, 17.0], [87.8, 14.63], [130.0, 16.0], [99.8, 16.24], [105.0, 16.0], [105.0, 16.25], [108.0, 17.25], [99.8, 16.23], [94.8, 16.23], [85.0, 14.83], [86.48, 14.24], [89.8, 16.04], [86.48, 14.24], [110.0, 17.2], [129.9, 16.25], [80.0, 14.0], [86.8, 14.24], [79.6, 13.6], [64.9, 11.5], [92.0, 16.2], [104.98, 16.23], [105.0, 16.23], [129.98, 16.26], [108.0, 17.25], [110.0, 19.2], [79.78, 13.22], [65.5, 10.83], [105.02, 16.23], [100.2, 17.23], [100.0, 16.0], [90.8, 14.84], [110.0, 19.26], [110.0, 19.25], [110.0, 19.2], [110.0, 19.2], [99.8, 16.05], [99.8, 16.25], [99.8, 16.25], [86.8, 16.23], [79.6, 13.6], [89.8, 14.8], [110.0, 19.2], [110.0, 19.25], [105.0, 16.23], [87.0, 14.83], [85.28, 14.23], [86.8, 14.04], [80.0, 13.08], [92.0, 14.84], [87.8, 14.82], [86.0, 14.0], [100.0, 16.0], [92.0, 16.24], [102.0, 16.24], [86.0, 15.0], [89.8, 14.84], [108.0, 17.25], [86.8, 16.3], [100.0, 16.0], [98.8, 16.2], [87.0, 14.83], [79.6, 13.6], [84.0, 14.0], [107.0, 17.24], [92.0, 16.2], [106.0, 17.25], [104.81, 16.23], [99.8, 16.25], [92.0, 16.2], [100.0, 16.0], [112.0, 17.2], [99.6, 16.7], [92.0, 16.24], [99.8, 16.2], [86.86, 13.64], [100.0, 17.23], [93.82, 16.2], [80.0, 14.0], [80.0, 14.0], [80.0, 13.63], [80.0, 13.63], [110.0, 17.0], [92.0, 14.83], [99.8, 16.25], [108.0, 17.25], [110.0, 17.0], [110.0, 18.0], [110.0, 19.25], [106.0, 17.25], [106.8, 16.25], [95.0, 16.23], [87.0, 13.6], [110.0, 17.0], [75.7, 13.12], [130.0, 16.0], [110.0, 17.2], [105.0, 17.2], [110.0, 19.2], [92.0, 14.83], [99.9, 16.24], [99.8, 16.3], [86.48, 14.24], [85.32, 14.16], [79.0, 13.0], [86.8, 16.23], [82.0, 14.04], [99.8, 16.25], [85.0, 14.03], [87.0, 14.8], [79.6, 13.63], [79.8, 13.6], [129.97, 16.2], [92.0, 14.85], [86.0, 14.0], [108.0, 17.2], [79.6, 13.6], [99.8, 16.21], [88.0, 14.0], [129.98, 16.26], [87.0, 14.0], [99.8, 16.25], [100.0, 16.0], [105.0, 16.0], [65.5, 10.83], [87.0, 14.83], [87.0, 13.62], [78.0, 13.63], [79.6, 13.62], [130.0, 16.0], [90.8, 14.84], [99.8, 16.24], [90.0, 15.0], [105.0, 16.0], [82.0, 14.0], [105.0, 17.24], [110.0, 16.0], [107.0, 17.24], [105.0, 16.0], [104.81, 16.23], [110.0, 19.2], [100.0, 17.2], [86.8, 14.83], [105.0, 16.24], [79.58, 13.8], [129.92, 16.24], [107.0, 17.24], [99.8, 16.25], [86.0, 14.0], [74.3, 13.64], [99.6, 16.24], [87.0, 14.0], [99.6, 16.23]])
            wait_list=np.array([[105.0, 16.0], [110.0, 18.0], [100.0, 17.0], [106.0, 18.0], [109.0, 18.0], [130.0, 16.2], [108.0, 18.0],
              [92.0, 15.0], [110.0, 18.0], [100.0, 18.0], [95.0, 16.0], [110.0, 20.0], [105.0, 17.0], [110.0, 18.0],
              [110.0, 18.0], [108.0, 18.0], [100.0, 17.0], [92.0, 15.0], [105.0, 16.0], [85.0, 15.0], [85.0, 14.0],
              [130.0, 16.2], [87.0, 15.0], [92.0, 15.0], [87.0, 14.0], [85.0, 14.0], [75.0, 14.0], [100.0, 18.0],
              [80.0, 14.0], [80.0, 14.0], [92.0, 15.0], [95.0, 16.0], [80.0, 14.0], [107.0, 17.0], [92.0, 17.0],
              [87.0, 14.0], [106.0, 17.0], [130.0, 16.0], [93.0, 14.0], [100.0, 17.0], [80.0, 14.0], [95.0, 17.0],
              [75.0, 14.0], [79.0, 13.0], [80.0, 14.0], [77.0, 14.0], [89.0, 15.0], [88.0, 17.0], [87.0, 15.0],
              [92.0, 17.0], [105.0, 16.0], [110.0, 18.0], [100.0, 16.0], [130.0, 16.2], [110.0, 17.0], [87.0, 15.0],
              [110.0, 18.0], [105.0, 17.0], [85.0, 14.0], [78.0, 14.0], [100.0, 17.0], [107.0, 17.0], [92.0, 15.0],
              [75.0, 13.0], [80.0, 14.0], [90.0, 17.0]])
            # day25
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
            wait_list=np.array([[95., 16.],
                        [92., 17.],
                        [88., 17.]])
            # wait_list = np.array([[105.0, 16.0], [110.0, 18.0]])
            # #sheet1
            # wait_list=np.array([[110.0, 19.25], [110.0, 19.24], [99.0, 16.0], [99.8, 16.25], [106.0, 17.28], [110.0, 19.25], [87.0, 14.83], [105.0, 16.0], [79.6, 13.6], [105.0, 17.0], [110.0, 19.2], [110.0, 19.28], [109.7, 16.24], [130.0, 16.0], [87.3, 13.23], [83.0, 13.84], [84.9, 14.03], [90.45, 14.83], [79.0, 13.0], [80.0, 13.0], [87.0, 15.0], [105.02, 16.23], [80.0, 13.22], [78.0, 13.64], [76.7, 12.0], [109.8, 19.25], [92.0, 16.0], [129.97, 16.24], [92.0, 16.23], [105.0, 17.2], [92.0, 14.83], [92.0, 14.8], [79.6, 13.62], [105.0, 16.2], [87.0, 14.82], [87.0, 13.62], [78.0, 14.0], [107.0, 14.0], [108.0, 17.0], [87.8, 14.63], [130.0, 16.0], [99.8, 16.24], [105.0, 16.0], [105.0, 16.25], [108.0, 17.25], [99.8, 16.23], [94.8, 16.23], [85.0, 14.83], [86.48, 14.24], [89.8, 16.04], [86.48, 14.24], [110.0, 17.2], [129.9, 16.25], [80.0, 14.0], [86.8, 14.24], [79.6, 13.6], [64.9, 11.5]])
            # #sheet2
            # wait_list=np.array([[92.0, 16.2], [104.98, 16.23], [105.0, 16.23], [129.98, 16.26], [108.0, 17.25], [110.0, 19.2], [79.78, 13.22], [65.5, 10.83], [105.02, 16.23], [100.2, 17.23], [100.0, 16.0], [90.8, 14.84], [110.0, 19.26], [110.0, 19.25], [110.0, 19.2], [110.0, 19.2], [99.8, 16.05], [99.8, 16.25], [99.8, 16.25], [86.8, 16.23], [79.6, 13.6], [89.8, 14.8], [110.0, 19.2], [110.0, 19.25], [105.0, 16.23], [87.0, 14.83], [85.28, 14.23], [86.8, 14.04], [80.0, 13.08], [92.0, 14.84], [87.8, 14.82], [86.0, 14.0], [100.0, 16.0], [92.0, 16.24], [102.0, 16.24], [86.0, 15.0], [89.8, 14.84], [108.0, 17.25], [86.8, 16.3], [100.0, 16.0], [98.8, 16.2], [87.0, 14.83], [79.6, 13.6], [84.0, 14.0], [107.0, 17.24], [92.0, 16.2], [106.0, 17.25], [104.81, 16.23], [99.8, 16.25], [92.0, 16.2], [100.0, 16.0], [112.0, 17.2], [99.6, 16.7], [92.0, 16.24], [99.8, 16.2], [86.86, 13.64], [100.0, 17.23], [93.82, 16.2], [80.0, 14.0], [80.0, 14.0], [80.0, 13.63], [80.0, 13.63]])
            # ##sheet3
            # wait_list=np.array([[110.0, 17.0], [92.0, 14.83], [99.8, 16.25], [108.0, 17.25], [110.0, 17.0], [110.0, 18.0], [110.0, 19.25], [106.0, 17.25], [106.8, 16.25], [95.0, 16.23], [87.0, 13.6], [110.0, 17.0], [75.7, 13.12], [130.0, 16.0], [110.0, 17.2], [105.0, 17.2], [110.0, 19.2], [92.0, 14.83], [99.9, 16.24], [99.8, 16.3], [86.48, 14.24], [85.32, 14.16], [79.0, 13.0], [86.8, 16.23], [82.0, 14.04], [99.8, 16.25], [85.0, 14.03], [87.0, 14.8], [79.6, 13.63], [79.8, 13.6], [129.97, 16.2], [92.0, 14.85], [86.0, 14.0], [108.0, 17.2], [79.6, 13.6], [99.8, 16.21], [88.0, 14.0], [129.98, 16.26], [87.0, 14.0], [99.8, 16.25], [100.0, 16.0], [105.0, 16.0], [65.5, 10.83], [87.0, 14.83], [87.0, 13.62], [78.0, 13.63], [79.6, 13.62], [130.0, 16.0], [90.8, 14.84], [99.8, 16.24], [90.0, 15.0], [105.0, 16.0], [82.0, 14.0], [105.0, 17.24], [110.0, 16.0], [107.0, 17.24], [105.0, 16.0], [104.81, 16.23], [110.0, 19.2], [100.0, 17.2], [86.8, 14.83], [105.0, 16.24], [79.58, 13.8], [129.92, 16.24], [107.0, 17.24], [99.8, 16.25], [86.0, 14.0], [74.3, 13.64], [99.6, 16.24], [87.0, 14.0], [99.6, 16.23]])
            print(' wait_list={}'.format( wait_list))
            #
            # size_dict = {'1': (85.5, 16.3), '2': (99.3, 16.92), '3': (119.53, 22.5), '4': (110, 19.22), '5': (110, 17.2)}
            # wait_list = np.array(list(size_dict.values()) * repeat)
            #
            # # 新增随机造的船舶
            # wait_list = np.vstack([wait_list, [[round(ll, 2), round(ww, 2)] for ll, ww in zip(L_r, W_r)]])
            # with open('wait_list.json', 'w') as f:
            #     json.dump(wait_list.tolist(), f)

            #wait_list=np.array([[85.5, 16.3], [99.3, 16.92], [119.53, 22.5], [110.0, 19.22], [110.0, 17.2], [91.07, 18.68], [113.97, 22.33], [92.96, 21.72], [110.52, 16.93], [109.07, 19.81], [92.92, 22.13], [94.3, 22.16], [111.22, 20.09], [129.81, 21.48], [124.6, 20.91], [126.09, 19.62], [93.87, 16.06], [118.79, 17.75], [91.66, 17.91], [115.73, 17.95], [110.82, 22.75], [121.55, 18.56], [111.28, 19.54], [96.35, 19.25], [129.97, 21.96]])
            #wait_list=np.array([[85.5, 16.3], [99.3, 16.92], [119.53, 22.5], [110.0, 19.22], [110.0, 17.2], [107.89, 21.81], [112.59, 19.45], [113.22, 16.63], [115.0, 17.88], [121.51, 22.48], [103.83, 20.82], [111.98, 20.84], [99.14, 20.62], [94.86, 20.49], [94.56, 20.59], [113.72, 18.25], [109.3, 21.56], [128.49, 18.37], [111.43, 22.95], [99.9, 21.06], [109.9, 22.78], [105.04, 17.88], [126.07, 21.29], [102.57, 18.67], [111.29, 22.61]])
            # wait_list = np.array(
            #     [[85.5, 16.3], [99.3, 16.92], [119.53, 22.5], [110.0, 19.22], [110.0, 17.2], [91.07, 18.68], [113.97, 22.33],
            #      [92.96, 21.72], [110.52, 16.93], [109.07, 19.81], [92.92, 22.13], [94.3, 22.16], [111.22, 20.09],
            #      [129.81, 21.48], [124.6, 20.91], [126.09, 19.62], [93.87, 16.06], [118.79, 17.75], [91.66, 17.91],
            #      [115.73, 17.95], [110.82, 22.75], [121.55, 18.56], [111.28, 19.54], [96.35, 19.25], [129.97, 21.96]])
            #
            # wait_list=wait_list[3:9]
            # 按照宽度排序，宽的在前么
            # wait_list=sorted(wait_list,key =lambda x:x[1],reverse=True)

            #wait_list={index:each for index, each in enumerate(wait_list)}

            # W=82
            # L=430
            N = len(wait_list)

            print('N', N)
            all_brake_boat=main(wait_list, L, W)
            # f.write(str({'wait_list':wait_list.tolist(),'brake_boat':all_brake_boat[0]['brake_boat'],'best_use_rate':all_brake_boat[0]['best_use_rate']})+'\n')


            print('all_brake_boat',all_brake_boat)
            all_area_ratio=[]
            all_num=0
            for k,v in all_brake_boat.items():
                area_ratio = v['best_use_rate']
                brake_num = len(v['brake_boat'])

                all_num = all_num + brake_num
                print(f'局部brake_num:{k},area_ratio:{area_ratio},brake_num={brake_num}')
                all_area_ratio.append(area_ratio)
            print(f'总面积利用率：{sum(all_area_ratio)}')



            '''
            {
            0: {
                'brake_boat': {
                    202: [(0, 0), (91.91, 16.91)],
                    209: [(91.91, 0), (87.97, 17.53)],
                    26: [(179.88, 0), (99.3, 16.92)],
                    122: [(0, 16.91), (91.91, 16.91)],
                    21: [(179.88, 16.92), (99.3, 16.92)],
                    35: [(91.91, 17.53), (85.5, 16.3)]
                },
                'best_use_rate': 0.9878647373949582
            },
            1: {
                'brake_boat': {
                    109: [(0, 0), (87.97, 17.53)],
                    162: [(87.97, 0), (91.91, 16.91)],
                    0: [(0, 17.53), (85.5, 16.3)],
                    82: [(87.97, 16.91), (91.91, 16.91)],
                    16: [(179.88, 0), (99.3, 16.92)],
                    41: [(179.88, 16.92), (99.3, 16.92)]
                },
                'best_use_rate': 0.987864737394958
            }
        }
        
        
        {
            0: {
                'brake_boat': {
                    35: [(0, 0), (85.5, 16.3)],
                    40: [(0, 16.3), (85.5, 16.3)],
                    207: [(85.5, 0), (106.26, 16.58)],
                    20: [(85.5, 16.58), (85.5, 16.3)],
                    127: [(171.0, 16.58), (106.26, 16.58)],
                    30: [(191.76, 0), (85.5, 16.3)]
                },
                'best_use_rate': 0.9556913445378151
            },
            1: {
                'brake_boat': {
                    227: [(0, 0), (106.26, 16.58)],
                    45: [(0, 16.58), (85.5, 16.3)],
                    147: [(85.5, 16.58), (106.26, 16.58)],
                    25: [(106.26, 0), (85.5, 16.3)],
                    15: [(191.76, 0), (85.5, 16.3)],
                    0: [(191.76, 16.3), (85.5, 16.3)]
                },
                'best_use_rate': 0.9556913445378151
            }
        }
        
        
        {
            0: {
                'brake_boat': {
                    130: [(0, 0), (86.43, 17.56)],
                    10: [(0, 17.56), (85.5, 16.3)],
                    190: [(86.43, 0), (86.43, 17.56)],
                    35: [(85.5, 17.56), (85.5, 16.3)],
                    26: [(172.86, 0), (99.3, 16.92)],
                    21: [(172.86, 16.92), (99.3, 16.92)]
                },
                'best_use_rate': 0.9646043697478992
            },
            1: {
                'brake_boat': {
                    230: [(0, 0), (86.43, 17.56)],
                    0: [(0, 17.56), (85.5, 16.3)],
                    210: [(86.43, 0), (86.43, 17.56)],
                    11: [(172.86, 0), (99.3, 16.92)],
                    40: [(85.5, 17.56), (85.5, 16.3)],
                    46: [(172.86, 16.92), (99.3, 16.92)]
                },
                'best_use_rate': 0.9646043697478992
            }
        }
            '''
        print('time cost={}s'.format(time.time()-s))

