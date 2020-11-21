#encoding=utf8
#导入cplex
import cplex
from cplex.exceptions import CplexError

'''
https://blog.csdn.net/weixin_42644765/article/details/105145534
max z=3*x1+x2+3*x3+3

st:
-x1+2*x2+x3<=4
4*x2-3*x3<=2
x1-3*x2+2*x3<=3
x1,x2,x3>=0
x1为整数
x3为0-1变量

最优解
16.25
[4.0, 1.25, 1.0]

'''
import numpy as np

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
wait_list=wait_list[0:6]

li=np.array([each[0] for each in wait_list])
wi=np.array([each[1] for each in wait_list])
N=len(wait_list)
W=34
L=280


'''
变量个数：
x1-xN
y1-yN
e1-eN

s11-sNN (i!=j)
u11-uNN(i!=j)

'''

my_obj=li*wi/(L*W)#目标函数系数
my_ctype='ICI'#目标函数变量的类型，一般就是C,整数类型就是I就是integer
my_ub=[cplex.infinity, cplex.infinity,1]#变量的约束条件上限
my_lb=[0,0,0]#变量的约束条件下限
my_colnames=['x1','x2','x3']#column names列向量的名字
my_rhs=[4.0,2.0,3.0]#约束条件的值相当于b
my_rownames=['r1','r2','r3']#row names行向量的名字
#是约束条件的形式，L为小于号“less-than”,大于号是‘G’，即'greater than'
my_sense='LLL'

def populatebyrow(prob):
    #设置目标函数类型：求max or min
    prob.objective.set_sense(prob.objective.sense.maximize)
    #设置（增加）变量，明确目标函数，约束条件上限、下限，变量类型，还有变量名称
    prob.variables.add(obj=my_obj,lb=my_lb,ub=my_ub,types=my_ctype,
                      names=my_colnames)
    #对应的约束方程
    rows=[[['x1','x2','x3'],[-1.0,2.0,1.0]],
          [['x2','x3'],[4.0,-3.0]],
          [['x1','x2','x3'],[1.0,-3.0,2.0]]]
    #设置（增加）约束条件
    prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
                         rhs=my_rhs,names=my_rownames)

#初始化模型
my_prob=cplex.Cplex()
#计算
handle=populatebyrow(my_prob)
#求解
my_prob.solve()
#输出结果
print(my_prob.solution.get_objective_value())
x = my_prob.solution.get_values()
print(x)
