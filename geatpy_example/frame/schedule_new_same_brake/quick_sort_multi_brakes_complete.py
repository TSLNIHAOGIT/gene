#encoding=utf-8
import os ,sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..')))
from geatpy_example.frame.schedule_new_same_brake.plot_example import plot_example
import random
import numpy as np
np.random.seed(1001)
import time
from app_logging import get_logger
logger = get_logger()


###############结合遗传算法基本思想
'''
快速只排一个闸室：可行解，选排列
（1）一开始的想法，例如共12艘船，然后遗传算法每次随机选取其中的6艘进行排列，每次只计算这6艘船的适应度函数，进行优化

（2）随机取6艘船固定下来，然后进行全排列，计算完所有6艘船的适应度函数；遗传算法学到的是如何排列该6艘船
     https://blog.csdn.net/u011000290/article/details/46838079
快速同时排多个闸室：可行解，选排列
（1）假设一共需要排n个闸次，那么从总船队列中选择6*n个船进行选排列（若总数小于6*n则直接全排列），然后计算这6*n个船的适应度函数
（2）随机取6*n艘船固定下来，然后进行全排列，计算完所有6*n艘船的适应度函数；遗传算法学到的是如何排列该6*n艘船

大的逻辑为：对于某个船队列6*n,依顺序选第一艘船放入第一个闸室，第二艘船放入第二个闸室，第三艘船放入第三个闸室，
依次类推，每个闸室都放了一艘船之后，又从第一艘船开始放，如果某艘船在当前闸室可排点均放不下，则尝试下一个闸室可排点，直到能放下，
如果所有闸室可排点均放不下，则放弃该条船

即对于当前待排的一艘船，先试第一个闸室的所有可排点，直到能放下；否则尝试第二个闸室的所有可排点，直到能放下；
依次类推，如果所有闸室的所有可排点均放不下，则舍弃该船。

程序实现逻辑：
1.遍历船队列中的每一艘船
2.对应当前的船，选择某个闸室来排：按照每个闸室剩余面积占比归一化的概率选择对应的闸室【如果闸室中无可排点，认为剩余可用面积占归一化概率为0】
3.判断该船能否放在选择的闸室中
  3.1 如果能放入该闸室就放进去，重复1、2
  3.2 如果不能放入该闸室，就从剩下的闸室中按照2的方法选择闸室再放，直到放下；或者所有闸室可排点都无法满足要求，那么就放弃该船
4.直到船队列排完或者所有闸室没有可排点就结束

【待优化】放弃船问题，以及闸室无可排点问题；
按照概率分布选择，可以改成按照最大概率选择的问题【这一步非常重要，之前按照概率分布效果一直很差，改成按照最大概率效果一下子就上去了】

'''



#判断能否放下该船
def judge_put(xi,yi,li,wi,L,W):
    if (xi+li<=L) and (yi+wi)<=W:
        return True
    else:
        return False
#判断船之间不重叠：
def judge_overlab(xi,yi,li,wi,xj,yj,lj,wj):
    if (xi+li<=xj) or (xj+lj<=xi) or (yi+wi<=yj) or (yj+wj<=yi):
        return True
    else:
        return False

def softmax_1d(data):
    data=np.array(data)
    # logger.debug(f'data for softmax={data}')
    # print(f'data to softmax={data}')
    ##数值为0的输出概率也把变成零了
    data[data<=0]=-np.inf
    # print(f'data after for softmax={data}')
    soft_res=np.exp(data) / sum(np.exp(data))
    # print(f'soft_res={soft_res}')
    return soft_res
def one_brake_area_ratio(brake_boat,L,W):
    '''
    :param brake_boat: 闸室船舶信息
    :param L: 闸室长
    :param W: 闸室宽
    :return: 闸室面积利用率
    '''
    s=0
    for k,v in brake_boat.items():
        s=s+v[1][0]*v[1][1]
    return s/(L*W)

def all_remaining_brake_area_ratio(params):
    # 【这里本质上是选择闸室，然后放置船舶】
    # 按照剩余闸室面积占比选择闸室，然后向闸室中放置船舶，觉得这样比较合理，当闸室剩余面积小到连最小的船都放不下了，选择的概率就为0
    # 从队列中按照概率来选,根据每个闸室的剩余面积占比，进行softmax归一化计算选择闸室的概率，如果剩余面积小于一定阈值(没有可排点时)，就把直接改成0，表示不会在选该闸室
    # choice_break=np.random.choice([1, 2, 3, 4, 5], 1, p=softmax_1d([0.3, 0, 0.4, 0.6, 0]))[0]
    all_brake_remaining_area_ratio = {}
    all_brake_boat=params['all_brake_boat']
    # logger.debug(f' all_brake_boat to get max prob:{all_brake_boat}')
    brakes=params['brakes']
    all_brakes_available_queue=params['all_brakes_available_queue']
    # 获取所有闸室中，每个闸室的剩余可用的面积占比
    for brake_num, e_brake_boat in all_brake_boat.items():
        brake_boat_ = e_brake_boat['brake_boat']
        L, W = brakes[brake_num]
        remaining_area_ratio = 1 - one_brake_area_ratio(brake_boat_, L, W)
        # 当前闸室，可排点队列长度;无可排点时，将剩余可以使用面积占比设为0
        if (len(all_brakes_available_queue[brake_num]) == 0) or (len(brake_boat_) == 6):
            # print(f'brake_num:{brake_num}没有可排点，设置剩余可用面积为零：{all_brakes_available_queue[brake_num]}')
            remaining_area_ratio = 0
        all_brake_remaining_area_ratio[brake_num] = remaining_area_ratio
    return all_brake_remaining_area_ratio

def build_plot_para(brake_boat):
    X = []
    Y = []
    li = []
    wi = []
    N = len(brake_boat)
    for k, v in brake_boat.items():
        li.append(v[1][0])
        wi.append(v[1][1])
        X.append(v[0][0])
        Y.append(v[0][1])
    return np.array(X), np.array(Y), np.array(li), np.array(wi), N

def get_maxprob_brake_num(params):

    all_brake_remaining_area_ratio=all_remaining_brake_area_ratio(params)
    all_brake_remaining_area_ratio_num = all_brake_remaining_area_ratio.keys()
    all_brake_remaining_area_ratio_res = all_brake_remaining_area_ratio.values()
    # print(f'all_brake_remaining_area_ratio={all_brake_remaining_area_ratio}')
    # print(f'softmax_1d(list(all_brake_remaining_area_ratio_res))={softmax_1d(list(all_brake_remaining_area_ratio_res))}')
    ##按照概率分布选择闸次
    # choice_brake_num = np.random.choice(list(all_brake_remaining_area_ratio_num), 1, p=softmax_1d(list(all_brake_remaining_area_ratio_res)))[0]
    # 按照最大概率选择闸次,这样效果要好很多，对比按照概率分布
    # print(f'list(all_brake_remaining_area_ratio_res){list(all_brake_remaining_area_ratio_res)}')
    p = softmax_1d(list(all_brake_remaining_area_ratio_res))
    choice_brake_num = list(all_brake_remaining_area_ratio_num)[np.argmax(p)]
    return choice_brake_num



def quick_sort_multi_brakes(wait_list,brakes):
    '''
    wait_list:待排船队列
    brakes={'0':[L,W],'1':[L,W],'2':[L,W]} 闸室信息，闸的序号和长宽
    :return 返回每个闸室的排布信息
    all_brake_boat =
    {
    0: {'brake_boat': {23: [(0, 0), (92.0, 15.0)], 53: [(0, 15.0), (130.0, 17.0)], 21: [(130.0, 15.0), (130.0, 17.0)], 40: [(92.0, 0), (80.0, 14.0)], 17: [(172.0, 0), (92.0, 15.0)]}, 'best_use_rate': 0.8718487394957983},
    1: {'brake_boat': {30: [(0, 0), (92.0, 15.0)], 49: [(0, 15.0), (92.0, 17.0)], 41: [(92.0, 0), (95.0, 17.0)], 19: [(92.0, 17.0), (85.0, 15.0)], 24: [(177.0, 17.0), (87.0, 14.0)], 45: [(187.0, 0), (77.0, 14.0)]}, 'best_use_rate': 0.8539915966386554},
    2: {'brake_boat': {48: [(0, 0), (87.0, 15.0)], 5: [(0, 15.0), (130.0, 17.0)], 7: [(87.0, 0), (92.0, 15.0)], 37: [(130.0, 15.0), (130.0, 16.0)], 58: [(179.0, 0), (85.0, 14.0)]}, 'best_use_rate': 0.8576680672268907}}
    '''
    # L=280
    # W=34
    # brakes={'1':[L,W],'2':[L,W],'3':[L,W]}

    # 所有闸室的可排序点队列
    all_brakes_available_queue={ i:[(0, 0)] for i in brakes}
    all_brake_boat = {i:{'brake_boat':{}} for i in brakes}  # 船的序号，长，宽，在闸室中的坐标
    for index,each_boat in enumerate(wait_list):
        '''
        先试第一个可排点，再试第二个可排点，能放下（满足约束）就放，否则就放弃该船
        '''
        li,wi=each_boat
        #先假设船满足两个条件，再进行判断，不满足条件就不放，进行下一只船
        #判断该船是否放的下，
        #判断该船与闸室中其它所有船是否重叠；
        #闸室不为空的化，需要新增的与里面所有的进行比较看是否不重叠
        #无可排点时，退出
        all_brakes_available_queue_len={k:len(v) for k,v in all_brakes_available_queue.items()}
        #所有可排点队列长度之和
        all_brake_boat_nums=sum([len(v['brake_boat']) for k,v in all_brake_boat.items()])
        all_brake_nums=len(all_brake_boat)
        all_brake_boat_nums_max=int(0.6 * all_brake_nums*6+0.4* all_brake_nums*5)+1
        # all_brake_boat_nums_max = all_brake_nums*6

        if  (all_brake_boat_nums>=all_brake_boat_nums_max):
            # print(f'所有闸室总船数已达到数量上限{all_brake_boat_nums_max}，本轮结束')
            break
        if (sum(all_brakes_available_queue_len.values()) < 1) :
            logger.debug(f'所有闸室可排点队列长度之和为{sum(all_brakes_available_queue_len.values())}，本轮结束')
            break

        params={'all_brake_boat':all_brake_boat,'brakes': brakes,'all_brakes_available_queue':all_brakes_available_queue}
        choice_brake_num=get_maxprob_brake_num(params)
        all_brake_boat_copy = all_brake_boat.copy()

        L, W = brakes[choice_brake_num]
        #设置添加可排点的条件
        ava_L = 50
        ava_W = 8
        ##最多有三个闸次
        for i in range(len(all_brake_boat)):
            # logger.debug(f'len={len(all_brake_boat_copy)},all_brake_boat_copy={all_brake_boat_copy}')
            flag = False
            for availabel_point in all_brakes_available_queue[choice_brake_num]:

                xi, yi = availabel_point
                in_flag=judge_put(xi,yi,li,wi,L,W)

                brake_boat=all_brake_boat[choice_brake_num]['brake_boat']
                available_queue = all_brakes_available_queue[choice_brake_num]
                #判断能否放下该船
                if in_flag:
                    if len(brake_boat)>0:
                        #判断放下该船后，与闸室中其它的船是否会重叠
                        overlap_flag=False
                        for num_boat,in_boat in brake_boat.items():
                            [(xj,yj),(lj,wj)]=in_boat

                            if not judge_overlab(xi,yi,li,wi,xj,yj,lj,wj):
                                logger.debug(f'该船重叠:brake_num={choice_brake_num},index={index},li={li},wi={wi}')
                                overlap_flag=True
                                break
                        #能放下该船，但是与其它船有重叠，则选下一个排放点进行放
                        if overlap_flag:
                            continue
                        #不重叠时，把该船放入闸室中
                        if not overlap_flag:
                            brake_boat[index]=[(xi,yi),(li,wi)]
                            #移除已用的可排点，增加新的可排点
                            available_queue.remove(availabel_point)
                            # 可排点，应该能放下船，才会加入队列中
                            if (L - xi >= ava_L) and (W - yi - wi >= ava_W):
                                available_queue.append((xi, yi + wi))
                            if (L - xi - li >= ava_L) and (W - yi >= ava_W):
                                available_queue.append((xi + li, yi))
                            #可排点重新排序
                            available_queue=sorted(available_queue, key=(lambda x: [x]))
                            logger.debug(f'该船入闸:brake_num={choice_brake_num},index={index},li={li},wi={wi}')
                            break
                    else:
                        #闸室中一艘船都没有时，直接放
                        brake_boat[index]=[(xi,yi),(li,wi)]
                        #移除已用的可排点，增加新的可排点
                        available_queue.remove(availabel_point)

                        # 可排点，应该能放下船，才会加入队列中
                        if (L - xi >= ava_L) and (W - yi - wi >= ava_W):
                            available_queue.append((xi, yi + wi))
                        if (L - xi - li >= ava_L) and (W - yi >= ava_W):
                            available_queue.append((xi + li, yi))
                        # available_queue.extend([(xi,yi+wi),(xi+li,yi)])
                        # 可排点重新排序
                        available_queue = sorted(available_queue, key=(lambda x: [x]))
                        logger.debug(f'该船入闸:brake_num={choice_brake_num},index={index},li={li},wi={wi}')
                        break
            else:
                logger.debug(f'放弃该船:brake_num={choice_brake_num},index={index},li={li},wi={wi}')
                all_brake_boat_copy.pop(choice_brake_num)
                params = {'all_brake_boat': all_brake_boat_copy, 'brakes': brakes,
                          'all_brakes_available_queue': all_brakes_available_queue}
                all_brake_remaining_area_ratio = all_remaining_brake_area_ratio(params)
                if (len(all_brake_boat_copy)==0) or (sum(list(all_brake_remaining_area_ratio.values())) ==0):
                    logger.debug(f'放弃该船，该船在所有闸室中都放不下，brake_num={choice_brake_num},index={index},li={li},wi={wi}')
                    break
                choice_brake_num = get_maxprob_brake_num(params)
                flag = True
                pass
                #这里当前闸室可排点无法放下该船就放弃该船了，后面要改成，所有闸室可排点尝试后都放不下，才放弃该船
                ##待会根据逻辑改这里先调试运行一下
                #为了相对公平性，应该还是要尝试所有可排点，都不行才放弃；
                # 否则当前闸室放不下就放弃该船，会造成相对不公平以及造成船的浪费
                # 【例如三艘船，第一个闸室只能放两艘，放不下第三艘船时就放弃，但其实第三艘船可以放在第二个闸室,多次排序尝试也许就没问题】

            if not flag:
                break
        else:
            pass
    # print('finished')
    # print('所有闸室排布信息')
    return all_brake_boat


if __name__=='__main__':
    pass
    '''
    {
    0: {'brake_boat': {23: [(0, 0), (92.0, 15.0)], 53: [(0, 15.0), (130.0, 17.0)], 21: [(130.0, 15.0), (130.0, 17.0)], 40: [(92.0, 0), (80.0, 14.0)], 17: [(172.0, 0), (92.0, 15.0)]}, 'best_use_rate': 0.8718487394957983}, 
    1: {'brake_boat': {30: [(0, 0), (92.0, 15.0)], 49: [(0, 15.0), (92.0, 17.0)], 41: [(92.0, 0), (95.0, 17.0)], 19: [(92.0, 17.0), (85.0, 15.0)], 24: [(177.0, 17.0), (87.0, 14.0)], 45: [(187.0, 0), (77.0, 14.0)]}, 'best_use_rate': 0.8539915966386554}, 
    2: {'brake_boat': {48: [(0, 0), (87.0, 15.0)], 5: [(0, 15.0), (130.0, 17.0)], 7: [(87.0, 0), (92.0, 15.0)], 37: [(130.0, 15.0), (130.0, 16.0)], 58: [(179.0, 0), (85.0, 14.0)]}, 'best_use_rate': 0.8576680672268907}}

    '''
    #
    size_dict = {'1': (85.5, 16.3), '2': (99.3, 16.92), '3': (119.53, 22.5), '4': (110, 19.22), '5': (110, 17.2)}
    wait_list = list(size_dict.values()) * 10#[(278-85,34-16)]+
    # random.shuffle(wait_list)
    # wait_list=wait_list[6:12]
    # 按照宽度排序，宽的在前么
    # wait_list=sorted(wait_list,key =lambda x:x[1],reverse=True)
    W = 34
    L = 280
    N = len(wait_list)
    #
    ##################wait_list={index:each for index, each in enumerate(wait_list)}
    brakes = {'1': [L, W], '2': [L, W], '3': [L, W]}
    s1=time.time()
    all_brake_boat=quick_sort_multi_brakes(wait_list,brakes)
    s2=time.time()
    print(f'cost time:{s2-s1}')
    print(f'all_brake_boat:{all_brake_boat}')
    #
    # # # #绘图
    for brake_num,e_brake_boat in all_brake_boat.items():
        area_ratio=one_brake_area_ratio(e_brake_boat['brake_boat'], L, W)
        print(f'brake_num area_ratio={area_ratio}')
        X, Y, li_e, wi_e, N_e=build_plot_para(e_brake_boat['brake_boat'])
        print('绘图')
        plot_example(X, Y, li_e, wi_e,N_e)


