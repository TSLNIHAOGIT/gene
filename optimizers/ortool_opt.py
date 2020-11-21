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

from ortools.linear_solver import pywraplp

# 首先，调用CBC求解器
# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver('SCIP')
# 整数规划使用pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
# solver = pywraplp.Solver('SolveIntegerProblem',pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING,)

# 定义x和y的定义域，这里是从0到正无穷
x1 = solver.IntVar(0.0, solver.infinity(), 'x1')
x2 = solver.NumVar(0.0, solver.infinity(), 'x2')
x3 = solver.IntVar(0.0, 1.0, 'x3')
# 添加约束：-x1+2*x2+x3<=4
constraint1 = solver.Constraint(-solver.infinity(), 4)
constraint1.SetCoefficient(x1, -1)
constraint1.SetCoefficient(x2, 2)
constraint1.SetCoefficient(x3, 1)

# 添加约束：4*x2-3*x3<=2
constraint2 = solver.Constraint(-solver.infinity(), 2)
constraint2.SetCoefficient(x1, 0)
constraint2.SetCoefficient(x2, 4)
constraint2.SetCoefficient(x3, -3)

# 添加约束：x1-3*x2+2*x3<=3
constraint3 = solver.Constraint(-solver.infinity(), 3)
constraint3.SetCoefficient(x1, 1)
constraint3.SetCoefficient(x2, -3)
constraint3.SetCoefficient(x3, 2)


# 定义目标函数： 3*x1+x2+3*x3+3
objective = solver.Objective()
objective.SetCoefficient(x1, 3)
objective.SetCoefficient(x2, 1)
objective.SetCoefficient(x3, 3)

objective.SetMaximization()
# 获取问题的答案
result_status = solver.Solve()
print('result_status',result_status)
# 判断结果是否是最优解
assert result_status == pywraplp.Solver.OPTIMAL
# 验证一下结果是否正确，这一步不是必要但是推荐加上
assert solver.VerifySolution(1e-7, True)
# 输出结果
print('Number of variables =', solver.NumVariables())
print('Number of constraints =', solver.NumConstraints())
print('Optimal objective value = %d' % solver.Objective().Value())
variable_list = [x1, x2,x3]
for variable in variable_list:
    print('%s = %d' % (variable.name(), variable.solution_value()))
