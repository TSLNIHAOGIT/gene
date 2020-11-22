#encoding=utf-8
import os ,sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..')))
from geatpy_example.frame.schedule.plot_example import plot_example
import random







###############结合遗传算法基本思想
'''
（1）一开始的想法，例如共12艘船，然后遗传算法每次随机选取其中的6艘进行排列，每次只计算这6艘船的适应度函数，进行优化

（2）随机取6艘船固定下来，然后进行全排列，计算完所有6艘船的适应度函数；遗传算法学到的是如何排列该6艘船
     https://blog.csdn.net/u011000290/article/details/46838079


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


def quick_sort_brake(wait_list,L,W):
    # 可排序点队列
    available_queue = [(0, 0)]

    brake_boat = {}  # 船的序号，长，宽，在闸室中的坐标
    for index,each_boat in enumerate(wait_list):
        '''
        先试第一个可排点，再试第二个可排点，能放下（满足约束）就放，否则就放弃该船
        '''
        #初始化时，第一艘船的坐标为（0,0）
        # availabel_point=available_queue[0]

        li,wi=each_boat

        #先假设船满足两个条件，再进行判断，不满足条件就不放，进行下一只船
        #判断该船是否放的下，
        #判断该船与闸室中其它所有船是否重叠；
        #闸室不为空的化，需要新增的与里面所有的进行比较看是否不重叠

        #无可排点时，退出
        if len(available_queue)<1:
            print('无可排点，本轮结束')
            break

        for availabel_point in available_queue:

            xi, yi = availabel_point
            in_flag=judge_put(xi,yi,li,wi,L,W)

            #判断能否放下该船
            if in_flag:
                if len(brake_boat)>0:
                    #判断放下该船后，与闸室中其它的船是否会重叠
                    overlap_flag=False
                    for num_boat,in_boat in brake_boat.items():
                        [(xj,yj),(lj,wj)]=in_boat

                        if not judge_overlab(xi,yi,li,wi,xj,yj,lj,wj):
                            print('该船重叠',index,li,wi)
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

                        #可排点，应该能放下船，才会加入队列中
                        if (L-xi>=85) and (W-yi-wi>=16):
                            available_queue.append((xi,yi+wi))
                        if (L-xi-li>=85) and (W-yi>=16):
                            available_queue.append((xi+li,yi))

                        # available_queue.extend([(xi,yi+wi),(xi+li,yi)])
                        #可排点重新排序
                        available_queue=sorted(available_queue, key=(lambda x: [x]))
                        print('该船入闸',index,li,wi)
                        break


                else:
                    #闸室中一艘船都没有时，直接放
                    brake_boat[index]=[(xi,yi),(li,wi)]
                    #移除已用的可排点，增加新的可排点
                    available_queue.remove(availabel_point)

                    # 可排点，应该能放下船，才会加入队列中
                    if (L - xi >= 85) and (W - yi - wi >= 16):
                        available_queue.append((xi, yi + wi))
                    if (L - xi - li >= 85) and (W - yi >= 16):
                        available_queue.append((xi + li, yi))
                    # available_queue.extend([(xi,yi+wi),(xi+li,yi)])
                    # 可排点重新排序
                    available_queue = sorted(available_queue, key=(lambda x: [x]))
                    print('该船入闸',index,li,wi)
                    break
        else:
            print('放弃该船',index,li,wi)
    print('finished')
    print('闸室信息',brake_boat)
    return brake_boat


if __name__=='__main__':
    size_dict = {'1': (85.5, 16.3), '2': (99.3, 16.92), '3': (119.53, 22.5), '4': (110, 19.22), '5': (110, 17.2)}
    wait_list = list(size_dict.values()) * 2#[(278-85,34-16)]+
    # random.shuffle(wait_list)
    # wait_list=wait_list[6:12]
    # 按照宽度排序，宽的在前么
    # wait_list=sorted(wait_list,key =lambda x:x[1],reverse=True)
    W = 34
    L = 280
    N = len(wait_list)
    
    #wait_list={index:each for index, each in enumerate(wait_list)}

    brake_boat=quick_sort_brake(wait_list,L,W)

    X=[]
    Y=[]
    li_e=[]
    wi_e=[]

    s=0
    for k,v in brake_boat.items():
        s=s+v[1][0]*v[1][1]

        X.append(v[0][0]/L)
        Y.append(v[0][1]/W)
        li_e.append(v[1][0]/L)
        wi_e.append(v[1][1]/W)


    print('面积利用率',s/(L*W))

    N_e=len(brake_boat)

    plot_example(X, Y, li_e, wi_e,N_e)
    print('plot finished')

    '''
    F:\陶士来文件\software\python3_6_5\python.exe E:/tsl_file/python_project/gene/geatpy_example/frame/schedule/quick_sort_brake.py
    sys sss argv11 ['E:/tsl_file/python_project/gene/geatpy_example/frame/schedule/quick_sort_brake.py']
    sys sss argv22 ['E:/tsl_file/python_project/gene/geatpy_example/frame/schedule/quick_sort_brake.py']
    该船入闸 0 85.5 16.3
    该船入闸 1 99.3 16.92
    该船重叠 2 110 19.22
    放弃该船 2 110 19.22
    该船重叠 3 110 17.2
    该船入闸 3 110 17.2
    该船入闸 4 85.5 16.3
    该船重叠 5 99.3 16.92
    该船重叠 5 99.3 16.92
    放弃该船 5 99.3 16.92
    finished
    闸室信息 {0: [(0, 0), (85.5, 16.3)], 1: [(0, 16.3), (99.3, 16.92)], 3: [(99.3, 16.3), (110, 17.2)], 4: [(85.5, 0), (85.5, 16.3)]}
    plot finished
    
    Process finished with exit code 0
    
    '''
