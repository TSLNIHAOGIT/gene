#!/usr/bin/env python




# In[3]:


import pandas as pd




# kind_sheet.head(10)


# In[6]:


# kind_sheet=pd.read_csv('龙钢运输量表_final.csv')


# In[7]:


kind_sheet=pd.read_excel('龙钢运输量表_final-修改(1).xlsx')





kind_sheet['日运输量']=kind_sheet['物质量']/350*10000


# In[10]:


#车辆折算系数 所有大于14t的车都是3.0; 小于14t的  按照2.0计算
def p(row):
    if row['运输车辆的最大装载量']>=14:
        return 3
    else:
        return 2
        


kind_sheet['车辆折算系数']=kind_sheet.apply(lambda row:p(row),axis=1)


# In[11]:


# kind_sheet['运输车辆的最大装载量'].value_counts()


# In[12]:


import math


# In[13]:


kind_sheet.shape


# In[14]:


kind_sheet['车次']=kind_sheet['日运输量']*1.1/kind_sheet['运输车辆的最大装载量']
kind_sheet['车次']=kind_sheet['车次'].apply(lambda x:math.ceil(x))


# In[15]:


kind_sheet['车次'].sum()


# In[16]:


# kind_sheet['车次'].sum()


# In[ ]:





# In[17]:


kind_sheet.drop(columns=['日运输量新'],axis=1,inplace=True)


# In[18]:


kind_sheet=kind_sheet.sort_values(by='物质量',ascending=False)


# In[19]:


kind_sheet.head(20)


# In[20]:


kind_sheet.tail(20)


# In[21]:


# kind=kind_sheet['A'][1:]
o1=kind_sheet['重车起点']
d1=kind_sheet['重车终点']
o2=kind_sheet['空车起点']
d2=kind_sheet['空车终点']
# c1=kind_sheet['H'][1:]
# c2=kind_sheet['I'][1:]
E=kind_sheet['车辆折算系数']
# Q=kind_sheet['日运输量新']

Q=kind_sheet['日运输量']
cap=kind_sheet['运输车辆的最大装载量']


# In[22]:


# kind=kind_sheet['A'][1:]
# o1=kind_sheet['C'][1:]
# d1=kind_sheet['D'][1:]
# o2=kind_sheet['J'][1:]
# d2=kind_sheet['K'][1:]
# c1=kind_sheet['H'][1:]
# c2=kind_sheet['I'][1:]
# E=kind_sheet['G'][1:]
# Q=kind_sheet['E'][1:]
# cap=kind_sheet['F'][1:]


# In[23]:


Q.head()


# In[24]:


#暂时设定为10车次
# kind_sheet['车次']=3


# In[25]:


Amounts1=kind_sheet['车次']
Amounts2=kind_sheet['车次']


# In[26]:


Amounts1.head()


# In[27]:


# type(o1)


# In[204]:


# kind


# In[205]:


# ls


# In[29]:


l=pd.read_csv('distance.csv',header=None) #读取各个路段长度
# a=pd.read_csv('A（可达矩阵）') #读取各路段间的可达矩阵（此处应当按照物料品类进行分类，案列假设7种物料可达矩阵一致）
MSF=pd.read_csv('MSF.csv',header=None)#,'B2:K11');#读取路段的最大服务交通量
FHV=pd.read_csv('FHV.csv',header=None)#,'B2:K11');#读取交通组成修正系数
FD=pd.read_csv('FD.csv',header=None)#,'B2:K11');  #读取方向分布修正系数
FW=pd.read_csv('FW.csv',header=None)#,'B2:K11');  #读取车道宽度、路肩宽度修正系数
FF=pd.read_csv('FF.csv',header=None)#,'B2:K11');  #读取路测干扰修正系数


# In[30]:


# #道路路段：单项双车道,双向四车道
# #将节点列表转为各个路段（双向）
single_double_lane={'road1':[25,26,27],'road2':[17,28,29,30,31,59,32,33,34,35,36]}
def get_all_double_lane(single_double_lane):
    double_lanes=set()
    for road ,path in single_double_lane.items():
        for path_pair in zip(path,path[1:]):
            double_lanes.add(path_pair)
            double_lanes.add((path_pair[1],path_pair[0]))
            print(path_pair)
    return double_lanes
        
    
double_lanes=get_all_double_lane(single_double_lane)    
print('double_lanes',double_lanes)


# In[31]:


# ##禁止重车或空车通行的路段，默认为所有车次
# forbidden_paths={'material_type_index':0,'car_times':None,'forbidden_roads':[14,27]}


# In[32]:


# forbidden_paths.get('material_type_index0',False)


# In[ ]:





# In[ ]:





# In[33]:


FW[FW==1]=0.84


# In[34]:


# 道路宽度6m,0.52;7.5 ,0.56;9m,0.84;
# 10.5m 修正系数取值1   宽度12.5m 取值1.16   14.5m取值1.32  大于16.5 取值1.48   双车道情况下 ；
w={6:0.53,7.5:0.86,9:0.84,10.5:1,12.5:1.16,14.5:1.32,16.5:1.48}

path_w={(5,6):12,(6,5):12,(24,14):14.5,(14,15):14.5,(15,16):14.5,(14, 24): 14.5, (15, 14): 14.5, (16, 15): 14.5 }

def process_w(ew):
    if (ew>=6) & (ew<7.5):
        return  0.53
    elif (ew>=7.5) &( ew <9) :
        return 0.86
    elif (ew>=9) & (ew < 10.5):
        return 0.84
    elif (ew>=10.5) &( ew <12.5) :
        return 1
    elif (ew>=12.5) & (ew <14.5) :
        return 1.16
    elif (ew>=14.5) & (ew < 16.5):
        return 1.32
    elif (ew>= 16.5):
        return 1.48
    else:
        return 0.84
    


# In[35]:


for ep,ew in path_w.items():
    ep_index=(ep[0]-1,ep[1]-1)
    FW.iloc[ep_index]=process_w(ew)
    


# In[36]:


FW.iloc[(14,15)]


# In[37]:


FW.head(10)


# In[38]:


# t={(24,14):14.5,(14,15):14.5,(15,16):14.5}
# t2={(k[1],k[0]):v for k,v in t.items()}
# t2


# In[39]:


FW.head()


# In[40]:


l.head()


# In[41]:


MSF.head()


# In[42]:


FHV.head()


# In[43]:


ot=pd.DataFrame(o1.values.tolist())
dt=pd.DataFrame(d1.values.tolist())


# In[44]:


ot.head()


# In[45]:


dt.head()


# In[46]:


type(dt)


# In[47]:


type(dt.iloc[:,0])


# In[ ]:





# In[48]:


FF.head(20)


# In[49]:


# l=pd.read_excel(path,'L（路段长）').iloc[:,1:]#,'B2:K11');  #读取各个路段长度
# a=pd.read_excel(path,'A（可达矩阵）').iloc[:,1:]#,'B2:K11');  #读取各路段间的可达矩阵（此处应当按照物料品类进行分类，案列假设7种物料可达矩阵一致）
# MSF=pd.read_excel(path,'MSF（最大服务交通量）').iloc[:,1:]#,'B2:K11');#读取路段的最大服务交通量
# FHV=pd.read_excel(path,'FHV（交通组成修正系数）').iloc[:,1:]#,'B2:K11');#读取交通组成修正系数
# FD=pd.read_excel(path,'FD（方向分布系数）').iloc[:,1:]#,'B2:K11');  #读取方向分布修正系数
# FW=pd.read_excel(path,'FW（宽度修正系数）').iloc[:,1:]#,'B2:K11');  #读取车道宽度、路肩宽度修正系数
# FF=pd.read_excel(path,'FF（路测干扰系数）').iloc[:,1:]#,'B2:K11');  #读取路测干扰修正系数

# o1=pd.read_excel(path,'K（物料）','C3:C9');  #读取重车起点
# d1=pd.read_excel(path,'K（物料）','D3:D9');  #读取重车终点
# o2=pd.read_excel(path,'K（物料）','J3:J9');  #读取空车起点
# d2=pd.read_excel(path,'K（物料）','K3:K9');  #读取空车终点
# c1=pd.read_excel(path,'K（物料）','H3:H9');  #读取重车成本
# c2=pd.read_excel(path,'K（物料）','I3:I9');  #读取空车成本
# E=pd.read_excel(path,'K（物料）','G3:G9');     #读取运输物料k的车辆的折算系数
# Q=pd.read_excel(path,'K（物料）','E3:E9');     #读取物料k运输量的集合
# cap=pd.read_excel(path,'K（物料）','F3:F9');   #读取运载物料k的车辆的最大装载量
# alpha=0.8; 


# In[50]:


# c2.head(10)


# In[51]:


l.head()


# In[52]:


n=l.shape[0]
m=kind_sheet.shape[0]


# In[53]:


n


# In[54]:


m


# In[55]:


E.head(20)


# In[ ]:



        


# In[ ]:



    


# In[56]:


import networkx as nx
from matplotlib import pyplot as plt
import numpy as np


# In[57]:


##用最新程序运行


# In[58]:





# In[ ]:





# In[59]:


alpha=0.8
#用下面的代替车辆行驶100次
# alpha=0.08


# In[60]:


##起点，必经点集合（默认走第一个点，饱和之后顺次走下一个点），终点；index是物料类型

##物料0，必经点24，汽车衡720重卡每天（空车需要转为重车进行计算么？还是只计算重车，如果空车经过该汽车衡）


###禁止点集合：某类物料禁止经过该


# In[61]:


# 物料号，车次，禁止的路段;默认所有车次（）
forbidden_paths={ 0:[  None,  (14, 27)]}
# {'material_type_index': 0, 'car_times': None, 'forbidden_roads': [14, 27]}
material_info=forbidden_paths.get(0,False)
material_info[1]



##单向通行和禁止重车通行（有物料种类无关）
#单向通行，一开始就告诉哪些路段是单项通行的：告诉单向路径如1-2-3-4-5；初始化网络时完成
#禁止重车通行（双向），后面需要判断是否为重车，是重车就断开，重车行驶完毕再连接上；动态变化



# In[62]:


a=[1,2,3,4]
a.reverse()
a


# In[63]:


#必经点汽车衡约束
# 物料号，车次，必须经过的节点
##真实情况可能是多种物料经过多个汽车衡（多对多的关系，例如原料（物质1，物质2，物质3），可以经过汽车衡1、汽车衡2、汽车衡3（依次）），
# 如果某个汽车衡超标，就要自动选择一个可用的汽车衡还是怎么做（目前自动提示，已达到数量，然后提建议）？？？？
##采样点情况也一样

must_pass_nodes={0:[None,35,'truck_scale_nodes'],1:[None,35,'truck_scale_nodes']}#物料对应必经点信息
# must_passed_nodes_info={35:'truck_scale_nodes_index',24:'sample_nodes_index'}#


# In[64]:


# G.add_edge(*(14, 27))


# In[164]:


def get_shortest_path(index,car_times,start_end_tuple,car_type):   
    

    
#     for index,( s ,e) in enumerate(start_end_tuple_list):
#     print('start_end_tuple',type(start_end_tuple))
    if (start_end_tuple not in all_paths) or ( set(all_paths.get(start_end_tuple,(None,None)))&all_delete_edges):
        s,e=start_end_tuple

        all_shortest_path=list(nx.all_shortest_paths(G,s,e,'weight'))
        #最短路径有多条时，选择节点数最少的那个最短路径
        if len( all_shortest_path)>1:
            len_min_index=np.argmin([len(each)for each in all_shortest_path])
            all_shortest_path_use=all_shortest_path[len_min_index]
        else:
            all_shortest_path_use=all_shortest_path[0]
        all_heavy_path['{}{}'.format(car_type,index+1)]=all_shortest_path_use

#         print('路径号{},车次{}，{}{} 源节点{}，终点为{},最短路径为：{}'.format(index,car_times,car_type,index+1,s,e,all_shortest_path_use))
        distance=nx.shortest_path_length(G,s,e,'weight')


#         print('路径号{},车次{},{}{}源节点为{}，终点为{},最短距离：{}'.format(index,car_times,car_type,index+1,s,e, distance))
        pairs_list=list(zip(all_shortest_path_use,all_shortest_path_use[1:]))
#         print('pairs_list={}\n'.format(pairs_list))
    
        all_paths[start_end_tuple]=pairs_list
        all_distance[start_end_tuple]=distance
#         all_paths[start_end_tuple].append(pairs_list)
    else:
        pairs_list=all_paths[start_end_tuple]
        distance=all_distance[start_end_tuple]
#         print('已经存在的最短路径为：路径号{},车次{},{},{}'.format(index,car_times,start_end_tuple,pairs_list))

#     G.add_edge(*material_info[1])
    return  index,car_times,start_end_tuple,car_type,pairs_list,distance


# In[165]:


def judge_conditions(index,car_times,start_end_tuple,car_type,pairs_list,distance):   
    success=1#0是失败，1是成功
    res_temp_list=[]
    '''
    1.全部满足时，全部更新路段限制条件，并且返回最短路径和最短距离
    2.当某个路段不满足条件时，返回pair_index对应的路段，临时删除该路段，调用最短路径算法重新执行，然后在判断，直到全部满足条件或者无解时结束
    #重车时删除的路段先不恢复，等到空车时在将删除的路段恢复（相当于重新构建一次网络图，然后安装之前的策略进行），重新运行
    
    
    '''
    
    ##计算每个路段道路通行能力
    ##第一辆车拉着第一种货物一次经过第一个、二个、等各个节点
    e0=E.iloc[index]
    q0=Q.iloc[index]
    c0=cap.iloc[index]
    q_div_c=q0/c0
#     op=e0*math.ceil(q_div_c)
    op=e0
#     ##将重车转为标车
#     if op=='heavy':
# #         print('重车{},{},{}乘以1.5转为标车'.format(index,car_times,car_type))
#         op=op*1.5
# #     print('op',op)

    
#     print('约束最短路径为：',pairs_list)

    ##对于该路径中的所有路段，依次更新负荷值，全部路段满足要求时，该路径可以；
    #如果某个路段不满足要求，那么就要重新计算，并更新负荷值，直到满足要求为止。
    
    
    ###这个地方有问题，只有所有路段都满足通行要求时才能一次性更新，否则不能更新；只能重新计算最短路径然后在判断是否满足要求
    ###当然一个路段一个路段更新也是可以的，但是更新到最好必须是有解的，要是没有解的话得重新计算整条路径或者其它处理方法
    
    ##先假设都能有可行解，后面的待会考虑
    
    
    ##删除路段后也是重新计算最短路，所以还是一条路径满足所有条件时，然后才返回
#     print('预选路径号{},车次{}，{}{} 源节点{}，终点为{},最短路径为：{}'.format(index,car_times,car_type,index+1,start_end_tuple[0],start_end_tuple[1],pairs_list))
    for pair in pairs_list:
        ##已经使用的路段都是满足道路通行能力的   
        pair_index=tuple((int(each)-1 for each in pair))
        
        ##每个路段24小时实际通行能力（车辆数）
        real_amounts=(MSF.iloc[pair_index]*FHV.iloc[pair_index]*FD.iloc[pair_index]*FW.iloc[pair_index]*FF.iloc[pair_index]*24)
        if pair in double_lanes:
#              print('路段{}是单项双车道，乘以1.85'.format(pair))
             real_amounts= real_amounts*1.85
            
        
        
        res_temp= op/real_amounts
        
        
#         print('res_temp={},MSF={},FHV.iloc[pair_index]={},FD.iloc[pair_index]={},FW.iloc[pair_index]={},FF.iloc[pair_index]={}'.format(
#             MSF.iloc[pair_index]*FHV.iloc[pair_index]*FD.iloc[pair_index]*FW.iloc[pair_index]*FF.iloc[pair_index],
#             MSF.iloc[pair_index],
#             FHV.iloc[pair_index],
#             FD.iloc[pair_index],
#             FW.iloc[pair_index],
#             FF.iloc[pair_index]
            
            
            
#             ))
        
        res_temp_list.append(res_temp)
        
        ##可能第一个路段就大于alpha也可能是后面的路段才大于等于alpha
        
#         if res[pair_index]+res_temp<alpha:
        ##这里道路通行能力是双向的：即是整个道路而不是道路上某个方向的车道
        pair_index_invert=tuple((pair_index[1],pair_index[0]))
        if res[pair_index]+res[pair_index_invert]+res_temp<alpha:
            pass
# #             print('res_temp={},pair_res={},pair_index={}'.format(res_temp,res[pair_index],pair_index))
#             res[pair_index]+=res_temp
# #             print('当前最短路径为:pairs_list',pairs_list)
        
#             if pair not in all_pairs_index_new.keys():
#                 all_pairs_index_new[pair]={}
#                 if car_type not in all_pairs_index_new[pair].keys():
#                     all_pairs_index_new[pair][car_type]=[]
#                     all_pairs_index_new[pair][car_type].append(index+1)
#                 else:
#                     all_pairs_index_new[pair][car_type].append(index+1)
                    
                    
#             else:   
#                 if car_type not in all_pairs_index_new[pair].keys():
#                     all_pairs_index_new[pair][car_type]=[]
#                     all_pairs_index_new[pair][car_type].append(index+1)
#                 else:
#                     all_pairs_index_new[pair][car_type].append(index+1)
        else:
            #暂时删除该有项边，重新找最短路径，找到最短路径后在将有向边加上
            print('删除该路段 {}'.format(pair))#暂时注释掉
#             print('res_temp={},pair_res={},pair_index={}\n'.format(res_temp,res[pair_index],pair_index))
            
#             if 
            
            G.remove_edge(*pair)
            all_delete_edges.add(pair)
            success=0
            
            break  
            
#             get_limited_shortest_path(index,start_end_tuple,car_type)
#             get_limited_shortest_path(index,car_times,start_end_tuple,car_type)
            
#             print('添加该路段 {}\n'.format(pair))
#             G.add_edge(*pair)
#             all_delete_edges.remove(pair)
    if success:
            #成功返回最短路径；并整体更新限制条件
            for pair ,res_temp in zip(pairs_list,res_temp_list):
                    pair_index=tuple((int(each)-1 for each in pair))
                    #单元出入口等不计算负荷率
#                     join_set=set(pair)&set(no_rate_nodes)
#                     if join_set:
#                         print('join_set',join_set)
                    if not set(pair)&set(no_rate_nodes):
                        res[pair_index]+=res_temp


                    if pair not in all_pairs_index_new.keys():
                            all_pairs_index_new[pair]={}
                            if car_type not in all_pairs_index_new[pair].keys():
                                all_pairs_index_new[pair][car_type]=[]
                                all_pairs_index_new[pair][car_type].append(index+1)
                            else:
                                all_pairs_index_new[pair][car_type].append(index+1)


                    else:   
                        if car_type not in all_pairs_index_new[pair].keys():
                            all_pairs_index_new[pair][car_type]=[]
                            all_pairs_index_new[pair][car_type].append(index+1)
                        else:
                            all_pairs_index_new[pair][car_type].append(index+1)

                
            return success, pairs_list,distance
    else:      
        #失败返回，失败的那个路段
        return success,pair ,None       
    


# In[ ]:





# In[166]:


def get_limited_shortest_path(index,car_times,start_end_tuple,car_type): 
    
    
    index,car_times,start_end_tuple,car_type,pairs_list,distance=get_shortest_path(index,car_times,start_end_tuple,car_type)
    success,path,distance =judge_conditions(index,car_times,start_end_tuple,car_type,pairs_list,distance)
    
    ##删除某个路段之后，需要重新寻找最短路，即调用最短路径算法
    while True:
          try:
           
               if success:
                    break
               else:
                    index,car_times,start_end_tuple,car_type,pairs_list,distance=get_shortest_path(index,car_times,start_end_tuple,car_type)
                    success,path ,distance=judge_conditions(index,car_times,start_end_tuple,car_type,pairs_list,distance)
          except Exception as e:
            print('error 往后车次无解',e,start_end_tuple,)
            break
    ##获取该条满足条件的最短路径之后，恢复被删除的路径
     
#             all_delete_edges.remove(pair)
     
    all_delete_edges_copy=all_delete_edges.copy()
    for pair in all_delete_edges_copy:
#         print('pairssss',pair)
        G.add_edge(*pair)
        all_delete_edges.remove(pair)
    
    #清空删除的保存路径
#     global all_delete_edges

#     all_delete_edges=set()
        
                    
                    
    return path,distance
    


# In[167]:


o1.head()


# In[168]:


d1.head()


# In[169]:


all_car_se={}
all_car_se['heavy']=list(zip(o1,d1,Amounts1))
all_car_se['light']=list(zip(o2,d2,Amounts2))


# In[170]:


#生成网络图
import math
print('生成一个空的有向图')
G=nx.DiGraph()
print('为这个网络添加节点...')
for i in range(1,l.shape[0]):
    G.add_node(i)

# nx.draw_networkx(G)
# plt.show()
    
print('在网络中添加带权中的边...')
for r in range(l.shape[0]):
    for c in range(l.shape[1]):
        if l.iloc[r,c]>0:
            G.add_weighted_edges_from([(r+1,c+1,l.iloc[r,c])])


# In[171]:


import time


# In[172]:


# pd.DataFrame([[1,2,3],[4,5,6
#                       ]])
a=[2,3,4,0]
print(a.reverse())
a


# In[173]:


must_pass_nodes


# In[174]:


# start_end_tuple_list


# In[188]:


# all_car_se

##单元出入口 大门 汽车衡 采样点直接相连节点构成的路段等不计算道路负荷率
no_rate_nodes=[3,43,5,6,8,9]
# no_rate_nodes=[]


# In[189]:


##道路通行可分为：双向、单向（告诉单向路径列表）、禁止（告诉禁止路径列表）
res=np.zeros((59,59))
all_heavy_path={}
all_pairs_index_new={}

all_datas=[]
all_paths={}
all_distance={}
all_delete_edges=set()
all_must_passed_nodes_operating_rate={}#节点序号：作业率
# pair (2, 3) {'heavy': [1, 2]} 0.03879548100926288 True
# start_end_tuple_list=zip(o1,d1)
start=time.time()
# 数据格式all_car_se={{'heavy': [(15, 32, 97),(15, 43, 95)],'light': [(32, 15, 97),(32, 3, 94)]}
no_heavy_flag=1
# no_heavy_nodes_path=[25,33,34]
no_heavy_nodes_path=[(25,33),(33,34),(34,33),(33,25)]

for car_type,start_end_tuple_list in all_car_se.items():
    #car_type车型：heavy or light
#     start_end_tuple_list={'heavy': [(15, 32, 97),(15, 43, 95)] 包含起始点以及车次
    ##禁止重车通行：第一辆重车时删除；遇到空车时添加
    if car_type=='heavy' and no_heavy_flag:
        #删除禁止道路
        
        G.remove_edges_from(no_heavy_nodes_path)
        no_heavy_flag=0
    elif  car_type=='light':
        #添加删除的路段
        G.add_edges_from(no_heavy_nodes_path)
        no_heavy_flag=1
        
    
    
    for index,( s ,e,amounts) in enumerate(start_end_tuple_list):
       
        
         #会计算最短路径，更新路段使用的容量
    #     print(*(s,e))
        start_end_tuple=(s,e)
        
        ##这里要修改禁止通行的路段是与物料种类无关
        material_info=forbidden_paths.get(index,False)
        if material_info:
            G.remove_edge(*material_info[1])
            
            
        #必经点包括汽车衡以及采样点：与特定的物料绑定
        nodes_info=must_pass_nodes.get(index,False)
      
    
        
        
        
        for car_times in range(amounts):
            ##index要进行修改
#             each_temp=[]
            ##只对重车进行称量
            if nodes_info and car_type=='heavy':
               
        
                pass_node=nodes_info[1]
                rate_type=nodes_info[2]
                
                if pass_node not in  all_must_passed_nodes_operating_rate:
                     car_times_all=0
                    
                
                
                if rate_type=='truck_scale_nodes':
                        t=1.5
                else:
                        t=4
                
                ##汽车衡：以必经点为键，对应某种物料的车次通过不断相加；这里有问题要修改???????????
                
                car_times_all=car_times_all+1
                    
                print('car_times_all',car_times_all)
                all_must_passed_nodes_operating_rate[pass_node]=['{}'.format(rate_type),(car_times_all)*t/1440]
                
                if all_must_passed_nodes_operating_rate[pass_node][1]<0.8:
                    
                   

                    

                    start_end_tuple_1=(start_end_tuple[0],pass_node)
                    start_end_tuple_2=(pass_node,start_end_tuple[1])

                    path_1,dd1=get_limited_shortest_path(index,car_times,start_end_tuple_1,car_type)
                    path_2,dd2=get_limited_shortest_path(index,car_times,start_end_tuple_2,car_type)
                    if isinstance(path_1,list) and isinstance(path_2,list):
                        print('物料种类号{},必经点{}，车次{}，{}{} 源节点{}，终点为{},最短距离为：{}，路径为：{},{}'.format(index,pass_node,car_times,car_type,index+1,s,e,dd1+dd2,path_1,path_2))
                        all_datas.append([index,car_times,'{}{}'.format(car_type,index+1),s,e,dd1+dd2])
                    else:
                        print('无解：物料种类号{},必经点{}，车次{}，{}{} 源节点{}，终点为{},最短距离为：{}，路径为：{},{}'.format(index,pass_node,car_times,car_type,index+1,s,e,None,path_1,path_2))
                        all_datas.append([index,car_times,'{}{}'.format(car_type,index+1),s,e,None])
                else:
                     print('经过必经点无解')
                
            else:
                
                
               
                
            
                    path,dd=get_limited_shortest_path(index,car_times,start_end_tuple,car_type)
                    if isinstance(path,list):
        #              print('pathsssss',path)
                        print('物料种类号{},车次{}，{}{} 源节点{}，终点为{},最短距离为：{}，路径为：{}'.format(index,car_times,car_type,index+1,s,e,dd,path))
                    else:
                        print('无解：物料种类号{},车次{}，{}{} 源节点{}，终点为{},最短距离为：{}，路径为：{}'.format(index,car_times,car_type,index+1,s,e,dd,path))

                    all_datas.append([index,car_times,'{}{}'.format(car_type,index+1),s,e,dd])
        #         if index >1:
        #             break
        #     break

            #     break
    
    
        if material_info:
            G.add_edge(*material_info[1])
    
    
print('cost time:{}s'.format(time.time()-start))
all_df=pd.DataFrame(all_datas,columns=['物料号','车次','车类型','起点','终点','距离'])
all_df.head()

##空车1


# In[ ]:





# In[190]:


car_times_all


# In[191]:


all_must_passed_nodes_operating_rate


# In[192]:


# all_must_passed_nodes_operating_rate


# In[193]:


# all_df.to_excel('res.xlsx',index=False)


# In[194]:


FW.iloc[5,4]


# In[195]:


FW.iloc[4,5]


# In[196]:


print('res max',res[res>0].max())


# In[197]:


#新
# res[res>0]


# In[198]:


res.shape


# In[199]:


tt=res[0:10,0:10]


# In[200]:


for e1 in range(10):
    for e2 in range(10):
        rr=tt[e1,e2]+tt[e2,e1]
        if rr>0.7:
            print(e1,e2,rr)
    


# In[201]:


res[4,5]


# In[202]:


print(res[0:20,0:20])


