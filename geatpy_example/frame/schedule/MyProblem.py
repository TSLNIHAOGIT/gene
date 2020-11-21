# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
##遗传算法解决问题分为两种，一种是将问题转为规划类问题求解；一种是直接对原问题进行求解


###对于之前的车辆路径问题目前也是两个思路：
'''
1.直接转为规划类问题
2.直接对原问题进行求解
'''



"""
该案例展示了一个简单的离散型决策变量最大化目标的单目标优化问题。
max f = 4000*x1+3000*x2
s.t.
2*x1+x2<=10
x1+x2<=8
x2<=7
x1>=0
x2>=0


W=280
L=34

max 1/(L*W)
"""



wait_list=[(119.53, 22.5),
 (99.3, 16.92),
 (85.5, 16.3),
 (110, 17.2),
 (110, 19.22),
 (119.53, 22.5),
 (99.3, 16.92),
 (99.3, 16.92),
 (85.5, 16.3),
 (110, 17.2),
 (110, 17.2),
 (119.53, 22.5)]
wait_list=wait_list[0:12]

li=np.array([each[0] for each in wait_list])
wi=np.array([each[1] for each in wait_list])
N=len(wait_list)
W=34
L=280
NIND = 6000

'''

def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = N*2+N+(N**2-N)*2  # 初始化Dim（决策变量维数）
        varTypes = [1] * N*2+[0]*(N+(N**2-N)*2)  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0]*Dim  # 决策变量下界
        ub = [L-l_w[0] for l_w in wait_list]+[W-l_w[1] for l_w in wait_list]+[1]*(N+(N**2-N)*2 )   # 决策变量上界
        lbin = [0] * N*2+[1]*(N+(N**2-N)*2 )  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [0] * N*2+[1]*(N+(N**2-N)*2 )  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen  # 得到决策变量矩阵
        X=Vars[:, 0:N]#(4000, 12)
        Y=Vars[:,N:2*N]#(4000, 12)
        E=Vars[:,2*N:3*N]#(4000, 12)
        #S=Vars[:,3*N:3*N+N**2-N]#(4000, 132)
        #U=Vars[:,N**2+2*N:]#(4000, 132)


'''





class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 2  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = N*2+N+(N**2)*2  # 初始化Dim（决策变量维数）
        varTypes = [0] * N*2+[1]*(N+(N**2)*2)  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0]*Dim  # 决策变量下界
        ub = [L-l_w[0] for l_w in wait_list]+[W-l_w[1] for l_w in wait_list]+[1]*(N+(N**2)*2 )   # 决策变量上界
        lbin = [1] * N*2+[1]*(N+(N**2)*2 )  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * N*2+[1]*(N+(N**2)*2 )  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen  # 得到决策变量矩阵
        X=Vars[:, 0:N]#(4000, 12)
        Y=Vars[:,N:2*N]#(4000, 12)
        E=Vars[:,2*N:3*N]#(4000, 12)
        S=Vars[:,3*N:3*N+N**2].reshape(-1,N,N)#(4000, 12, 12)
        U=Vars[:,3*N+N**2:].reshape(-1,N,N)#(4000, 12, 12)
        # SU=S+U+S.transpose((0,2,1))+U.transpose((0,2,1))
        
        
        
        L_Constrain=np.zeros((NIND,N,N))
        W_Constrain=np.zeros((NIND,N,N))
        SU_Constrain=np.zeros((NIND,N,N))
        for i in range(N):
            for j in range(N):
                if i!=j:
                    L_Constrain[:,i,j]=X[:,i]-X[:,j]+L*S[:,i,j]+li[i]-L
                    W_Constrain[:,i,j]=Y[:,i]-Y[:,j]+W*U[:,i,j]+wi[i]-W
                    if i<j:
                        SU_Constrain[:,i,j]=S[:,i,j]+U[:,i,j]+S[:,j,i]+U[:,j,i]
                    


        obj1= (np.sum(X*Y*E,axis=1)/(L*W)).reshape(-1,1) # (4000,)#面积最大
        obj2= (1/(np.sum(E,axis=1)+1)).reshape(-1,1) # (4000,)#数量最少
        pop.ObjV = np.hstack([obj1,obj2])#计算目标函数值，赋值给pop种群对象的ObjV属性,求矩阵列和，即变量之和
        pop.CV = np.hstack([E*(X+np.array(li))-L,  # 第一个约束
                            E*(Y+np.array(wi))-W,  # 第二个约束
                            # (1-SU_Constrain).reshape(-1,N**2),         # 第三个约束#该约束会导致无可行解
                            # ( SU_Constrain-2).reshape(-1, N ** 2),  # 第三个约束#该约束会导致无可行解

                            L_Constrain.reshape(-1,N**2),
                            W_Constrain.reshape(-1,N**2),
                            (np.sum(X*Y*E,axis=1)-(L*W)).reshape(-1,1)
                        
                            
                            ])