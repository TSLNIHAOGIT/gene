import numpy as np
import geatpy as ea

class MyProblem(ea.Problem): # 继承Problem父类

    def __init__(self):
        name = 'BNH'                                    # 初始化name（函数名称，可以随意设置）
        M = 2                                           # 初始化M（目标维数）
        maxormins = [1] * M                             # 初始化maxormins
        Dim = 2                                         # 初始化Dim（决策变量维数）
        varTypes = [0] * Dim                            # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = [0] * Dim                                  # 决策变量下界
        ub = [5, 3]                                     # 决策变量上界
        lbin = [1] * Dim                                # 决策变量下边界
        ubin = [1] * Dim                                # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):                             # 目标函数
        Vars = pop.Phen                                 # 得到决策变量矩阵
        x1 = Vars[:, [0]]
        x2 = Vars[:, [1]]
        f1 = 4*x1**2 + 4*x2**2
        f2 = (x1 - 5)**2 + (x2 - 5)**2
        # 采用可行性法则处理约束
        pop.CV = np.hstack([(x1 - 5)**2 + x2**2 - 25, -(x1 - 8)**2 - (x2 - 3)**2 + 7.7])
        # 把求得的目标函数值赋值给种群pop的ObjV
        pop.ObjV = np.hstack([f1, f2])

    def calBest(self):                                  # 计算全局最优解
        N = 10000                                       # 欲得到10000个真实前沿点
        x1 = np.linspace(0, 5, N)
        x2 = x1.copy()
        x2[x1 >= 3] = 3
        return np.vstack((4 * x1**2 + 4 * x2**2, (x1 - 5)**2 + (x2 - 5)**2)).T