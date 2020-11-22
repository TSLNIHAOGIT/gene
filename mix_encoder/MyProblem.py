# -*- coding: utf-8 -*-
"""MyProblem.py"""
import numpy as np
import geatpy as ea
class MyProblem(ea.Problem): # 继承Problem父类
	def __init__(self):
		name = 'MyProblem' # 初始化name（函数名称，可以随意设置）
		M = 1 # 初始化M（目标维数）
		# 初始化maxormins（目标最小最大化标记列表，1：最小化；-1：最大化）
		maxormins = [-1]
		Dim = 6+3 # 初始化Dim（决策变量维数）
		# 初始化决策变量的类型，元素为0表示变量是连续的；1为离散的
		
		##当决策变量的个数与范围相等时，就是全排列，这里就是再加三个变量，否则就是选排列
		varTypes = [0,0,1,1,1,1]+[1]*3
		lb = [-1.5,-1.5,1,1,1,1]+[1]*3 # 决策变量下界
		ub = [2.5,2.5,7,7,7,7]+[7]*3 # 决策变量上界
		lbin = [1] * Dim # 决策变量下边界
		ubin = [1] * Dim # 决策变量上边界
		# 调用父类构造方法完成实例化
		ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
	def aimFunc(self, pop): # 目标函数
		X = pop.Phen # 得到决策变量矩阵
		x1 = X[:, [0]]
		x2 = X[:, [1]]
		x3 = X[:, [2]]
		x4 = X[:, [3]]
		x5 = X[:, [4]]
		x6 = X[:, [5]]
		pop.ObjV = np.sin(2*x1) - np.cos(x2) + 2*x3**2 -3*x4 + (x5-3)**2 + 7*x6 # 计算目标函数值，赋值给pop种群对象的ObjV属性