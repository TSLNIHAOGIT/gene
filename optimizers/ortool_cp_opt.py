from ortools.sat.python import cp_model
#https://zhuanlan.zhihu.com/p/55866072
'''
max z=3*x1+x2+3*x3+3

st:
-x1+2*x2+x3<=4
4*x2-3*x3<=2
x1-3*x2+2*x3<=3
x1,x2,x3>=0
x1为整数
x3为0-1变量
'''

def main():

    # 首先是创建模型
    model = cp_model.CpModel()

    # 定义变量，指定变量的范围
    # 根据题目可以知道，x,y,z 的最大值肯定不超过50
    # var_upper_bound 相当于减少了搜索空间范围
    # 注意，我们这里定义的是整数变量
    var_upper_bound = max(50, 45, 37)
    x = model.NewIntVar(0, var_upper_bound, 'x')
    y = model.NewIntVar(0, var_upper_bound, 'y')
    z = model.NewIntVar(0, 1, 'z')

    # 添加约束
    # 注意到，我们第一个约束条件是 x + 7⁄2 y + 3⁄2 z  ≤   25
    # 但是 CP-SAT 只能处理整数问题，所以需要对第一个约束处理，使得系数全部是整数
    # 方法很简单，左边右边都乘以2就可以了
    model.Add(-x+2*y+z<=4)
    # 添加第二个约束
    model.Add(4*y-3*z<=2)
    # 添加第三个约束
    model.Add(x-3*y+2*z<=3)

    # 定义目标函数
    model.Maximize(3*x+y+3*z)

    # 求解并打印结果
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print('Maximum of objective function: %i' % solver.ObjectiveValue())
        print('x value: ', solver.Value(x))
        print('y value: ', solver.Value(y))
        print('z value: ', solver.Value(z))


if __name__ == '__main__':
    main()

# # 结果
# Maximum of objective function: 19
#
# x value:  4
# y value:  1
# z value:  1