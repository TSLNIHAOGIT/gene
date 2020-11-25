# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea # import geatpy
import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..')))
from geatpy_example.frame.schedule_new.MyProblem import MyProblem # 导入自定义问题接口
from geatpy_example.frame.schedule_new.plot_example import plot_example
from geatpy_example.frame.schedule_new.quick_sort_brake import quick_sort_brake
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
    return best_use_rate



def each_brake(each_wait_list,L,W,brake_num,wait_list_num):
    wait_list=each_wait_list
    """===============================实例化问题对象==========================="""
    problem = MyProblem(wait_list, L, W)  # 生成问题对象
    """=================================种群设置==============================="""
    Encoding = 'P'  # 编码方式
    NIND = 6000  #4000,6000 种群规模
    # ranges还是原来的，Field会在最后一行加上1
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象，单目标模板
    # myAlgorithm=ea.moea_NSGA2_templet(problem, population)  #多目模板
    myAlgorithm.MAXGEN = 3  # 13 # 最大进化代数
    myAlgorithm.recOper = ea.Xovox(XOVR=0.8)  # 设置交叉算子 __init__(self, XOVR=0.7, Half=False)
    myAlgorithm.mutOper = ea.Mutinv(Pm=0.2)  # 设置变异算子
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

    print('有效进化代数：%s' % (obj_trace.shape[0]))
    print('最优的一代是第 %s 代' % (best_gen + 1))
    print('评价次数：%s' % (myAlgorithm.evalsNum))
    print('时间已过 %s 秒' % (myAlgorithm.passTime))
    return {'brake_boat':brake_boat,'best_sort_sequence':best_sort_sequence,'best_use_rate':best_use_rate}

def main(wait_list,L,W):
    all_record={}
    
    wait_list_num=np.array([i for i in range(len(wait_list))])
    all_brake_boat={}

    #贪婪的获取多闸次最优组合：即先获取第一闸的最优组合，然后去掉已经组合的内容，将剩下的内容继续进行最优组合以此类推

    #三闸有问题待会调试（后面两闸数据重合）
    for brake_num in range(3):
        # print('brake_num={} \n wait_list shape={}'.format(brake_num,wait_list.shape))
        each_wait_list=wait_list
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
    # repeat = 10
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

    #wait_list=np.array([[85.5, 16.3], [99.3, 16.92], [119.53, 22.5], [110.0, 19.22], [110.0, 17.2], [91.07, 18.68], [113.97, 22.33], [92.96, 21.72], [110.52, 16.93], [109.07, 19.81], [92.92, 22.13], [94.3, 22.16], [111.22, 20.09], [129.81, 21.48], [124.6, 20.91], [126.09, 19.62], [93.87, 16.06], [118.79, 17.75], [91.66, 17.91], [115.73, 17.95], [110.82, 22.75], [121.55, 18.56], [111.28, 19.54], [96.35, 19.25], [129.97, 21.96]])
    wait_list=np.array([[85.5, 16.3], [99.3, 16.92], [119.53, 22.5], [110.0, 19.22], [110.0, 17.2], [107.89, 21.81], [112.59, 19.45], [113.22, 16.63], [115.0, 17.88], [121.51, 22.48], [103.83, 20.82], [111.98, 20.84], [99.14, 20.62], [94.86, 20.49], [94.56, 20.59], [113.72, 18.25], [109.3, 21.56], [128.49, 18.37], [111.43, 22.95], [99.9, 21.06], [109.9, 22.78], [105.04, 17.88], [126.07, 21.29], [102.57, 18.67], [111.29, 22.61]])
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

