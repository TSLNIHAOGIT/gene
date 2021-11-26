# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea # import geatpy
import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..')))
from geatpy_example.frame.schedule_new_same_brake.MyProblemMultiObjDynamicProcess  import MyProblem # 导入自定义问题接口
from geatpy_example.frame.schedule_new_same_brake.plot_example import plot_example
# from geatpy_example.frame.schedule_new_same_brake.quick_sort_multi_brakes import quick_sort_multi_brakes
# from geatpy_example.frame.schedule_new_same_brake.quick_sort_multi_brakes_complete import quick_sort_multi_brakes
from geatpy_example.frame.schedule_new_same_brake.quick_sort_multi_obj_dynamic_brakes_complete import quick_sort_multi_brakes
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

def get_raw_num_brake_boat( params):
    '''
    顺序对齐
    :return:
    '''
    #最优序列顺序
    best_sort_sequence_=params['best_sort_sequence']
    #闸次数
    brakes=params['brakes']
    #输入的原始序列
    best_brake_seq=params['best_brake_seq']

    all_brake_boat, brakes = quick_sort_multi_brakes(best_brake_seq, brakes=brakes)

    for brake_num, e_brake_boat in all_brake_boat.items():
        brake_boat = e_brake_boat['brake_boat']

        # 将快速入闸的顺序，对应到最优选择的顺序
        brake_boat = {best_sort_sequence_[k]: v for k, v in brake_boat.items()}
        # 将最优选择的顺序，对应到最原始的队列中的序号
        wait_list_num = np.array([i for i in range(len(wait_list))])
        brake_boat = {wait_list_num[k]: v for k, v in brake_boat.items()}
        e_brake_boat['brake_boat'] = brake_boat
    return all_brake_boat


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
    # brakes = {'0': [L, W], '1': [L, W], '2': [L, W],'3': [L, W],'4': [L, W],
    #           '5': [L, W], '6': [L, W], '7': [L, W],
    #           '8': [L, W],'9': [L, W],
    #           '10': [L, W], '11': [L, W], '12': [L, W], '13': [L, W], '14': [L, W],'15': [L, W],
    #           # '16': [L, W],
    #           # '17': [L, W],
    #           # '18': [L, W]
    #           }
    # brakes = {'0': [L, W], '1': [L, W], '2': [L, W]}
    
    wait_list=each_wait_list
    """===============================实例化问题对象==========================="""
    problem = MyProblem(wait_list, brakes=None)  # 生成问题对象
    """=================================种群设置==============================="""
    NIND = 80  # 5000 种群规模
    Encodings = ['RI', 'P']
    Field1 = ea.crtfld(Encodings[0], problem.varTypes[:1], problem.ranges[:, :1], problem.borders[:, :1])
    Field2 = ea.crtfld(Encodings[1], problem.varTypes[1:], problem.ranges[:, 1:], problem.borders[:, 1:])
    Fields = [Field1, Field2]
    population = ea.PsyPopulation(Encodings, Fields, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）

    # Encoding = 'P'  # 编码方式
    # NIND = 120 #5000 种群规模
    # # ranges还是原来的Field会在最后一行加上1
    # Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    # population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    # myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象，单目标模板
    # myAlgorithm=ea.moea_NSGA2_templet(problem, population)  #多目模板
    #混合染色体编码多目标模板
    myAlgorithm=ea.moea_psy_NSGA2_templet(problem, population)
    # myAlgorithm = ea.moea_psy_NSGA3_templet(problem, population)

    myAlgorithm.MAXGEN = 150# 30;13 # 最大进化代数
    # myAlgorithm.recOper = ea.Xovox(XOVR=0.8)  # 设置交叉算子 __init__(self, XOVR=0.7, Half=False)
    # myAlgorithm.mutOper = ea.Mutinv(Pm=0.2)  # 设置变异算子
    myAlgorithm.logTras = 0  # 设置每多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）

    """==========================调用算法模板进行种群进化======================="""
    NDSet=myAlgorithm.run()
    # [population, obj_trace, var_trace] = myAlgorithm.run()  # 执行算法模板
    NDSet.save()  # 把非支配种群的信息保存到文件中
    problem.pool.close()

    print('用时：%f秒' % (myAlgorithm.passTime))
    print('评价次数：%d次' % (myAlgorithm.evalsNum))
    print('非支配个体数：%d个' % (NDSet.sizes))
    print(f'单位时间找到帕累托前沿点个数：{int(NDSet.sizes // myAlgorithm.passTime)}个' )
    # NDSet.ObjV为最优解个体的目标函数值；NDSet.Phen为对应的决策变量值。
    obj_=NDSet.ObjV
    phen_=NDSet.Phen
    # print(f'目标函数最优解：{obj_}')
    # print(f'最优解对应的决策变量：{phen_}')
    data = np.hstack([obj_, phen_])
    data = np.around(data, decimals=10)  #
    obj_sort=sorted(data, key=lambda d: (d[0], d[1]), reverse=True)
    # print(f'obj_sort:{obj_sort}')
    obj_opt=obj_sort[0][:2]
    brakes_num_=obj_sort[0][2:3]
    best_sort_sequence_=obj_sort[0][3:]
    best_sort_sequence_ = [int(each) for each in best_sort_sequence_]
    print(f'obj_opt 0 ={obj_opt}')
    print(f'brakes_num_ 0={brakes_num_}')
    print(f'best_sort_sequence_0={best_sort_sequence_}')

    # all_res = []
    for each in obj_sort:
        ###且闸次数量要小于之前的，否则不加进来
        if (each[0] < obj_opt[0]) and (brakes_num_[0]-each[2:3]==1):
            print(each)
            # all_res.append(each)

            obj_opt_1 = each[:2]
            brakes_num_1 = each[2:3]
            best_sort_sequence_1 = each[3:]
            best_sort_sequence_1 = [int(each_) for each_ in best_sort_sequence_1]
            print(f'obj_opt 1 ={obj_opt_1}')
            print(f'brakes_num_ 1={brakes_num_1}')
            print(f'best_sort_sequence_1={best_sort_sequence_1}')

            brakes1 = {f'{i}': [L, W] for i in range(int(brakes_num_1[0]))}
            best_brake_seq1 = wait_list[best_sort_sequence_1]
            params1 = {'best_sort_sequence': best_sort_sequence_1, 'brakes': brakes1, 'best_brake_seq': best_brake_seq1}
            all_brake_boat1 = get_raw_num_brake_boat(params1)
            print(f'all_brake_boat1={all_brake_boat1}')
            statics_data(all_brake_boat1)
            break

    best_brake_seq = wait_list[best_sort_sequence_]
    brakes = {f'{i}': [L, W] for i in range(int(brakes_num_[0]))}

    params0={'best_sort_sequence':best_sort_sequence_,'brakes':brakes,'best_brake_seq':best_brake_seq}
    all_brake_boat=get_raw_num_brake_boat(params0)




    # best_brake_seq = wait_list[best_sort_sequence_]
    # brakes = {f'{i}': [L, W] for i in range(int(brakes_num_[0]))}
    # all_brake_boat,brakes=quick_sort_multi_brakes(best_brake_seq,brakes=brakes)
    # for brake_num,e_brake_boat in all_brake_boat.items():
    #     brake_boat=e_brake_boat['brake_boat']
    #     # 将快速入闸的顺序，对应到最优选择的顺序
    #     brake_boat = {best_sort_sequence_[k]: v for k, v in brake_boat.items()}
    #     # 将最优选择的顺序，对应到最原始的队列中的序号
    #     wait_list_num = np.array([i for i in range(len(wait_list))])
    #     brake_boat = {wait_list_num[k]: v for k, v in brake_boat.items()}
    #     e_brake_boat['brake_boat']=brake_boat
    # print(' all_brake_boat11', all_brake_boat)
    

    # print('有效进化代数：%s' % (obj_trace.shape[0]))
    # print('最优的一代是第 %s 代' % (best_gen + 1))
    # print('评价次数：%s' % (myAlgorithm.evalsNum))
    # print('时间已过 %s 秒' % (myAlgorithm.passTime))
    return all_brake_boat

def main(wait_list,L,W):
    all_brake_boat=batch_brakes(wait_list, L, W)
    return all_brake_boat


def statics_data(all_brake_boat):
    # # # #绘图
    all_area_ratio = 0
    all_num = 0
    for brake_num, e_brake_boat in all_brake_boat.items():
        area_ratio = one_brake_area_ratio(e_brake_boat['brake_boat'], L, W)
        brake_num = len(e_brake_boat['brake_boat'])
        all_area_ratio = all_area_ratio + area_ratio
        all_num = all_num + brake_num
        print(f'brake_num area_ratio={area_ratio},brake_num={brake_num}')

        # X, Y, li_e, wi_e, N_e=build_plot_para(e_brake_boat['brake_boat'])
        # print('绘图')
        # plot_example(X, Y, li_e, wi_e,N_e)
    print(f'总面积使用率为：{all_area_ratio},总闸次数：{len(all_brake_boat)}，总船数为：{all_num}')
    print(f'平均一个闸室面积使用率为：{all_area_ratio / len(all_brake_boat)},总船数为：{all_num}')



if __name__ == '__main__':
    wait_list = np.array(
        [
         [105.0, 16.0], [110.0, 18.0], [100.0, 17.0], [106.0, 18.0],
         [109.0, 18.0], [130.0, 16],
         [108.0, 18.0], [92.0, 15.0], [110.0, 18.0], [100.0, 18.0], [95.0, 16.0], [110.0, 20.0], [105.0, 17.0],
         [110.0, 18.0], [110.0, 18.0], [108.0, 18.0], [100.0, 17.0], [92.0, 15.0], [105.0, 16.0], [85.0, 15.0],
         [85.0, 14.0], [130.0, 16], [87.0, 15.0], [92.0, 15.0], [87.0, 14.0], [85.0, 14.0], [75.0, 14.0],
         [100.0, 18.0], [80.0, 14.0], [80.0, 14.0], [92.0, 15.0], [95.0, 16.0], [80.0, 14.0], [107.0, 17.0],
         [92.0, 17.0], [87.0, 14.0], [106.0, 17.0], [130.0, 16.0], [93.0, 14.0], [100.0, 17.0], [80.0, 14.0],
         [95.0, 17.0], [75.0, 14.0], [79.0, 13.0], [80.0, 14.0], [77.0, 14.0], [89.0, 15.0], [88.0, 17.0],
         [87.0, 15.0], [92.0, 17.0], [105.0, 16.0], [110.0, 18.0], [100.0, 16.0], [130.0, 16], [110.0, 17.0],
         [87.0, 15.0], [110.0, 18.0], [105.0, 17.0], [85.0, 14.0], [78.0, 14.0], [100.0, 17.0], [107.0, 17.0],
         [92.0, 15.0], [75.0, 13.0], [80.0, 14.0], [90.0, 17.0]
         ])

    wait_list = np.array(
        [
            [87.0, 15.0], [110.0, 18.0], [105.0, 17.0], [85.0, 14.0], [78.0, 14.0], [100.0, 17.0], [107.0, 17.0],[80.0, 14.0],
            [90.0, 17.0]
         ])

    # wait_list=wait_list[6:12]
    # 按照宽度排序，宽的在前么
    # wait_list=sorted(wait_list,key =lambda x:x[1],reverse=True)
    
    #wait_list={index:each for index, each in enumerate(wait_list)}
    # W = 34
    # L = 280

    W = 32.8  # 34 ,32.8
    L =266  # 280,264

    # W=82
    # L=430
    N = len(wait_list)

    print('N', N)
    all_brake_boat=main(wait_list, L, W)
    print(f'brake_num={len(all_brake_boat)},all_brake_boat={all_brake_boat}')
    statics_data(all_brake_boat)


