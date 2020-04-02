from sko.GA import GA
from sko.GA import GA_TSP
# demo_func = lambda x: x[0] ** 2 + (x[1] - 0.05) ** 2 + x[2] ** 2
# ga = GA(func=demo_func, n_dim=3, max_iter=500, lb=[0, 0, 0], ub=[1, 1, 1], precision=[1, 1e-7, 1e-7])
# best_x, best_y = ga.run()
# print('best_x:', best_x, '\n', 'best_y:', best_y)
import numpy as np


weights = {'(1, 2)': 36, '(1, 3)': 27, '(2, 4)': 18, '(2, 5)': 20, '(2, 3)': 13, '(3, 5)': 12,
                        '(3, 6)': 23,
                        '(4, 7)': 11, '(4, 8)': 32, '(5, 4)': 16, '(5, 6)': 30, '(6, 7)': 12, '(6, 9)': 38,
                        '(7, 8)': 20,
                        '(7, 9)': 32, '(8, 9)': 15, '(8, 10)': 24, '(9, 10)': 13}


def demo_func(x):
    # print('x',x)
    #x是10*10的矩阵
    x=x.reshape((10,10))
    # print('x',x)
    s=0
    for node_pair ,w in weights.items():
        key = eval(node_pair)
        i = key[0] - 1
        j = key[1] - 1
        s=s+x[i,j]*w
    return s
constraint_eq=[
    lambda x:np.sum(x,axis=0)[1:-1]-np.sum(x,axis=1)[1:-1],
    lambda x: np.sum(x[0,:])-1,
    lambda x: np.sum(x[:,0]) ,

    lambda x: np.sum(x[:,-1])-1,
    lambda x: np.sum(x[-1,:]) ,
]

constraint_ueq=[
    lambda x:np.sum(x,axis=1)-1,
    lambda x:np.sum(x,axis=0)-1,
]




#
# demo_func = lambda x: -(x[0] * 4000 + x[1]* 3000)##目标函数是求最小值
# #约束条件小于等于0是满足
# constraint_ueq=[
#     lambda x:2*x[0]+x[1]-10,
#     lambda x:x[0]+x[1]-8,
#     lambda x:x[1]-7,
#     # lambda x:-x[0],
#     # lambda x:-x[1],
# ]

ga = GA(func=demo_func, n_dim=(10,10), constraint_ueq=constraint_ueq,max_iter=500, lb=[0]*100, ub=[1]*100,
        precision=[1]*100)
res = ga.run()
# print('best_x:', best_x, '\n', 'best_y:', best_y)
print(res)