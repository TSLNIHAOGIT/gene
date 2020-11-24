# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea # import geatpy
import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..')))
from geatpy_example.frame.schedule_new_same.MyProblem import MyProblem # 导入自定义问题接口
from geatpy_example.frame.schedule_new_same.plot_example import plot_example
from geatpy_example.frame.schedule_new_same.quick_sort_brake import quick_sort_brake
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


def each_brake(each_wait_list,L,W):
    def get_sqare_rate(in_brake_sort, L,W):
        brake_boat=quick_sort_brake(in_brake_sort, L, W)
        s=0
        for k,v in brake_boat.items():
            s=s+v[1][0]*v[1][1]
    
        sqare_rate=s/(L*W)            
        return sqare_rate,brake_boat
    
    
    
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
    myAlgorithm.MAXGEN = 3  # 13 # 最大进化代数
    myAlgorithm.logTras = 1  # 设置每多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）

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



    # best_brake_seq = wait_list[best_sort_sequence]
    # all_brake_boat = {}
    # in_brake_sort = best_brake_seq
    # sqare_rate,brake_boat=get_sqare_rate(in_brake_sort, L,W)
    # brake_num=list(brake_boat.keys())
    # brake_boat={best_sort_sequence[k]:v for k,v in brake_boat.items()}
    # all_brake_boat[0]= {'brake_boat':brake_boat,'best_use_rate':sqare_rate}
    # print('一闸最优解：组合={} \n 面积利用率={}'.format(brake_boat,sqare_rate))
    #
    # each2=np.delete(best_sort_sequence,brake_num,axis=0)
    # in_brake_sort2=np.delete(in_brake_sort,brake_num,axis=0)
    # if len(in_brake_sort2)>0:
    #     sqare_rate2,brake_boat2=get_sqare_rate(in_brake_sort2, L,W)
    #     brake_num2=list(brake_boat2.keys())
    #     #sqare_rate=sqare_rate+sqare_rate2
    #     brake_boat2={each2[k]:v for k,v in brake_boat2.items()}
    #     all_brake_boat[1] = {'brake_boat':brake_boat2,'best_use_rate':sqare_rate2}
    #     print('二闸最优解：组合={} \n 面积利用率={}'.format(brake_boat2,sqare_rate2))
    #
    #     each3=np.delete(each2,brake_num2,axis=0)
    #     in_brake_sort3=np.delete(in_brake_sort2,brake_num2,axis=0)
    #     if len(in_brake_sort3)>0:
    #         sqare_rate3,brake_boat3=get_sqare_rate(in_brake_sort3, L,W)
    #         brake_num3=list(brake_boat3.keys())
    #
    #         brake_boat3={each3[k]:v for k,v in brake_boat3.items()}
    #         all_brake_boat[2] = {'brake_boat':brake_boat3,'best_use_rate':sqare_rate3}#brake_boat3
    #         print('三闸最优解：组合={} \n 面积利用率={}'.format(brake_boat3,sqare_rate3))
    #         #sqare_rate=sqare_rate+sqare_rate3
    # print('all_brake_boat00',all_brake_boat)




    best_brake_seq = wait_list[best_sort_sequence]
    all_brake_boat = {}
    all_brake_times = 0
    in_brake_sort = best_brake_seq
    while True:
        if len(in_brake_sort) > 0 and all_brake_times < 3:
            sqare_rate, brake_boat = get_sqare_rate(in_brake_sort, L, W)
            # 将闸室序号，映射到原始信号

            brake_num = list(brake_boat.keys())

            # 更新in_brake_sort
            ##each2=np.delete(each,brake_num,axis=0)
            in_brake_sort = np.delete(in_brake_sort, brake_num, axis=0)

            brake_boat = {best_sort_sequence[k]: v for k, v in brake_boat.items()}

            best_sort_sequence = np.delete(best_sort_sequence, brake_num, axis=0)

            all_brake_boat[all_brake_times] = {'brake_boat': brake_boat, 'best_use_rate': sqare_rate}

            print('第{}闸最优解：组合={} \n 面积利用率={}'.format(all_brake_times, brake_boat, sqare_rate))


            #绘制并保存图形
            plot_save(brake_boat, all_brake_times)

            all_brake_times = all_brake_times + 1
        else:
            break
    print(' all_brake_boat11', all_brake_boat)
    
    
    
    
    
    
    
    #brake_boat = quick_sort_brake(best_brake_seq, L, W)
    
    ##将快速入闸的顺序，对应到最优选择的顺序
    #brake_boat={best_sort_sequence[k]:v for k,v in brake_boat.items()}
    
    ##将最优选择的顺序，对应到最原始的队列中的序号
    #brake_boat={wait_list_num[k]:v for k,v in brake_boat.items()}
    
    



    print('有效进化代数：%s' % (obj_trace.shape[0]))
    print('最优的一代是第 %s 代' % (best_gen + 1))
    print('评价次数：%s' % (myAlgorithm.evalsNum))
    print('时间已过 %s 秒' % (myAlgorithm.passTime))
    return all_brake_boat

def main(wait_list,L,W):
    all_brake_boat=each_brake(wait_list, L, W)

        
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
    wait_list=np.array([[85.5, 16.3], [99.3, 16.92], [119.53, 22.5], [110.0, 19.22], [110.0, 17.2], [91.07, 18.68], [113.97, 22.33], [92.96, 21.72], [110.52, 16.93], [109.07, 19.81], [92.92, 22.13], [94.3, 22.16], [111.22, 20.09], [129.81, 21.48], [124.6, 20.91], [126.09, 19.62], [93.87, 16.06], [118.79, 17.75], [91.66, 17.91], [115.73, 17.95], [110.82, 22.75], [121.55, 18.56], [111.28, 19.54], [96.35, 19.25], [129.97, 21.96]])

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

